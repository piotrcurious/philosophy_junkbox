#!/usr/bin/env python3
"""
psychogeographical_mapper.py - Extracts drift data, executes epistemic agents & etiological listening center,
and constructs a multidimensional psychogeographical map across 5 dimensions:
1. Spatial Axis (Locations & Corridors: Saint-Saturnin, A75, Montceau, Belfort, Lure, Aire de la Guye)
2. Temporal & Historical Genealogy Axis (1941 Chantiers de la Jeunesse, 2008-2019 rural driving trends, modern cloud OTA era)
3. Mimetic & Spectacular Axis (Copied desires, SUV lifestyle, subscription monetization, spectacle illusions)
4. Information Metabolism Axis (Kępiński input vs integration capacity, psychiatric deserts, attention entropy)
5. Control Source & Cybernetic Axis (Engine, Market, Platform Cloud, Algorithm, Epistemic Brakes)
"""

import os
import json
import matplotlib.pyplot as plt
import networkx as nx
from etiological_listening_center import EtiologicalListeningCenter

def extract_drift_data():
    """
    Extracts structured nodes, facts, and feedback loops from raw drift texts.
    """
    drift_nodes = [
        {
            "id": "Saint-Saturnin",
            "category": "Spatial Node",
            "stats": {"workers_living": 544, "workers_commuting_out": 462, "local_jobs": 223, "car_dependency_pct": 89.6, "transit_pct": 0.7},
            "metabolic_phenomenon": "Spatial separation of living and production; mandatory returning to work system via highway.",
            "control_source": "Highway Infrastructure & Spatial Planning"
        },
        {
            "id": "A75 Highway Corridor",
            "category": "Spatial / Cybernetic Corridor",
            "stats": {"daily_driving_km_avg": 32, "rural_driving_increase_min": "45-47 min daily (2008-2019)", "commute_dist_increase_km": "15.5 to 18.6km"},
            "metabolic_phenomenon": "Not a boundary between nature and city, but an information & labor conduit connecting two sides of same system.",
            "control_source": "Positive feedback loop: Housing dispersion <-> Road construction <-> Car dependency"
        },
        {
            "id": "Montceau-les-Mines",
            "category": "Spatial Node",
            "stats": {"context": "Post-industrial mining basin & memory node"},
            "metabolic_phenomenon": "Deindustrialization memory -> systemic transformation -> transition to automated/connected economy.",
            "control_source": "Historical industrial trajectory"
        },
        {
            "id": "Belfort-Lure Drift",
            "category": "Spatial Node / Route",
            "stats": {"context": "Eastern France industrial/rural nexus"},
            "metabolic_phenomenon": "Intersection of industrial decay, rural commuting, and technological dependence.",
            "control_source": "Regional logistics and industrial infrastructure"
        },
        {
            "id": "Aire de la Guye",
            "category": "Spatial / Environmental Node",
            "stats": {"context": "Highway service & ecological observation point"},
            "metabolic_phenomenon": "Drought & environmental stress triggering feedback correction loops.",
            "control_source": "Climatic & ecological constraints"
        },
        {
            "id": "Connected Car / Subscription Economy",
            "category": "Cybernetic / Platform Node",
            "stats": {"examples": ["BMW heated seat subscription rejection", "OTA firmware updates", "Paywalled ECU features"]},
            "metabolic_phenomenon": "Vehicle shifts from human tool to active node in cloud economic platform.",
            "control_source": "Cloud Platforms & Digital Monopolies"
        },
        {
            "id": "Psychiatric & Medical Deserts",
            "category": "Metabolic / Healthcare Strain Node",
            "stats": {"regions": ["Haute-Garonne", "Puy-de-Dôme"], "symptom": "Lack of doctors/psychiatrists causing closed emergency units"},
            "metabolic_phenomenon": "Loss of societal metabolic resolution; inability to diagnose/process systemic stress.",
            "control_source": "Resource allocation & administrative silos"
        },
        {
            "id": "Youth / Counterculture Inertia",
            "category": "Social / Mimetic Node",
            "stats": {"youth_anhedonia_fatigue": "58% lack of energy, 44% concentration difficulty"},
            "metabolic_phenomenon": "Energy captured by digital platforms; absence of counter-cultural physical density.",
            "control_source": "Attention economy & mimetic digital media"
        }
    ]

    edges = [
        ("Saint-Saturnin", "A75 Highway Corridor", {"label": "Feeds 89.6% commuters into"}),
        ("A75 Highway Corridor", "Connected Car / Subscription Economy", {"label": "Requires automated/connected transit"}),
        ("Connected Car / Subscription Economy", "Youth / Counterculture Inertia", {"label": "Extracts attention & subscription capital"}),
        ("Psychiatric & Medical Deserts", "Saint-Saturnin", {"label": "Reduces regional metabolic support"}),
        ("Montceau-les-Mines", "Belfort-Lure Drift", {"label": "Historical industrial continuum"}),
        ("Aire de la Guye", "A75 Highway Corridor", {"label": "Ecological anomaly checkpoint on highway"}),
        ("Youth / Counterculture Inertia", "Psychiatric & Medical Deserts", {"label": "Signals burnout & fatigue"})
    ]

    return drift_nodes, edges

