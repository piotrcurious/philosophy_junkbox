"""
Full Dataset Ingestion & Entity-Relation Extractor
Parses raw MHTML drift logs without truncation.
Extracts spatial, cybernetic, medical, social, and infrastructure entities,
along with numerical metrics, verbatim log excerpts, paragraph co-occurrences, and Prolog relational facts.
"""

import os
import re
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Tuple

def extract_raw_text_from_mhtml(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    html_parts = re.findall(r'Content-Type:\s*text/html.*?\n\n(.*?)(?=\n------=|\Z)', content, re.DOTALL)
    full_text = ""
    for part in html_parts:
        decoded = re.sub(r'=\n', '', part)
        decoded = re.sub(r'=([0-9A-Fa-f]{2})', lambda m: chr(int(m.group(1), 16)), decoded)
        soup = BeautifulSoup(decoded, 'html.parser')
        full_text += soup.get_text(separator=' ') + "\n"

    if not full_text:
        soup = BeautifulSoup(content, 'html.parser')
        full_text = soup.get_text(separator=' ')

    return full_text

def extract_full_dataset(log_paths: List[str]) -> Dict[str, Any]:
    nodes_map = {}
    co_occurrence_map = {}

    spatial_patterns = [
        (r'Saint-Saturnin.*?(?=\.|\n)', "Saint-Saturnin", "Spatial Corridor"),
        (r'A75.*?(?=\.|\n)', "A75 Highway Corridor", "Spatial Corridor"),
        (r'Montceau-les-Mines.*?(?=\.|\n)', "Montceau-les-Mines", "Spatial Corridor"),
        (r'Belfort.*?(?=\.|\n)', "Belfort-Lure Belt", "Spatial Corridor"),
        (r'Lure.*?(?=\.|\n)', "Lure Zone", "Spatial Corridor"),
        (r'Aire de la Guye.*?(?=\.|\n)', "Aire de la Guye", "Ecological Checkpoint"),
        (r'Clermont-Ferrand.*?(?=\.|\n)', "Clermont-Ferrand Hub", "Spatial Corridor"),
        (r'Haute-Garonne.*?(?=\.|\n)', "Haute-Garonne Region", "Healthcare Strain Zone"),
        (r'Puy-de-Dôme.*?(?=\.|\n)', "Puy-de-Dôme Region", "Healthcare Strain Zone"),
        (r'Mond\'Arverne.*?(?=\.|\n)', "Mond'Arverne Mobility Area", "Spatial Corridor")
    ]

    cybernetic_patterns = [
        (r'BMW.*?(?=\.|\n)', "BMW SaaS Platform", "Cybernetic Platform"),
        (r'OTA.*?(?=\.|\n)', "Over-The-Air Update ECU", "Cybernetic Platform"),
        (r'subskrypcj.*?siedzeñ.*?(?=\.|\n)', "Seat Heating Paywall", "Cybernetic Lockin"),
        (r'samochód.*?uczestnik.*?(?=\.|\n)', "Connected Car Platform Node", "Cybernetic Platform"),
        (r'Autofac.*?(?=\.|\n)', "Anti-Autofac Meta-Regulator", "Cybernetic Control")
    ]

    metabolic_patterns = [
        (r'IGAS.*?(?=\.|\n)', "IGAS Medical Audit", "Healthcare Strain"),
        (r'brak.*?lekarz.*?(?=\.|\n)', "Medical & Psychiatric Desert", "Healthcare Strain"),
        (r'odwo³ane.*?dy¿ury.*?(?=\.|\n)', "Emergency Unit Closures", "Healthcare Strain"),
        (r'brak energii.*?58%.*?(?=\.|\n)', "Youth Energy Depletion (58%)", "Metabolic Deficit"),
        (r'trudnoúci koncentracji.*?44%.*?(?=\.|\n)', "Concentration Deficit (44%)", "Metabolic Deficit")
    ]

    all_patterns = spatial_patterns + cybernetic_patterns + metabolic_patterns

    for path in log_paths:
        if not os.path.exists(path):
            continue
        text = extract_raw_text_from_mhtml(path)
        paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 40]

        for p in paragraphs:
            matching_entities_in_p = set()
            for pattern, entity_name, category in all_patterns:
                if re.search(pattern, p, re.IGNORECASE):
                    matching_entities_in_p.add(entity_name)
                    if entity_name not in nodes_map:
                        nodes_map[entity_name] = {
                            "id": entity_name,
                            "category": category,
                            "excerpts": [],
                            "stats": [],
                            "raw_count": 0
                        }
                    nodes_map[entity_name]["raw_count"] += 1
                    if len(nodes_map[entity_name]["excerpts"]) < 5:
                        clean_p = re.sub(r'\s+', ' ', p)[:300]
                        nodes_map[entity_name]["excerpts"].append(clean_p)
                        nums = re.findall(r'\d+(?:\.\d+)?%?', clean_p)
                        if nums:
                            nodes_map[entity_name]["stats"].extend(nums)

            # Track explicit co-occurrences in the same paragraph
            matching_list = sorted(list(matching_entities_in_p))
            for i in range(len(matching_list)):
                for j in range(i + 1, len(matching_list)):
                    pair = (matching_list[i], matching_list[j])
                    co_occurrence_map[pair] = co_occurrence_map.get(pair, 0) + 1

    node_list = list(nodes_map.values())
    relational_facts = []
    for (n1, n2), count in co_occurrence_map.items():
        relational_facts.append({
            "predicate": "co_occurs_with",
            "subject": n1,
            "object": n2,
            "co_occurrence_count": count
        })

    return {
        "nodes": node_list,
        "total_entities_extracted": len(node_list),
        "relational_facts": relational_facts
    }

if __name__ == "__main__":
    dataset = extract_full_dataset([
        "drifting_logs/Dryf psychogeograficzny",
        "drifting_logs/Stwórz dryft Belfort Lure"
    ])
    output_path = "drifting_logs/full_extracted_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"Extracted full dataset with {dataset['total_entities_extracted']} entities saved to {output_path}")
