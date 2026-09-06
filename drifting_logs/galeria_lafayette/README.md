# Galeries Lafayette - 10D Psychogeographical Map Visualizer & Multi-Language Engine

An interactive, multi-dimensional psychogeographical map visualizer and formal drift trajectory analysis system for Galeries Lafayette, combining **SWI-Prolog**, **GHC Haskell**, **R**, **Python**, and **Three.js WebGL**.

---

## 🏛️ System Architecture

```
                                  ┌───────────────────────────┐
                                  │   drift_ontology.pl       │
                                  │   (SWI-Prolog Engine)     │
                                  └─────────────┬─────────────┘
                                                │ exports
                                                ▼
┌───────────────────────────┐     ┌───────────────────────────┐
│   TrajectoryEngine.hs     │     │   ontology_output.json    │
│   (GHC Haskell 10D)       │     │   (Formal Axiom Proofs)   │
└─────────────┬─────────────┘     └─────────────┬─────────────┘
              │ CSV trajectory                  │
              ▼                                 │
┌───────────────────────────┐                   │
│ high_dim_trajectories.csv │                   │
└─────────────┬─────────────┘                   │
              │                                 │
              └─────────────────┬───────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ dimension_decompression.R │
                  │ (R MDS/PCA Reduction)     │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │  decompressed_data.json   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐ ◄─── import_data.py
                  │    index.html (WebGL)     │      (Python CSV/JSON Ingestion)
                  └───────────────────────────┘
```

---

## 📦 Language Components

1. **SWI-Prolog (`drift_ontology.pl`)**
   - Serves as the core N-dimensional ontology and logic engine.
   - Registers spatial and psychogeographical dimensions (temperature, humidity, commerce index, accessibility, symbolic value, thermal stress, crowd flow density).
   - Formally checks 5 psychogeographical axioms: Thermal Barrier (A1), Commercial Exclusion (A2), Symbolic Spectacle (A3), Reachability Continuity (A4), and Surveillance Symmetry (A5).
   - Validates trajectory compatibility and exports `ontology_output.json`.

2. **GHC Haskell (`TrajectoryEngine.hs`)**
   - High-dimensional manifold trajectory interpolation engine.
   - Calculates cumulative 10D trajectory path distances and non-linear warped waypoints for archetypes (`Tourist`, `Worker`, `Resident`, `Surveillance`).
   - Supports CLI argument controls for interpolation step resolution and output paths (`./TrajectoryEngine <stepRes> <outFile>`).

3. **R (`dimension_decompression.R`)**
   - Performs Multidimensional Scaling (MDS via `cmdscale`) and Principal Component Analysis (PCA via `prcomp`) on high-dimensional scaled feature vectors.
   - Merges Prolog verification results and reduced 3D coordinates into `decompressed_data.json`.

4. **Python Data Import Engine (`import_data.py`)**
   - CLI tool to validate, parse, and merge external CSV or JSON psychogeographical drift data into the active WebGL pipeline.
   - Usage: `python3 import_data.py -i <input_file> -b decompressed_data.json -o decompressed_data.json`

5. **Three.js WebGL Visualizer (`index.html`)**
   - Interactive 3D visualization engine featuring:
     - 5 Projection Modes: Physical 3D Architecture, MDS, PCA, Custom 10D Axes Mapping, and Local Pivot Neighborhood Projections.
     - Flow Dynamics Simulation: Stream particles, node vortices, adjustable speed, turbulence, and particle density.
     - Non-linear Local Warping: Gamma factor warping and spatial curvature controls.
     - Feature Amplification Sliders: Dynamic weights for climate, commerce, symbolic heritage, and crowd flow.
     - Event Extensions: Friction jump vectors, pivot neighborhood sphere, cross-section slicing plane.
     - Prolog Formal Proof Status Overlay.
     - WebGL UI Drag-and-Drop / File Browser Data Import and Visualizer Session State Export (.json).

---

## 🧪 Running the Test Suite

Execute the automated end-to-end test suite:

```bash
python3 drifting_logs/galeria_lafayette/test_pipeline.py
```

The test suite validates Prolog formal proof output, Haskell trajectory binary compilation, R dimension decompression, Python data import engine, and index.html DOM integrity.