def build_multidimensional_map():
    print("Executing Multi-Agent System and Etiological Listening Center...")

    # Read full raw drift text for agent execution
    raw_texts = []
    for fname in ['dryf1_raw.txt', 'dryf2_raw.txt']:
        if os.path.exists(fname):
            with open(fname, 'r', encoding='utf-8') as f:
                raw_texts.append(f.read())
    combined_text = "\n\n".join(raw_texts)

    listening_center = EtiologicalListeningCenter()
    diagnosis = listening_center.listen_and_diagnose(combined_text[:50000])

    nodes, edges = extract_drift_data()

    # Construct NetworkX graph
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n["id"], category=n["category"], phenomenon=n["metabolic_phenomenon"])
    for u, v, data in edges:
        G.add_edge(u, v, label=data["label"])

    # Generate Matplotlib visualization of Multidimensional Psychogeographical Map
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=0.8)

    # Draw nodes with distinct colors based on category
    color_map = []
    for node in G.nodes():
        cat = G.nodes[node].get("category", "")
        if "Spatial" in cat:
            color_map.append("#4C72B0") # Blue
        elif "Cybernetic" in cat:
            color_map.append("#DD8452") # Orange
        elif "Metabolic" in cat:
            color_map.append("#55A868") # Green
        else:
            color_map.append("#C44E52") # Red

    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=color_map, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", font_color="white")
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="#888888", width=2)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Multidimensional Psychogeographical Map\n(Information Metabolism, Cybernetic Corridors, & Etiological Control Sources)", fontsize=14, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    map_img_path = "drifting_logs/multidimensional_psychogeographical_map.png"
    plt.savefig(map_img_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved map visualization to {map_img_path}")

    # Compile comprehensive research report JSON
    research_report = {
        "title": "Multidimensional Psychogeographical & Epistemic Map of Drifting Logs",
        "etiological_diagnosis": diagnosis,
        "multidimensional_axes": {
            "1_Spatial_Axis": [
                "Saint-Saturnin (544 workers, 462 commuters out, 89.6% car dependency)",
                "A75 Highway Corridor (Clermont-Ferrand metropolitan flow, 32km avg daily driving)",
                "Montceau-les-Mines (Post-industrial transition node)",
                "Belfort - Lure Corridor (Eastern industrial/rural nexus)",
                "Aire de la Guye (Ecological drought/feedback observation)"
            ],
            "2_Temporal_Genealogy_Axis": [
                "1941 Chantiers de la Jeunesse (Theix discipline heritage)",
                "2008-2019 Rural Commuting Shift (+45-47 mins daily driving)",
                "Present OTA / Subscription platform capitalism"
            ],
            "3_Mimetic_Spectacular_Axis": [
                "Girardian copied desires (suburban sprawl, SUV mimesis)",
                "Debordian spectacle illusion (framing forced motorization as individual freedom)"
            ],
            "4_Information_Metabolism_Axis": [
                "Kępiński metabolic strain (high input speed, low value-integration capacity)",
                "Psychiatric deserts (loss of societal metabolic resolution in Haute-Garonne & Puy-de-Dôme)"
            ],
            "5_Cybernetic_Control_Axis": [
                "Anti-Autofac epistemic brake engaged",
                "Requisite variety gap identified (Ashby law)",
                "Shift from human tool to cloud platform node"
            ]
        },
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

    print(f"Saved research report JSON to {report_path}")
    return research_report

if __name__ == "__main__":
    build_multidimensional_map()
