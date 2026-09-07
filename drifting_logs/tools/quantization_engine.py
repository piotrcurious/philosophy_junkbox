"""
Quantization & Granulation Engine for Psychogeographical Systems
Implements the paradigm shift described in paradigm_fixes/quantization.md:
1. Level I: Spatial Granulation (V = {C_1, ..., C_N}) with scale dependency Δx and aggregation conflict loss
2. Level II: Parameter Quantization (z -> Q_1(z)) with discrete cost/value classes
3. Level III: Relational Quantization ((c_ij, a_i, a_j) -> Q_2 -> R_ij) with discrete relation algebra R
4. Level IV: Decision Quantization (U_ij -> Q_3 -> D_ij) with discrete automata, hysteresis, and threshold jumps
5. Emergent Psychogeographical Fields Ψ_i and Phase Boundaries (R_ij = R_c + ε)
"""

import math
import numpy as np
from enum import Enum
from typing import Dict, List, Any, Tuple, Optional


class RelationType(Enum):
    STRONGLY_ATTRACTIVE = 2
    ATTRACTIVE = 1
    NEUTRAL = 0
    REPULSIVE = -1
    BARRIER = -2


class ParameterQuantizer:
    """
    Level II: Parameter Quantization Q_1(z)
    Maps continuous parameters (cost, distance, noise, risk, GDP) into discrete cost/value classes.
    """
    def __init__(self, thresholds: Optional[List[float]] = None):
        # Default cost thresholds: <1 -> 0, [1, 3) -> 1, [3, 7) -> 2, [7, 15) -> 3, >=15 -> 4
        self.thresholds = thresholds if thresholds is not None else [1.0, 3.0, 7.0, 15.0]

    def quantize(self, val: float) -> int:
        for idx, t in enumerate(self.thresholds):
            if val < t:
                return idx
        return len(self.thresholds)

    def quantized_pair_probability(self, cost: float, beta: float = 1.0) -> float:
        """
        p_ij ∝ e^(-β * Q_1(c_ij))
        Demonstrates that small physical changes across boundaries cause sharp jumps,
        while changes within a class produce identical probability.
        """
        q_cost = self.quantize(cost)
        return float(np.exp(-beta * q_cost))


class SpatialGrain:
    """
    Level I: Spatial Grain C_i representing a spatial cell/zone at scale Δx.
    """
    def __init__(self, grain_id: str, center_coords: Tuple[float, float, float],
                 scale_dx: float = 1.0, internal_conflict: float = 0.0,
                 sub_grains: Optional[List[str]] = None, domain_data: Optional[Dict[str, Any]] = None):
        self.grain_id = grain_id
        self.center_coords = center_coords
        self.scale_dx = scale_dx
        self.internal_conflict = internal_conflict
        self.sub_grains = sub_grains if sub_grains is not None else [grain_id]
        self.domain_data = domain_data if domain_data is not None else {}


