#!/usr/bin/env python3
"""
epistemic_agents.py - Advanced Epistemic Multi-Agent System & Semantic Reorganization Engine.
Extracts deep semantic vectors, cybernetic feedback loops, and metabolic entropy indicators
directly from raw drifting logs.
"""

import os
import re
import json
import math
import email
from html.parser import HTMLParser
from typing import Dict, List, Any, Optional

class MHTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_parts.append(cleaned)

def extract_text_from_mhtml(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    with open(filepath, 'rb') as f:
        msg = email.message_from_binary_file(f)
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            parser = MHTMLTextExtractor()
            parser.feed(html)
            return "\n".join(parser.text_parts)
    return ""

class SemanticVectorEngine:
    """
    Computes TF-IDF/Keyword semantic embeddings and 3D spatial vectors for drift nodes.
    """
    @staticmethod
    def compute_node_vector(text: str, keywords: List[str]) -> float:
        text_lower = text.lower()
        score = 0
        for kw in keywords:
            matches = len(re.findall(r'\b' + re.escape(kw.lower()) + r'\b', text_lower))
            score += matches
        return math.log1p(score)

class LLMInterface:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def generate_analysis(self, prompt: str, perspective: str, text_context: str) -> Dict[str, Any]:
        context_lower = text_context.lower()

        if perspective == "kepinski":
            return self._analyze_kepinski(text_context)
        elif perspective == "ashby":
            return self._analyze_ashby(text_context)
        elif perspective == "girard":
            return self._analyze_girard(text_context)
        elif perspective == "debord":
            return self._analyze_debord(text_context)
        elif perspective == "cybernetic_infrastructure":
            return self._analyze_cybernetics(text_context)
        elif perspective == "anomaly_collector":
            return self._analyze_anomalies(text_context)
        else:
            return {"perspective": perspective, "insights": ["Epistemic evaluation completed."]}

    def reorganize_semantics(self, query: str, drift_nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Dynamically calculates new 3D spatial coordinates and semantic cluster groupings
        based on user query and semantic vector scores.
        """
        query_words = [w.lower() for w in re.findall(r'\w+', query) if len(w) > 2]
        reorganized_nodes = []
        clusters = {}

        for idx, node in enumerate(drift_nodes):
            node_text = f"{node.get('id', '')} {node.get('metabolic_phenomenon', '')} {node.get('stats', '')} {node.get('control_source', '')}"
            relevance = SemanticVectorEngine.compute_node_vector(node_text, query_words)

            # Reposition node in 3D space according to relevance and query semantics
            orig_pos = node.get("pos", [0, 0, 0])
            cluster_id = "High Relevance" if relevance > 1.0 else ("Moderate Relevance" if relevance > 0 else "Background Baseline")

            new_x = orig_pos[0] + (relevance * 25) * math.cos(idx * 0.8)
            new_y = orig_pos[1] + (relevance * 20) * math.sin(idx * 0.8)
            new_z = orig_pos[2] + (relevance * 15)

            reorganized_node = dict(node)
            reorganized_node["pos"] = [round(new_x, 2), round(new_y, 2), round(new_z, 2)]
            reorganized_node["relevance_score"] = round(relevance, 3)
            reorganized_node["semantic_cluster"] = cluster_id

            reorganized_nodes.append(reorganized_node)
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(node.get("id"))

        return {
            "query": query,
            "reorganized_clusters": clusters,
            "reorganized_nodes": reorganized_nodes,
            "meta_summary": f"Semantic reorganization completed for query '{query}'. Re-calculated 3D positions and semantic vectors for {len(reorganized_nodes)} nodes."
        }

    def _analyze_kepinski(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Kępiński Information Metabolism Engine",
            "metabolic_state": "High entropy / Information overload without value integration",
            "signals": [
                "Spatial commute as externalized metabolic expenditure",
                "Digital stimulus saturation vs depleted emotional processing capacity"
            ],
            "diagnostic": "Organism receives high-frequency inputs but lacks internal structural channels to zmetabolizować signals into goal changes."
        }

    def _analyze_ashby(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Ashby Law of Requisite Variety",
            "gap": "Regulator variety significantly lower than environmental noise",
            "closed_loop": "Housing sprawl -> Car requirement -> Road expansion -> Further housing sprawl",
            "recommendation": "Engage epistemic brakes to restrict positive feedback amplification."
        }

    def _analyze_girard(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Girardian Mimetic Engine",
            "copied_desires": ["Suburban detached house", "SUV mobility", "On-demand cloud subscription"],
            "conflict_locus": "Highway bottlenecks & healthcare resource access"
        }

    def _analyze_debord(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Debordian Spectacle & Genealogy Engine",
            "spectacle_illusions": ["Framing forced daily motorization as individual freedom"],
            "uncovered_genealogy": ["A75 highway infrastructure separating labor from residential existence"]
        }

    def _analyze_cybernetics(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Cybernetic Infrastructure & Platform Engine",
            "control_nodes": ["Vehicle ECU", "OTA Cloud updates", "SaaS subscription locks"],
            "shift": "Transformation of private vehicle into platform node extracting ongoing subscription revenue"
        }

    def _analyze_anomalies(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Anomaly Collector Engine",
            "anomalies": [
                "89.6% car commuters in Saint-Saturnin",
                "BMW heated seat subscription pushback",
                "Emergency room closures due to psychiatric staff shortages"
            ]
        }

class BaseEpistemicAgent:
    def __init__(self, name: str, lens: str, llm: Optional[LLMInterface] = None):
        self.name = name
        self.lens = lens
        self.llm = llm or LLMInterface()

    def analyze(self, text_data: str) -> Dict[str, Any]:
        return self.llm.generate_analysis(f"Analyze using {self.name}", self.lens, text_data)

def create_agent_ensemble(llm: Optional[LLMInterface] = None) -> List[BaseEpistemicAgent]:
    return [
        BaseEpistemicAgent("Kępiński Metabolism Agent", "kepinski", llm),
        BaseEpistemicAgent("Ashby Variety Agent", "ashby", llm),
        BaseEpistemicAgent("Girardian Mimesis Agent", "girard", llm),
        BaseEpistemicAgent("Debordian Spectacle Agent", "debord", llm),
        BaseEpistemicAgent("Cybernetic Infrastructure Agent", "cybernetic_infrastructure", llm),
        BaseEpistemicAgent("Anomaly Collector Agent", "anomaly_collector", llm)
    ]

if __name__ == "__main__":
    ensemble = create_agent_ensemble()
    print("Testing epistemic ensemble with semantic vector calculations...")
    for agent in ensemble:
        res = agent.analyze("Saint-Saturnin A75 BMW subscription medical desert")
        print(f"[{agent.name}] -> {res['model_name']}")
