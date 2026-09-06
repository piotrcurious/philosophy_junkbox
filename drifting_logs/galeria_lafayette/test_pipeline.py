#!/usr/bin/env python3
"""
Automated end-to-end test suite for Galeries Lafayette Psychogeographical Pipeline
Tests Prolog ontology output, Haskell trajectory generation with CLI parameters, R dimension decompression,
Python Data Import Engine, README documentation, and WebGL HTML asset integrity.
"""

import json
import os
import csv
import subprocess
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TestGaleriaLafayettePipeline(unittest.TestCase):

    def test_01_prolog_ontology_execution(self):
        """Test SWI-Prolog ontology execution and JSON schema output."""
        prolog_file = os.path.join(BASE_DIR, "drift_ontology.pl")
        cmd = ["swipl", "-g", "main", "-t", "halt", prolog_file]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        self.assertEqual(result.returncode, 0, f"Prolog failed: {result.stderr}")

        output_json = os.path.join(BASE_DIR, "ontology_output.json")
        self.assertTrue(os.path.exists(output_json), "ontology_output.json was not created")

        with open(output_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("dimensions", data)
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertIn("axioms", data)
        self.assertIn("verification", data)
        self.assertIn("formal_trajectories", data)

        self.assertEqual(len(data["nodes"]), 6)
        self.assertEqual(data["verification"]["manifold_status"], "PROVED_CONSISTENT")

    def test_02_haskell_trajectory_engine(self):
        """Test Haskell TrajectoryEngine binary compilation and CLI argument execution."""
        engine_hs = os.path.join(BASE_DIR, "TrajectoryEngine.hs")
        engine_bin = os.path.join(BASE_DIR, "TrajectoryEngine")
        csv_out = os.path.join(BASE_DIR, "high_dim_trajectories.csv")

        # Compile Haskell program
        compile_cmd = ["ghc", "-O2", engine_hs, "-o", engine_bin]
        compile_res = subprocess.run(compile_cmd, capture_output=True, text=True, cwd=BASE_DIR)
        self.assertEqual(compile_res.returncode, 0, f"GHC compile failed: {compile_res.stderr}")

        # Run binary with CLI parameters (resolution 0.2, custom csv)
        run_res = subprocess.run([engine_bin, "0.2", csv_out], capture_output=True, text=True, cwd=BASE_DIR)
        self.assertEqual(run_res.returncode, 0, f"TrajectoryEngine execution failed: {run_res.stderr}")
        self.assertTrue(os.path.exists(csv_out), "high_dim_trajectories.csv missing")

        # Verify CSV columns and rows
        with open(csv_out, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertGreater(len(rows), 10, "Trajectory CSV should have waypoints")
        expected_cols = ["archetype", "id", "name", "posX", "posY", "posZ",
                         "temperature", "humidity", "commercialVal",
                         "accessibility", "symbolicVal", "thermalStress", "flowDensity"]
        for col in expected_cols:
            self.assertIn(col, rows[0], f"Missing column {col} in trajectory CSV")

        # Clean up binary build artifacts
        for ext in ["", ".hi", ".o"]:
            target = engine_bin + ext
            if os.path.exists(target):
                os.remove(target)

    def test_03_r_dimension_decompression(self):
        """Test R dimension decompression script execution and decompressed_data.json schema."""
        r_script = os.path.join(BASE_DIR, "dimension_decompression.R")
        data_json = os.path.join(BASE_DIR, "decompressed_data.json")

        cmd = ["Rscript", r_script]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        self.assertEqual(result.returncode, 0, f"Rscript failed: {result.stderr}")
        self.assertTrue(os.path.exists(data_json), "decompressed_data.json missing")

        with open(data_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("trajectories", data)
        self.assertIn("prolog_verification", data)
        self.assertIn("prolog_axioms", data)
        self.assertIn("prolog_formal_trajectories", data)

        trajectories = data["trajectories"]
        self.assertGreater(len(trajectories), 0)
        first = trajectories[0]
        self.assertIn("spatial_3d", first)
        self.assertIn("mds_3d", first)
        self.assertIn("pca_3d", first)
        self.assertIn("raw_10d", first)

        self.assertIn("temperature", first["raw_10d"])
        self.assertIn("commercialVal", first["raw_10d"])

    def test_04_data_import_engine(self):
        """Test import_data.py Python Data Import Engine for CSV and JSON files."""
        import_py = os.path.join(BASE_DIR, "import_data.py")
        csv_in = os.path.join(BASE_DIR, "high_dim_trajectories.csv")
        base_json = os.path.join(BASE_DIR, "decompressed_data.json")
        out_json = os.path.join(BASE_DIR, "test_import_output.json")

        cmd = ["python3", import_py, "-i", csv_in, "-b", base_json, "-o", out_json]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        self.assertEqual(result.returncode, 0, f"Data import engine failed: {result.stderr}")
        self.assertTrue(os.path.exists(out_json), "Imported output JSON missing")

        with open(out_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("trajectories", data)
        self.assertIn("imported_count", data)
        self.assertGreater(data["imported_count"], 0)

        if os.path.exists(out_json):
            os.remove(out_json)

    def test_05_html_visualizer_integrity(self):
        """Test index.html DOM element structure and required controls."""
        html_path = os.path.join(BASE_DIR, "index.html")
        self.assertTrue(os.path.exists(html_path), "index.html missing")

        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        required_ids = [
            "projection-select",
            "select-pivot-node",
            "slider-w-thermal",
            "slider-w-commerce",
            "slider-w-symbolic",
            "slider-w-flow",
            "slider-flow-speed",
            "slider-flow-turb",
            "slider-particle-density",
            "slider-gamma",
            "slider-curvature",
            "chk-ext-friction",
            "chk-ext-pivot-sphere",
            "chk-ext-cross-section",
            "file-import-input",
            "btn-export-session",
            "import-status",
            "prolog-verification-panel",
            "info-panel"
        ]

        for req_id in required_ids:
            self.assertIn(f'id="{req_id}"', html_content, f"Missing DOM element id='{req_id}' in index.html")

    def test_06_readme_documentation(self):
        """Test presence and content of README.md documentation."""
        readme_path = os.path.join(BASE_DIR, "README.md")
        self.assertTrue(os.path.exists(readme_path), "README.md missing")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Galeries Lafayette", content)
        self.assertIn("drift_ontology.pl", content)
        self.assertIn("TrajectoryEngine.hs", content)

if __name__ == "__main__":
    unittest.main()