class SpatialGranulationEngine:
    """
    Manages spatial grains, multi-scale aggregation C = C_1 ∪ C_2,
    internal conflict destruction tracking under aggregation, and critical scale Δx* analysis.
    """
    def __init__(self, grains: Optional[List[SpatialGrain]] = None):
        self.grains = {g.grain_id: g for g in grains} if grains else {}

    def add_grain(self, grain: SpatialGrain):
        self.grains[grain.grain_id] = grain

    def aggregate_grains(self, new_grain_id: str, grain_ids: List[str],
                         relations_map: Dict[Tuple[str, str], float]) -> SpatialGrain:
        """
        Aggregates sub-grains C = C_1 ∪ C_2 ... ∪ C_k.
        Calculates loss of internal conflict information under aggregation:
        If sub-grain C_1 has positive relation (+) and sub-grain C_2 has negative relation (-),
        their aggregation produces a neutral average R(C) ≈ 0, destroying internal conflict.
        """
        valid_grains = [self.grains[gid] for gid in grain_ids if gid in self.grains]
        if not valid_grains:
            raise ValueError("No valid sub-grains provided for aggregation")

        # Average center coordinates
        coords = np.mean([g.center_coords for g in valid_grains], axis=0)
        scale_dx = sum(g.scale_dx for g in valid_grains)

        # Internal conflict metric: sum of variances in internal pair relations
        internal_pair_vals = []
        for i, g1 in enumerate(valid_grains):
            for j, g2 in enumerate(valid_grains):
                if i < j:
                    r_val = relations_map.get((g1.grain_id, g2.grain_id), 0.0)
                    internal_pair_vals.append(r_val)

        if internal_pair_vals:
            # High variance of opposing +/- signs indicates high internal conflict destroyed by aggregation
            pos_count = sum(1 for v in internal_pair_vals if v > 0)
            neg_count = sum(1 for v in internal_pair_vals if v < 0)
            conflict = float(np.std(internal_pair_vals) * (1.0 + min(pos_count, neg_count)))
        else:
            conflict = 0.0

        sub_list = []
        for g in valid_grains:
            sub_list.extend(g.sub_grains)

        aggregated = SpatialGrain(
            grain_id=new_grain_id,
            center_coords=(float(coords[0]), float(coords[1]), float(coords[2])),
            scale_dx=scale_dx,
            internal_conflict=conflict,
            sub_grains=sub_list
        )
        self.grains[new_grain_id] = aggregated
        return aggregated

    def analyze_critical_scale(self, scale_steps: List[float],
                                raw_edges: List[Tuple[str, str, float]]) -> Dict[str, Any]:
        """
        Evaluates system dynamics across scale steps Δx to find critical scale Δx*
        where information density / conflict visibility is maximized.
        """
        scale_results = []
        best_scale = scale_steps[0] if scale_steps else 1.0
        max_conflict_visibility = -1.0

        for dx in scale_steps:
            # Group nodes within distance dx
            conflict_sum = 0.0
            group_count = 0
            for u, v, weight in raw_edges:
                if weight < dx:
                    conflict_sum += abs(weight - (dx / 2.0))
                    group_count += 1

            conflict_visibility = conflict_sum / max(1, group_count)
            scale_results.append({
                "scale_dx": dx,
                "conflict_visibility": round(float(conflict_visibility), 4),
                "active_groups": group_count
            })

            if conflict_visibility > max_conflict_visibility:
                max_conflict_visibility = conflict_visibility
                best_scale = dx

        return {
            "critical_scale_dx_star": best_scale,
            "max_conflict_visibility": round(float(max_conflict_visibility), 4),
            "scale_curve": scale_results
        }


class RelationalQuantizer:
    """
    Level III: Relational Quantization (c_ij, a_i, a_j, ...) -> Q_2 -> R_ij
    Maps pair metrics into discrete relation algebra R_ij ∈ {STRONGLY_ATTRACTIVE, ATTRACTIVE, NEUTRAL, REPULSIVE, BARRIER}.
    """
    def __init__(self, param_quantizer: Optional[ParameterQuantizer] = None):
        self.param_quantizer = param_quantizer if param_quantizer is not None else ParameterQuantizer()

    def classify_relation(self, raw_cost: float, attraction_bias: float = 0.0) -> RelationType:
        q_c = self.param_quantizer.quantize(raw_cost)
        effective_score = attraction_bias - q_c

        if effective_score >= 1.5:
            return RelationType.STRONGLY_ATTRACTIVE
        elif effective_score >= 0.5:
            return RelationType.ATTRACTIVE
        elif effective_score >= -0.5:
            return RelationType.NEUTRAL
        elif effective_score >= -1.5:
            return RelationType.REPULSIVE
        else:
            return RelationType.BARRIER

    def compute_quantized_edge_relation(self, src_state: Dict[str, Any], tgt_state: Dict[str, Any],
                                        base_cost: float) -> Dict[str, Any]:
        """
        Converts continuous pair parameters into quantized relation type R_ij and probability.
        """
        src_attr = src_state.get("attraction", 1.0)
        tgt_attr = tgt_state.get("attraction", 1.0)
        net_bias = (src_attr + tgt_attr) / 2.0

        rel_type = self.classify_relation(base_cost, net_bias)
        q_cost = self.param_quantizer.quantize(base_cost)
        prob = self.param_quantizer.quantized_pair_probability(base_cost)

        return {
            "raw_cost": base_cost,
            "quantized_cost_class": q_cost,
            "relation_type": rel_type.name,
            "relation_numeric": rel_type.value,
            "quantized_probability": round(prob, 4)
        }


