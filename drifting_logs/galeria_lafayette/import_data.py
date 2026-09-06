#!/usr/bin/env python3
"""
import_data.py - Psychogeographical Data Import Engine

Parses, validates, normalizes, and ingests external psychogeographical drift data
and structural data (JSON or CSV) into the multi-dimensional Prolog & WebGL pipeline.
"""

import os
import sys
import json
import csv
import argparse

def parse_csv_drift_data(filepath):
    nodes = []
    trajectories = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            # Extract standard fields or dynamic dimensions
            archetype = row.get('archetype', 'CustomImport')
            node_id = row.get('id', f'node_{idx}')
            node_name = row.get('name', f'Imported Node {idx}')

            # Map numeric fields into raw_10d vector dictionary
            vector_dict = {}
            for k, v in row.items():
                if k not in ['archetype', 'id', 'name']:
                    try:
                        vector_dict[k] = float(v)
                    except ValueError:
                        pass

            traj_item = {
                'id': node_id,
                'name': node_name,
                'archetype': archetype,
                'raw_10d': vector_dict,
                'spatial_3d': {
                    'x': vector_dict.get('posX', 0.0),
                    'y': vector_dict.get('posY', 0.0),
                    'z': vector_dict.get('posZ', 0.0)
                },
                'mds_3d': {
                    'x': vector_dict.get('posX', 0.0) * 0.5,
                    'y': vector_dict.get('posY', 0.0) * 0.5,
                    'z': vector_dict.get('posZ', 0.0) * 0.5
                },
                'pca_3d': {
                    'x': vector_dict.get('posX', 0.0) * 0.8,
                    'y': vector_dict.get('posY', 0.0) * 0.8,
                    'z': vector_dict.get('posZ', 0.0) * 0.8
                }
            }
            trajectories.append(traj_item)

    return trajectories

def parse_json_drift_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'trajectories' in data:
        return data['trajectories']
    elif isinstance(data, dict) and 'nodes' in data:
        # Convert nodes schema into trajectory format
        trajectories = []
        for n in data['nodes']:
            vec = n.get('vector', [0.0]*10)
            traj_item = {
                'id': n.get('id', 'node'),
                'name': n.get('label', 'Node Label'),
                'archetype': 'StructuralImport',
                'raw_10d': {
                    'posX': vec[0] if len(vec) > 0 else 0.0,
                    'posY': vec[1] if len(vec) > 1 else 0.0,
                    'posZ': vec[2] if len(vec) > 2 else 0.0,
                    'temperature': vec[3] if len(vec) > 3 else 25.0,
                    'humidity': vec[4] if len(vec) > 4 else 0.5,
                    'commercialVal': vec[5] if len(vec) > 5 else 0.5,
                    'accessibility': vec[6] if len(vec) > 6 else 0.5,
                    'symbolicVal': vec[7] if len(vec) > 7 else 0.5,
                    'thermalStress': vec[8] if len(vec) > 8 else 0.5,
                    'flowDensity': vec[9] if len(vec) > 9 else 0.5,
                },
                'spatial_3d': {'x': vec[0] if len(vec) > 0 else 0.0, 'y': vec[1] if len(vec) > 1 else 0.0, 'z': vec[2] if len(vec) > 2 else 0.0},
                'mds_3d': {'x': (vec[0] if len(vec) > 0 else 0.0)*0.5, 'y': (vec[1] if len(vec) > 1 else 0.0)*0.5, 'z': (vec[2] if len(vec) > 2 else 0.0)*0.5},
                'pca_3d': {'x': (vec[0] if len(vec) > 0 else 0.0)*0.8, 'y': (vec[1] if len(vec) > 1 else 0.0)*0.8, 'z': (vec[2] if len(vec) > 2 else 0.0)*0.8}
            }
            trajectories.append(traj_item)
        return trajectories
    else:
        raise ValueError("Unrecognized JSON psychogeographical schema structure.")

def merge_and_export(imported_trajectories, base_json_path, output_json_path):
    base_data = {}
    if os.path.exists(base_json_path):
        with open(base_json_path, 'r', encoding='utf-8') as f:
            base_data = json.load(f)

    base_trajectories = base_data.get('trajectories', [])
    combined_trajectories = base_trajectories + imported_trajectories
    base_data['trajectories'] = combined_trajectories
    base_data['imported_count'] = len(imported_trajectories)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(base_data, f, indent=2)

    print(f"[Import Engine] Successfully merged {len(imported_trajectories)} items into {output_json_path}")

def main():
    parser = argparse.ArgumentParser(description="Psychogeographical Drift Data Import Engine")
    parser.add_argument("--input", "-i", required=True, help="Path to CSV or JSON data file to import")
    parser.add_argument("--base", "-b", default="decompressed_data.json", help="Path to base decompressed_data.json")
    parser.add_argument("--output", "-o", default="decompressed_data.json", help="Path to output merged JSON file")

    args = parser.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext == '.csv':
        trajectories = parse_csv_drift_data(args.input)
    elif ext in ['.json', '.geojson']:
        trajectories = parse_json_drift_data(args.input)
    else:
        sys.exit(f"Unsupported file format: {ext}")

    merge_and_export(trajectories, args.base, args.output)

if __name__ == "__main__":
    main()
