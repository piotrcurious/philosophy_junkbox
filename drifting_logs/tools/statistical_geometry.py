"""
Statistical Geometry & Metric Embedding Module
Computes covariance matrices, Multidimensional Scaling (MDS) embeddings,
Riemannian manifold distance metrics, and vector field flows for psychogeographical drift.
"""

import numpy as np
from typing import Dict, List, Any, Tuple

class StatisticalGeometryEngine:
    def __init__(self, raw_features: np.ndarray = None):
        if raw_features is None:
            # Default raw metric matrix across nodes: [Spatial_Mobility, Cybernetic_Entrapment, Healthcare_Strain, Mimetic_Desire]
            self.features = np.array([
                [8.9, 2.1, 1.2, 3.4], # Saint-Saturnin
                [9.5, 7.8, 2.0, 4.1], # A75 Corridor
                [3.2, 1.1, 4.5, 2.0], # Montceau-les-Mines
                [4.1, 2.5, 3.1, 5.0], # Belfort-Lure
                [6.0, 4.0, 5.2, 1.5], # Aire de la Guye
                [1.5, 9.2, 3.0, 8.5], # Connected Car
                [0.5, 3.0, 9.8, 2.1], # Medical Desert
                [2.0, 8.5, 5.8, 9.1]  # Youth Inertia
            ])
        else:
            self.features = raw_features

    def compute_covariance_and_spectrum(self) -> Dict[str, Any]:
        cov = np.cov(self.features, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        idx = np.argsort(eigenvalues)[::-1]
        return {
            "covariance": cov.tolist(),
            "eigenvalues": eigenvalues[idx].tolist(),
            "eigenvectors": eigenvectors[:, idx].tolist()
        }

    def compute_mds_embedding(self, metric_tensor_weight: float = 1.0, dim: int = 3) -> np.ndarray:
        """
        Multidimensional Scaling (MDS) embedding with metric tensor weighting
        Transforms high-dimensional feature space into 3D manifold geometry coordinates.
        """
        N = self.features.shape[0]
        # Pairwise Mahalanobis / Metric weighted distance matrix
        diffs = self.features[:, None, :] - self.features[None, :, :]
        weight_matrix = np.diag([1.0, metric_tensor_weight, 1.0 / max(0.1, metric_tensor_weight), 1.0])

        dist_matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                d = diffs[i, j]
                dist_matrix[i, j] = np.sqrt(np.dot(d, np.dot(weight_matrix, d)))

        # Double centering matrix B
        H = np.eye(N) - np.ones((N, N)) / N
        B = -0.5 * H.dot(dist_matrix ** 2).dot(H)

        evals, evecs = np.linalg.eigh(B)
        idx = np.argsort(evals)[::-1]
        top_evals = np.maximum(0, evals[idx[:dim]])
        top_evecs = evecs[:, idx[:dim]]

        coords = top_evecs.dot(np.diag(np.sqrt(top_evals)))

        # Scale to canonical [-200, 200] range for WebGL visualization
        coords_max = np.max(np.abs(coords))
        if coords_max > 0:
            coords = (coords / coords_max) * 180.0

        return coords

    def compute_quantized_mds_embedding(self, metric_tensor_weight: float = 1.0,
                                         dim: int = 3,
                                         thresholds: List[float] = [2.0, 5.0, 9.0]) -> np.ndarray:
        """
        Level II Quantized MDS Embedding:
        Applies parameter quantization Q_1(d_ij) to continuous distance metrics before double centering,
        reflecting discrete step-like manifold geometry transitions.
        """
        N = self.features.shape[0]
        diffs = self.features[:, None, :] - self.features[None, :, :]
        weight_matrix = np.diag([1.0, metric_tensor_weight, 1.0 / max(0.1, metric_tensor_weight), 1.0])

        dist_matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                d = diffs[i, j]
                raw_d = np.sqrt(np.dot(d, np.dot(weight_matrix, d)))

                # Apply Level II Quantization Q_1(raw_d)
                q_class = 0
                for t in thresholds:
                    if raw_d >= t:
                        q_class += 1
                dist_matrix[i, j] = float(q_class * 2.5)

        H = np.eye(N) - np.ones((N, N)) / N
        B = -0.5 * H.dot(dist_matrix ** 2).dot(H)

        evals, evecs = np.linalg.eigh(B)
        idx = np.argsort(evals)[::-1]
        top_evals = np.maximum(0, evals[idx[:dim]])
        top_evecs = evecs[:, idx[:dim]]

        coords = top_evecs.dot(np.diag(np.sqrt(top_evals)))
        coords_max = np.max(np.abs(coords))
        if coords_max > 0:
            coords = (coords / coords_max) * 180.0

        return coords

    def compute_geodesic_flow_fields(self, M: float, V: float, mu: float, Sigma: float) -> List[Dict[str, Any]]:
        """
        Calculates vector flow fields representing psychogeographical drift velocities dx/dt
        under specific axiom configurations.
        """
        coords = self.compute_mds_embedding(metric_tensor_weight=Sigma / max(0.1, M))
        flows = []
        for i, pt in enumerate(coords):
            x, y, z = pt
            # Drift velocity vector field
            vx = -0.05 * x + (mu * y) / max(0.1, M)
            vy = -0.05 * y + (V * z) / max(0.1, Sigma)
            vz = -0.08 * z + (M * x) / max(0.1, mu)
            flows.append({
                "point": [float(x), float(y), float(z)],
                "velocity": [float(vx), float(vy), float(vz)],
                "magnitude": float(np.sqrt(vx**2 + vy**2 + vz**2))
            })
        return flows

if __name__ == "__main__":
    engine = StatisticalGeometryEngine()
    print("Covariance Spectrum:", engine.compute_covariance_and_spectrum()["eigenvalues"])
    print("MDS 3D Embedding:\n", engine.compute_mds_embedding())
    print("Flow Field Sample:", engine.compute_geodesic_flow_fields(1.0, 2.0, 0.5, 1.0)[0])
