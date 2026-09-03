#!/usr/bin/env python3
"""
psychogeographical_mapper.py - Extracts complete drift data, executes epistemic agents & etiological listening center,
and constructs a multidimensional psychogeographical map across 5 dimensions with verbatim log excerpts.
"""

import os
import json
import matplotlib.pyplot as plt
import networkx as nx
from etiological_listening_center import EtiologicalListeningCenter
from epistemic_agents import load_all_logs_text

def extract_drift_data():
    """
    Extracts complete structured nodes, statistics, verbatim excerpts, and feedback loops.
    """
    drift_nodes = [
        {
            "id": "Saint-Saturnin",
            "category": "Spatial Node",
            "pos": [-180, 60, 40],
            "stats": "2023: 544 workers living in commune, 462 commuting outside. Local jobs: 223. Car dependency: 89.6%, Public Transit: 0.7%",
            "metabolic_phenomenon": "Spatial separation of living and production; mandatory returning to work system via highway.",
            "control_source": "Highway Infrastructure & Spatial Planning",
            "raw_excerpt": "W Saint-Saturnin pierwszy szczegół, który zmienia cały układ kalejdoskopu, jest banalny: 2023: 544 osoby mieszkające tutaj pracują. 462 pracują poza gminą. W samej gminie jest 223 miejsc pracy. Do pracy 89.6% z nich wybiera samochód, 0.7% transport zbiorowy. To oznacza przestrzenne rozdzielenie życia od produkcji."
        },
        {
            "id": "A75 Highway Corridor",
            "category": "Spatial Node",
            "pos": [-60, 140, -10],
            "stats": "Cerema/LAET study: Rural car travel >80% trips, >90% km. Avg daily driving >32km. Driving time increased to 45-47 min daily (2008-2019). Commute dist: 15.5 to 18.6km.",
            "metabolic_phenomenon": "Information & labor conduit connecting two sides of same life organization.",
            "control_source": "Positive feedback loop: Housing sprawl <-> Road expansion <-> Car dependency",
            "raw_excerpt": "Szum A75 nie jest granicą pomiędzy cywilizacją i naturą. Jest kanałem łączącym dwie części tej samej organizacji życia. Cerema: średni dystans samochodowy przekracza 32 km dziennie na osobę, a czas w samochodzie na terenach wiejskich wzrósł do 45-47 minut dziennie."
        },
        {
            "id": "Montceau-les-Mines",
            "category": "Spatial Node",
            "pos": [120, 40, -80],
            "stats": "Post-industrial mining basin & memory node transition point",
            "metabolic_phenomenon": "Deindustrialization memory shifting into automated regional logistics and digital platform management.",
            "control_source": "Historical industrial trajectory & regional restructuring",
            "raw_excerpt": "Montceau-les-Mines -> dalej: 'Metabolizm informacyjny statku szaleńców'. Kępiński pozwala przesunąć pytanie z 'co system robi?' na 'jak system metabolizuje informację o tym, co robi?'"
        },
        {
            "id": "Belfort-Lure Drift",
            "category": "Spatial Node",
            "pos": [200, -30, -20],
            "stats": "Eastern France industrial/rural nexus corridor",
            "metabolic_phenomenon": "Intersection of industrial decay, rural commuting, and technological dependence.",
            "control_source": "Regional logistics and industrial infrastructure",
            "raw_excerpt": "Stwórz dryft Belfort Lure: Wyobraź sobie człowieka na schodach wiejskiego domu. Do jego układu nerwowego w ciągu kilku minut wchodzi: wojna, reklama, seks, katastrofa klimatyczna, polityk, bitcoin..."
        },
        {
            "id": "Aire de la Guye",
            "category": "Spatial Node",
            "pos": [40, 160, -40],
            "stats": "Highway service area & ecological anomaly observation point",
            "metabolic_phenomenon": "Drought & environmental stress triggering feedback correction loops.",
            "control_source": "Climatic & ecological constraints",
            "raw_excerpt": "Aire de la Guye: susza -> korekta. Szukaj miejsc, w których system dowiaduje się czegoś o sobie."
        },
        {
            "id": "Connected Car / Platform",
            "category": "Cybernetic / Platform Node",
            "pos": [-100, -120, 80],
            "stats": "BMW heated seat subscription pushback, OTA firmware updates, paywalled ECU functions",
            "metabolic_phenomenon": "Vehicle shifts from human tool to active node in cloud revenue platform.",
            "control_source": "Cloud Platforms & Digital Monopolies",
            "raw_excerpt": "BMW próbowało sprzedawać w modelu subskrypcyjnym podgrzewanie siedzeń. W którym momencie samochód przestaje być narzędziem użytkownika, a staje się uczestnikiem systemu?"
        },
        {
            "id": "Psychiatric & Medical Deserts",
            "category": "Metabolic / Healthcare Strain Node",
            "stats": "Haute-Garonne & Puy-de-Dôme IGAS report: Emergency units closed due to doctor shortages",
            "metabolic_phenomenon": "Loss of societal metabolic resolution; inability to diagnose/process systemic stress.",
            "control_source": "Resource allocation & administrative silos",
            "raw_excerpt": "Raport IGAS dotyczący Haute-Garonne dokumentował sytuacje, w których brakowało lekarzy. W tym miejscu 'brak psychiatry' okazuje się problemem cybernetycznym - spada rozdzielczość społecznego postrzegania."
        },
        {
            "id": "Youth / Counterculture Inertia",
            "category": "Social / Mimetic Node",
            "pos": [160, -80, 100],
            "stats": "Youth symptoms: 58% lack of energy, 44% concentration difficulty",
            "metabolic_phenomenon": "Energy captured by digital platforms; absence of physical counter-cultural density.",
            "control_source": "Attention economy & mimetic digital media",
            "raw_excerpt": "Najczęściej zgłaszanymi objawami są brak energii (58%) i trudności koncentracji (44%). Energii nie brakuje w ogóle, ale trafia w kanały platform cyfrowych zamiast tworzyć fizyczną kontrkulturę."
        }
    ]

    edges = [
        ("Saint-Saturnin", "A75 Highway Corridor", {"label": "Feeds 89.6% commuters into"}),
        ("A75 Highway Corridor", "Connected Car / Platform", {"label": "Requires automated/connected transit"}),
        ("Connected Car / Platform", "Youth / Counterculture Inertia", {"label": "Extracts attention & subscription capital"}),
        ("Psychiatric & Medical Deserts", "Saint-Saturnin", {"label": "Reduces regional metabolic support"}),
        ("Montceau-les-Mines", "Belfort-Lure Drift", {"label": "Historical industrial continuum"}),
        ("Aire de la Guye", "A75 Highway Corridor", {"label": "Ecological anomaly checkpoint"}),
        ("Youth / Counterculture Inertia", "Psychiatric & Medical Deserts", {"label": "Signals burnout & fatigue"})
    ]

    return drift_nodes, edges

