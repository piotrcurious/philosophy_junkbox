#!/usr/bin/env python3
"""
epistemic_agents.py - Extended Multi-model Epistemic Agents with Semantic Reorganization
and Constraint-Based Filtering.
"""

import json
import re
from typing import Dict, List, Any, Optional

class LLMInterface:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def generate_analysis(self, prompt: str, perspective: str, text_context: str) -> Dict[str, Any]:
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
            return {"perspective": perspective, "insights": ["Generic epistemic observation."]}

    def reorganize_semantics(self, query: str, drift_nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Interactively reorganizes nodes and semantic relationships based on user/LLM query.
        """
        query_lower = query.lower()
        clusters = {}
        for node in drift_nodes:
            n_id = node.get("id", "")
            cat = node.get("category", "")
            if any(k in query_lower for k in ["car", "highway", "commute", "a75", "spatial"]):
                cluster = "Automotive Corridor & Commuting Entrapment" if "Spatial" in cat else "Cloud Platform Control"
            elif any(k in query_lower for k in ["health", "psychiat", "doctor", "strain", "metabol"]):
                cluster = "Information Metabolism & Healthcare Deficit"
            else:
                cluster = "General Psychogeographical Dynamics"

            if cluster not in clusters:
                clusters[cluster] = []
            clusters[cluster].append(n_id)

        return {
            "query_applied": query,
            "reorganized_clusters": clusters,
            "epistemic_insight": f"Re-clustered {len(drift_nodes)} nodes under query criteria '{query}'. Highlighted second-order feedback linkages."
        }

    def _analyze_kepinski(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Kępiński Information Metabolism",
            "metabolic_state": "High entropy / Overload without value-integration capacity",
            "information_input_rate": "High",
            "value_hierarchy_status": "Fragmented under informational pressure",
            "key_signals": ["Automotive mobility as externalized information metabolism"],
            "diagnostic": "The system receives massive data inputs but lacks shared value-metabolism channels to convert signals into goal revision."
        }

    def _analyze_ashby(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Ashby Requisite Variety",
            "environmental_variety": "Extremely High (unpredictable spatial dynamics, supply chain, weather)",
            "regulator_variety": "Low / Monolithic (single-dimensional optimization: speed, throughput)",
            "requisite_variety_gap": "Critical gap: Regulator cannot control system without inflating local noise",
            "feedback_loops": ["Closed positive feedback loop: housing dispersion -> road construction -> car dependency"],
            "recommendation": "Increase meta-regulator variety; introduce epistemic brakes to interrupt closed feedback loops."
        }

    def _analyze_girard(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Girardian Mimetic Desire",
            "triangular_model_sources": ["Marketing/Advertising", "Algorithmic recommendation", "Peer mimesis"],
            "copied_desires": ["SUV ownership", "Suburban house far from work", "Subscription-based autonomy"],
            "mimetic_conflict_points": ["Resource competition on highways (A75)", "Healthcare access bottlenecks"],
            "landscape_effect": "Landscape becomes physical embodiment of copied desires."
        }

    def _analyze_debord(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Debordian Spectacle & Genealogy",
            "spectacle_illusions": [
                "Infrastructure presented as 'natural necessity'",
                "Car dependency framed as individual freedom/choice"
            ],
            "uncovered_genealogy": [
                "Saint-Saturnin / A75 separation of residence and production",
                "Historical urban planning choices favoring highway corridors over rail"
            ],
            "alienation_type": "Maximization of micro-decisions while minimizing macro-control over life direction."
        }

    def _analyze_cybernetics(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Cybernetic Infrastructure & Connected Systems",
            "nodes_identified": ["Vehicle ECU / OTA", "A75 Corridor", "Paywalled feature subscriptions"],
            "control_sources": ["Cloud platform providers", "OEM feature lock-in"],
            "system_shift": "Shift from vehicle as user tool to vehicle as active node in cloud economic platform."
        }

    def _analyze_anomalies(self, text: str) -> Dict[str, Any]:
        return {
            "model_name": "Anomaly & Counter-Model Collector",
            "anomalies_detected": [
                "89.6% car commuting in Saint-Saturnin despite proximity to nature",
                "BMW seat heating subscription rejected by users as anomalous monetization"
            ],
            "counter_examples": ["Local mobility demand contradicting current highway routing"],
            "rule": "Do not synthesize prematurely. Hold anomalies open until model adapts."
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