class DecisionQuantizer:
    """
    Level IV: Decision Quantization U_ij -> Q_3 -> D_ij ∈ {0, 1, ..., K}
    Models discrete behavioral choices, hysteresis loops, threshold jumps,
    and discrete iterative dynamics x_{t+1} = Q_3(F(x_t)).
    """
    def __init__(self, threshold_c: float = 2.0, hysteresis_margin: float = 0.5):
        self.threshold_c = threshold_c
        self.hysteresis_margin = hysteresis_margin

    def quantize_decision(self, utility: float, previous_decision: int = 0) -> int:
        """
        Decides transition class D_ij ∈ {0: No Transition, 1: Local Transition, 2: Highway Transit, 3: Category Jump}
        incorporating hysteresis to avoid rapid state flickering around critical thresholds.
        """
        if previous_decision == 0:
            # Needs to cross upper threshold to switch to state 1
            if utility > (self.threshold_c + self.hysteresis_margin):
                return 1
            return 0
        elif previous_decision == 1:
            # Switches back to 0 only if falling below lower threshold
            if utility < (self.threshold_c - self.hysteresis_margin):
                return 0
            elif utility > (self.threshold_c + 2.0 * self.hysteresis_margin):
                return 2
            return 1
        elif previous_decision == 2:
            if utility < (self.threshold_c + self.hysteresis_margin):
                return 1
            elif utility > (self.threshold_c + 4.0 * self.hysteresis_margin):
                return 3
            return 2
        else: # previous_decision == 3
            if utility < (self.threshold_c + 3.0 * self.hysteresis_margin):
                return 2
            return 3

    def run_iterative_decision_trajectory(self, initial_x: float, iterations: int = 5,
                                           func=None) -> List[Dict[str, Any]]:
        """
        Simulates x_{t+1} = Q_3(F(x_t)) demonstrating trajectory divergence,
        metastability, and hysteresis from quantized decision steps.
        """
        if func is None:
            func = lambda x: 1.2 * x + 0.5

        trajectory = []
        curr_x = initial_x
        curr_d = 0

        for t in range(iterations):
            u = func(curr_x)
            next_d = self.quantize_decision(u, previous_decision=curr_d)
            trajectory.append({
                "step": t,
                "x_t": round(float(curr_x), 4),
                "utility": round(float(u), 4),
                "decision_D": next_d,
                "jump_occurred": next_d != curr_d
            })
            curr_x = float(next_d * 2.5 + u * 0.2)
            curr_d = next_d

        return trajectory