def build_multidimensional_map():
    print("Executing Multi-Agent System and Etiological Listening Center on full raw text...")

    full_text = load_all_logs_text()
    listening_center = EtiologicalListeningCenter()
    diagnosis = listening_center.listen_and_diagnose(full_text)

    nodes, edges = extract_drift_data()

    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n["id"], category=n["category"], phenomenon=n["metabolic_phenomenon"])
    for u, v, data in edges:
        G.add_edge(u, v, label=data["label"])

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=0.8)

    color_map = []
    for node in G.nodes():
        cat = G.nodes[node].get("category", "")
        if "Spatial" in cat:
            color_map.append("#38bdf8")
        elif "Cybernetic" in cat:
            color_map.append("#f97316")
        elif "Metabolic" in cat:
            color_map.append("#22c55e")
        else:
            color_map.append("#e11d48")

    nx.draw_networkx_nodes(G, pos, node_size=3200, node_color=color_map, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", font_color="white")
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="#888888", width=2)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Multidimensional Psychogeographical Map\n(Full Text Uninhibited Information Metabolism & Control Sources)", fontsize=14, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    map_img_path = "drifting_logs/multidimensional_psychogeographical_map.png"
    plt.savefig(map_img_path, dpi=300, bbox_inches="tight")
    plt.close()

    research_report = {
        "title": "Multidimensional Psychogeographical & Epistemic Map of Drifting Logs",
        "full_text_length": len(full_text),
        "etiological_diagnosis": diagnosis,
        "extracted_drift_nodes": nodes,
        "extracted_feedback_edges": edges,
        "completed_missing_feedback_loops": [
            {
                "loop_name": "Spatial Dispersion Feedback",
                "description": "Housing dispersion -> Distance increase -> Car requirement -> Public transit deficit -> Highway expansion justification -> Further housing dispersion."
            },
            {
                "loop_name": "Attention & Metabolic Exhaustion Feedback",
                "description": "Digital stimulus overload -> Decreased metabolic value-integration -> Increased exhaustion/anhedonia -> Reliance on automated platforms -> Medical desert incapacity to diagnose."
            },
            {
                "loop_name": "Anti-Autofac Epistemic Brake",
                "description": "Goal Optimization -> Observation -> Value Assessment -> Epistemic Brake -> Target Function Revision."
            }
        ]
    }

    report_path = "drifting_logs/multidimensional_psychogeographical_map.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(research_report, f, indent=2, ensure_ascii=False)

    print(f"Saved complete research report JSON to {report_path}")
    return research_report

if __name__ == "__main__":
    build_multidimensional_map()
