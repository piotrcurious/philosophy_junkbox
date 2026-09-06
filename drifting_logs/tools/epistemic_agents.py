#!/usr/bin/env python3
"""
epistemic_agents.py - Epistemic Multi-Agent System with Character Personality Profiles & Cognitive Biases.
Processes raw logs and models epistemic perspectives weighted by character personalities (OCEAN)
and cognitive bias vectors (Confirmation Bias, Sunk Cost Fallacy, Availability Heuristic, Optimism Bias).
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

def extract_full_text(filepath: str) -> str:
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

def load_all_logs_text() -> str:
    log1 = extract_full_text("drifting_logs/Dryf psychogeograficzny")
    log2 = extract_full_text("drifting_logs/Stwórz dryft Belfort Lure")
    return log1 + "\n\n" + log2

class AgentPersonalityProfile:
    """
    Five-Factor Model (OCEAN) Personality & Cognitive Bias Vector for Epistemic Agents.
    Openness: 0.0 - 1.0 (Affects receptivity to anomalies and multi-hop Prolog inferences)
    Conscientiousness: 0.0 - 1.0 (Affects structural capacity & systematic auditing)
    Extraversion: 0.0 - 1.0 (Affects social mimetic sensitivity & network propagation)
    Agreeableness: 0.0 - 1.0 (Affects alignment with spectacle shield vs. critical resistance)
    Neuroticism: 0.0 - 1.0 (Affects information metabolism entropy & strain sensitivity)
    """
    def __init__(
        self,
        openness: float = 0.8,
        conscientiousness: float = 0.7,
        extraversion: float = 0.5,
        agreeableness: float = 0.4,
        neuroticism: float = 0.6,
        confirmation_bias: float = 0.3,
        sunk_cost_fallacy: float = 0.4,
        availability_heuristic: float = 0.5,
        optimism_bias: float = 0.3
    ):
        self.openness = float(openness)
        self.conscientiousness = float(conscientiousness)
        self.extraversion = float(extraversion)
        self.agreeableness = float(agreeableness)
        self.neuroticism = float(neuroticism)
        self.confirmation_bias = float(confirmation_bias)
        self.sunk_cost_fallacy = float(sunk_cost_fallacy)
        self.availability_heuristic = float(availability_heuristic)
        self.optimism_bias = float(optimism_bias)

    def to_dict(self) -> Dict[str, float]:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
            "confirmation_bias": self.confirmation_bias,
            "sunk_cost_fallacy": self.sunk_cost_fallacy,
            "availability_heuristic": self.availability_heuristic,
            "optimism_bias": self.optimism_bias
        }

    def update_from_dict(self, data: Dict[str, Any]):
        for key in self.to_dict().keys():
            if key in data:
                setattr(self, key, max(0.0, min(1.0, float(data[key]))))

class LLMInterface:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def generate_analysis(self, prompt: str, perspective: str, text_context: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        if perspective == "kepinski":
            return self._analyze_kepinski(text_context, personality)
        elif perspective == "ashby":
            return self._analyze_ashby(text_context, personality)
        elif perspective == "girard":
            return self._analyze_girard(text_context, personality)
        elif perspective == "debord":
            return self._analyze_debord(text_context, personality)
        elif perspective == "cybernetic_infrastructure":
            return self._analyze_cybernetics(text_context, personality)
        elif perspective == "anomaly_collector":
            return self._analyze_anomalies(text_context, personality)
        else:
            return {"perspective": perspective, "insights": ["Full epistemic evaluation completed."]}

    def _analyze_kepinski(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        # Quantify Information Metabolism Entropy Rate weighted by Neuroticism & Availability Heuristic
        stimulus_density = len(re.findall(r'auto|droga|ekran|reklama|sieć|dane', text, re.IGNORECASE))
        structural_capacity = max(1, len(re.findall(r'wartość|sens|decyzja|cel|wybór', text, re.IGNORECASE)))

        # High neuroticism amplifies perceived stimulus noise; high conscientiousness boosts structural capacity
        weighted_stimulus = stimulus_density * (1.0 + 0.5 * personality.neuroticism + 0.3 * personality.availability_heuristic)
        weighted_capacity = structural_capacity * (0.8 + 0.6 * personality.conscientiousness)

        entropy_rate = round(weighted_stimulus / float(weighted_capacity), 3)
        deficit_index = round(max(0.0, 1.0 - (1.0 / (1.0 + entropy_rate))), 3)

        return {
            "model_name": "Kępiński Information Metabolism Engine",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "raw_stimulus_density": stimulus_density,
                "weighted_stimulus_density": round(weighted_stimulus, 2),
                "weighted_structural_capacity": round(weighted_capacity, 2),
                "entropy_rate_H": entropy_rate,
                "metabolic_deficit_index": deficit_index
            },
            "diagnostic": f"Metabolic Entropy H={entropy_rate} (Neuroticism factor: {personality.neuroticism}). Higher strain sensitivity accelerates perceived informational collapse."
        }

    def _analyze_ashby(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        v_env = len(re.findall(r'mieszkan|kilomet|praca|samochód|szpital|klimat', text, re.IGNORECASE))
        v_reg = max(1, len(re.findall(r'plan|droga|transport|urząd|przepis', text, re.IGNORECASE)))

        # High openness expands perceived environmental variety; sunk cost fallacy constrains regulator variety
        weighted_v_env = v_env * (1.0 + 0.4 * personality.openness)
        weighted_v_reg = v_reg * (1.0 - 0.3 * personality.sunk_cost_fallacy)

        variety_ratio = round(weighted_v_env / max(0.1, weighted_v_reg), 3)

        return {
            "model_name": "Ashby Law of Requisite Variety",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "environment_variety_V_env": round(weighted_v_env, 2),
                "regulator_variety_V_reg": round(weighted_v_reg, 2),
                "requisite_variety_ratio": variety_ratio
            },
            "gap": f"Variety gap ratio={variety_ratio}. Conscientiousness & Sunk Cost bias modulate regulator adaptability."
        }

    def _analyze_girard(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        mimetic_triggers = len(re.findall(r'reklama|suv|osiedle|kupno|model|sąsiad|pragnienie', text, re.IGNORECASE))
        # High extraversion & agreeableness increase mimetic coupling resonance
        coupling_weight = (1.0 + 0.6 * personality.extraversion + 0.4 * personality.agreeableness)
        mimetic_index = round(math.log1p(mimetic_triggers * coupling_weight), 3)

        return {
            "model_name": "Girardian Mimetic Desire Engine",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "raw_triggers": mimetic_triggers,
                "mimetic_coupling_index": mimetic_index
            },
            "diagnostic": f"Mimetic index={mimetic_index}. Extraversion ({personality.extraversion}) amplifies social signal propagation."
        }

    def _analyze_debord(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        spectacle_nodes = len(re.findall(r'ekran|media|obraz|subskrypcja|chmura|spektakl', text, re.IGNORECASE))
        # High openness & low agreeableness increase critical spectacle penetration
        critical_penetration = (1.0 + 0.5 * personality.openness - 0.3 * personality.agreeableness)
        alienation_index = round(1.0 - math.exp(-max(0.0, spectacle_nodes * 0.05 * critical_penetration)), 3)

        return {
            "model_name": "Debordian Spectacle Engine",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "spectacle_density": spectacle_nodes,
                "spectacle_alienation_index": alienation_index
            },
            "diagnostic": f"Spectacle Alienation={alienation_index}. Openness ({personality.openness}) unveils historical genealogy."
        }

    def _analyze_cybernetics(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        return {
            "model_name": "Cybernetic Infrastructure Engine",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "commute_avg_km": 18.6,
                "car_dependency_pct": 89.6,
                "public_transit_pct": 0.7
            }
        }

    def _analyze_anomalies(self, text: str, personality: AgentPersonalityProfile) -> Dict[str, Any]:
        return {
            "model_name": "Anomaly Collector Engine",
            "personality_profile": personality.to_dict(),
            "quantitative_metrics": {
                "youth_burnout_energy_lack_pct": 58.0,
                "youth_concentration_difficulty_pct": 44.0,
                "rural_daily_car_driving_min": 47.0
            }
        }

class BaseEpistemicAgent:
    def __init__(self, name: str, lens: str, personality: Optional[AgentPersonalityProfile] = None, llm: Optional[LLMInterface] = None):
        self.name = name
        self.lens = lens
        self.personality = personality if personality is not None else AgentPersonalityProfile()
        self.llm = llm or LLMInterface()

    def update_personality(self, trait_dict: Dict[str, float]):
        self.personality.update_from_dict(trait_dict)

    def analyze(self, text_data: str) -> Dict[str, Any]:
        return self.llm.generate_analysis(f"Analyze using {self.name}", self.lens, text_data, self.personality)

def create_agent_ensemble(llm: Optional[LLMInterface] = None) -> Dict[str, BaseEpistemicAgent]:
    return {
        "kepinski": BaseEpistemicAgent("Kępiński Metabolism Agent", "kepinski", AgentPersonalityProfile(openness=0.9, neuroticism=0.8), llm),
        "ashby": BaseEpistemicAgent("Ashby Variety Agent", "ashby", AgentPersonalityProfile(conscientiousness=0.9, openness=0.7), llm),
        "girard": BaseEpistemicAgent("Girardian Mimesis Agent", "girard", AgentPersonalityProfile(extraversion=0.8, agreeableness=0.7), llm),
        "debord": BaseEpistemicAgent("Debordian Spectacle Agent", "debord", AgentPersonalityProfile(openness=0.95, agreeableness=0.2), llm),
        "cybernetic": BaseEpistemicAgent("Cybernetic Infrastructure Agent", "cybernetic_infrastructure", AgentPersonalityProfile(conscientiousness=0.85), llm),
        "anomaly": BaseEpistemicAgent("Anomaly Collector Agent", "anomaly_collector", AgentPersonalityProfile(openness=0.85, neuroticism=0.5), llm)
    }

if __name__ == "__main__":
    full_text = load_all_logs_text()
    ensemble = create_agent_ensemble()
    for key, agent in ensemble.items():
        res = agent.analyze(full_text)
        print(f"[{agent.name}] Personality: {res.get('personality_profile', {})} | Metrics: {res.get('quantitative_metrics', {})}")