class QuantizedPsychogeographicalPipeline:
    """
    Full 4-Level Quantized Pipeline for G = (V, E, Q, R, D)
    Continuous Space -> Granulation -> Graph -> Pair Functions -> Relational Quantization -> Flows -> Decision Quantization -> Emergent Fields
    """
    def __init__(self, threshold_c: float = 2.0):
        self.param_quantizer = ParameterQuantizer()
        self.granulation_engine = SpatialGranulationEngine()
        self.relational_quantizer = RelationalQuantizer(self.param_quantizer)
        self.decision_quantizer = DecisionQuantizer(threshold_c=threshold_c)

    def process_pipeline(self, raw_nodes: List[Dict[str, Any]],
                         raw_edges: List[Tuple[str, str, float]]) -> Dict[str, Any]:
        """
        Executes complete multi-layer quantization pipeline and returns emergent psychogeographical fields.
        """
        # Level I: Granulate Space
        grains = []
        for idx, n in enumerate(raw_nodes):
            gid = n["id"]
            pos = n.get("pos", [0.0, 0.0, 0.0])
            grain = SpatialGrain(
                grain_id=gid,
                center_coords=(pos[0], pos[1], pos[2]),
                scale_dx=1.0,
                domain_data={"category": n.get("category", ""), "stats": n.get("stats", "")}
            )
            self.granulation_engine.add_grain(grain)
            grains.append(grain)

        # Level II & III: Parameter & Relational Quantization
        quantized_edges = []
        psychogeographical_boundaries = []

        for u, v, raw_cost in raw_edges:
            src_state = {"attraction": 1.5 if "Saint" in u or "A75" in u else 0.8}
            tgt_state = {"attraction": 1.2 if "Car" in v or "Desert" in v else 0.9}

            rel_info = self.relational_quantizer.compute_quantized_edge_relation(src_state, tgt_state, raw_cost)

            # Level IV: Decision Quantization
            utility = 3.0 - rel_info["quantized_cost_class"] + rel_info["relation_numeric"]
            decision_val = self.decision_quantizer.quantize_decision(utility)

            edge_record = {
                "source": u,
                "target": v,
                "raw_cost": raw_cost,
                "quantized_cost_class": rel_info["quantized_cost_class"],
                "relation_type": rel_info["relation_type"],
                "relation_numeric": rel_info["relation_numeric"],
                "quantized_probability": rel_info["quantized_probability"],
                "decision_choice_D": decision_val
            }
            quantized_edges.append(edge_record)

            # Detect psychogeographical phase boundary (R_ij ≈ R_c boundary crossing)
            if rel_info["relation_numeric"] == 0 or rel_info["relation_type"] == "NEUTRAL":
                psychogeographical_boundaries.append({
                    "source": u,
                    "target": v,
                    "critical_threshold_R_c": rel_info["raw_cost"],
                    "description": f"Psychogeographical phase boundary between {u} and {v}"
                })

        # Calculate Emergent Psychogeographical Field Ψ_i for each node
        emergent_fields = {}
        for g in grains:
            gid = g.grain_id
            incident_relations = [
                e["relation_numeric"] for e in quantized_edges if e["source"] == gid or e["target"] == gid
            ]
            avg_rel = np.mean(incident_relations) if incident_relations else 0.0
            psi_i = round(float(avg_rel * 1.5 + g.scale_dx * 0.5), 4)
            emergent_fields[gid] = {
                "Psi_emergent_field": psi_i,
                "incident_edge_count": len(incident_relations),
                "avg_quantized_relation": round(float(avg_rel), 4)
            }

        # Scale Dependency Analysis
        scale_analysis = self.granulation_engine.analyze_critical_scale(
            scale_steps=[1.0, 5.0, 10.0, 15.0, 20.0],
            raw_edges=raw_edges
        )

        return {
            "spatial_grains_count": len(grains),
            "quantized_edges": quantized_edges,
            "psychogeographical_boundaries": psychogeographical_boundaries,
            "emergent_psychogeographical_fields": emergent_fields,
            "scale_dependency_analysis": scale_analysis
        }


if __name__ == "__main__":
    param_q = ParameterQuantizer()
    print("Cost 2.99 -> Class:", param_q.quantize(2.99), "Prob:", param_q.quantized_pair_probability(2.99))
    print("Cost 3.01 -> Class:", param_q.quantize(3.01), "Prob:", param_q.quantized_pair_probability(3.01))
    print("Cost 6.99 -> Class:", param_q.quantize(6.99), "Prob:", param_q.quantized_pair_probability(6.99))

    pipeline = QuantizedPsychogeographicalPipeline()
    sample_nodes = [{"id": "A", "pos": [0, 0, 0]}, {"id": "B", "pos": [10, 0, 0]}]
    sample_edges = [("A", "B", 2.99), ("A", "B", 3.01)]
    res = pipeline.process_pipeline(sample_nodes, sample_edges)
    print("Sample Pipeline Result Boundaries:", len(res["psychogeographical_boundaries"]))
