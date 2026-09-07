"""
Unit tests for Quantization Paradigm in drifting_logs/tools/quantization_engine.py
Tests Level I Spatial Granulation, Level II Parameter Quantization, Level III Relational Quantization,
Level IV Decision Quantization with Hysteresis, 4-Level Pipeline, Prolog KB Integration, & Transformer Integration.
"""

import unittest
import numpy as np

from drifting_logs.tools.quantization_engine import (
    ParameterQuantizer, SpatialGrain, SpatialGranulationEngine,
    RelationalQuantizer, DecisionQuantizer, QuantizedPsychogeographicalPipeline,
    RelationType
)
from drifting_logs.tools.algebraic_model_transformer import AlgebraicModelTransformer
from drifting_logs.tools.prolog_engine import PrologAxiomProgram


class TestParameterQuantizer(unittest.TestCase):
    def setUp(self):
        self.quantizer = ParameterQuantizer(thresholds=[1.0, 3.0, 7.0, 15.0])

    def test_threshold_class_boundaries(self):
        # 2.99 and 3.01 cross class boundary (Class 1 vs Class 2)
        c1 = 2.99
        c2 = 3.01
        c3 = 6.99
        q1 = self.quantizer.quantize(c1)
        q2 = self.quantizer.quantize(c2)
        q3 = self.quantizer.quantize(c3)

        self.assertEqual(q1, 1)
        self.assertEqual(q2, 2)
        self.assertEqual(q3, 2)
        self.assertNotEqual(q1, q2)
        self.assertEqual(q2, q3)

    def test_quantized_pair_probabilities(self):
        prob_2_99 = self.quantizer.quantized_pair_probability(2.99)
        prob_3_01 = self.quantizer.quantized_pair_probability(3.01)
        prob_6_99 = self.quantizer.quantized_pair_probability(6.99)

        self.assertAlmostEqual(prob_3_01, prob_6_99)
        self.assertGreater(prob_2_99, prob_3_01)


class TestSpatialGranulation(unittest.TestCase):
    def setUp(self):
        self.engine = SpatialGranulationEngine()
        self.g1 = SpatialGrain("C1", (0.0, 0.0, 0.0), scale_dx=1.0)
        self.g2 = SpatialGrain("C2", (2.0, 0.0, 0.0), scale_dx=1.0)
        self.engine.add_grain(self.g1)
        self.engine.add_grain(self.g2)

    def test_aggregation_and_conflict_loss(self):
        # C1 has positive relation with C2 (+2.0) vs C3 (-2.0)
        g3 = SpatialGrain("C3", (4.0, 0.0, 0.0), scale_dx=1.0)
        self.engine.add_grain(g3)

        relations_map = {
            ("C1", "C2"): 2.0,
            ("C1", "C3"): -2.0,
            ("C2", "C3"): 0.0
        }

        aggregated = self.engine.aggregate_grains("C_aggregated", ["C1", "C2", "C3"], relations_map)
        self.assertEqual(aggregated.grain_id, "C_aggregated")
        self.assertGreater(aggregated.internal_conflict, 0.0)
        self.assertEqual(len(aggregated.sub_grains), 3)

    def test_critical_scale_analysis(self):
        raw_edges = [("A", "B", 2.0), ("B", "C", 8.0), ("A", "C", 14.0)]
        scale_res = self.engine.analyze_critical_scale([1.0, 5.0, 10.0, 15.0], raw_edges)

        self.assertIn("critical_scale_dx_star", scale_res)
        self.assertIn("scale_curve", scale_res)
        self.assertGreater(len(scale_res["scale_curve"]), 0)


class TestRelationalQuantizer(unittest.TestCase):
    def setUp(self):
        self.quantizer = RelationalQuantizer()

    def test_relation_classification_algebra(self):
        rel_strong = self.quantizer.classify_relation(raw_cost=0.5, attraction_bias=2.0)
        rel_neutral = self.quantizer.classify_relation(raw_cost=3.0, attraction_bias=2.0)
        rel_barrier = self.quantizer.classify_relation(raw_cost=16.0, attraction_bias=0.0)

        self.assertEqual(rel_strong, RelationType.STRONGLY_ATTRACTIVE)
        self.assertEqual(rel_neutral, RelationType.NEUTRAL)
        self.assertEqual(rel_barrier, RelationType.BARRIER)


class TestDecisionQuantizer(unittest.TestCase):
    def setUp(self):
        self.quantizer = DecisionQuantizer(threshold_c=2.0, hysteresis_margin=0.5)

    def test_hysteresis_dynamics(self):
        # Switching from state 0 -> state 1 requires utility > threshold + margin (2.5)
        d_sub = self.quantizer.quantize_decision(utility=2.2, previous_decision=0)
        d_above = self.quantizer.quantize_decision(utility=2.6, previous_decision=0)
        self.assertEqual(d_sub, 0)
        self.assertEqual(d_above, 1)

        # Staying in state 1 when utility drops slightly below upper threshold (e.g. 2.1)
        d_stay = self.quantizer.quantize_decision(utility=2.1, previous_decision=1)
        d_drop = self.quantizer.quantize_decision(utility=1.4, previous_decision=1)
        self.assertEqual(d_stay, 1) # Hysteresis holds state 1
        self.assertEqual(d_drop, 0) # Below lower threshold (1.5) switches back to 0

    def test_iterative_decision_trajectory(self):
        traj = self.quantizer.run_iterative_decision_trajectory(initial_x=1.0, iterations=5)
        self.assertEqual(len(traj), 5)
        for step_info in traj:
            self.assertIn("decision_D", step_info)
            self.assertIn("jump_occurred", step_info)


class TestPipelineAndIntegration(unittest.TestCase):
    def test_4level_pipeline(self):
        pipeline = QuantizedPsychogeographicalPipeline()
        sample_nodes = [{"id": "NodeA", "pos": [0, 0, 0]}, {"id": "NodeB", "pos": [10, 0, 0]}]
        sample_edges = [("NodeA", "NodeB", 3.0)]

        res = pipeline.process_pipeline(sample_nodes, sample_edges)
        self.assertEqual(res["spatial_grains_count"], 2)
        self.assertIn("quantized_edges", res)
        self.assertIn("emergent_psychogeographical_fields", res)

    def test_transformer_integration(self):
        transformer = AlgebraicModelTransformer()
        model_output = transformer.transform_model()

        self.assertIn("quantized_psychogeography", model_output)
        self.assertIn("relational_flows", model_output)
        first_flow = model_output["relational_flows"][0]
        self.assertIn("quantized_cost_class", first_flow)
        self.assertIn("relation_type", first_flow)
        self.assertIn("decision_choice_D", first_flow)

    def test_prolog_kb_integration(self):
        prolog = PrologAxiomProgram()
        boundaries = prolog.parse_and_query_string("psychogeographical_boundary(?X, ?Y)")
        self.assertGreater(len(boundaries), 0)


if __name__ == "__main__":
    unittest.main()
