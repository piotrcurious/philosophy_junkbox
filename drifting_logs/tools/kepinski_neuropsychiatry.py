"""
Kępiński Localized Neuropsychiatric & LSTM Information Metabolism Engine
Models open-system information metabolism governed by neurotransmitters, genetics/epigenetics,
and a recurrent LSTM cell tracking long-term metabolic memory (c_t) and hidden psychic output (h_t).
"""

import math
import numpy as np
from typing import Dict, List, Any, Tuple

def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -15.0, 15.0)))

class KepinskiInformationLSTM:
    """
    Recurrent LSTM Cell for Kępiński Information Metabolism.
    Input x_t = [DA, 5-HT, NE, GABA, Glu, BDNF_expression] (dim 6)
    Hidden dim = 4 (representing 4 functional metabolic dimensions)
    """
    def __init__(self, input_dim: int = 6, hidden_dim: int = 4, seed: int = 42):
        np.random.seed(seed)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # Gate weights
        self.W_f = np.random.randn(hidden_dim, input_dim) * 0.5
        self.U_f = np.random.randn(hidden_dim, hidden_dim) * 0.5
        self.b_f = np.zeros((hidden_dim, 1))

        self.W_i = np.random.randn(hidden_dim, input_dim) * 0.5
        self.U_i = np.random.randn(hidden_dim, hidden_dim) * 0.5
        self.b_i = np.zeros((hidden_dim, 1))

        self.W_c = np.random.randn(hidden_dim, input_dim) * 0.5
        self.U_c = np.random.randn(hidden_dim, hidden_dim) * 0.5
        self.b_c = np.zeros((hidden_dim, 1))

        self.W_o = np.random.randn(hidden_dim, input_dim) * 0.5
        self.U_o = np.random.randn(hidden_dim, hidden_dim) * 0.5
        self.b_o = np.zeros((hidden_dim, 1))

        # Initial memory cell and hidden state
        self.c_t = np.zeros((hidden_dim, 1))
        self.h_t = np.zeros((hidden_dim, 1))

    def step(self, x_t: np.ndarray) -> Dict[str, Any]:
        """
        Executes one recurrent LSTM step for input x_t.
        """
        x_t = x_t.reshape(-1, 1)

        f_t = sigmoid(self.W_f @ x_t + self.U_f @ self.h_t + self.b_f)
        i_t = sigmoid(self.W_i @ x_t + self.U_i @ self.h_t + self.b_i)
        c_tilde = np.tanh(self.W_c @ x_t + self.U_c @ self.h_t + self.b_c)

        self.c_t = f_t * self.c_t + i_t * c_tilde
        o_t = sigmoid(self.W_o @ x_t + self.U_o @ self.h_t + self.b_o)
        self.h_t = o_t * np.tanh(self.c_t)

        return {
            "forget_gate_f_t": f_t.flatten().tolist(),
            "input_gate_i_t": i_t.flatten().tolist(),
            "output_gate_o_t": o_t.flatten().tolist(),
            "cell_memory_c_t": self.c_t.flatten().tolist(),
            "hidden_state_h_t": self.h_t.flatten().tolist()
        }

class LocalizedNodeNeuropsychiatry:
    """
    Node-level Neuropsychiatric & Epigenetic State Model.
    Tracks localized neurotransmitters, epigenetic methylation, and LSTM memory state.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id

        # Neurotransmitters (0.0 - 2.0)
        self.DA = 1.0     # Dopamine
        self.HT5 = 1.0    # Serotonin (5-HT)
        self.NE = 1.0     # Norepinephrine
        self.GABA = 1.0   # GABA
        self.Glu = 1.0    # Glutamate

        # Genetics / Epigenetics
        self.COMT_val158met = 0.5      # 0.0=Met/Met (stable DA), 1.0=Val/Val (high DA clearance)
        self.SERT_5httlpr = 0.5        # 0.0=s/s (vulnerable), 1.0=l/l (resilient)
        self.BDNF_methylation = 0.2    # 0.0=unmethylated (high plasticity), 1.0=hypermethylated
        self.H3K9ac_acetylation = 0.8  # Histone acetylation accessibility

        # LSTM Cell
        self.lstm = KepinskiInformationLSTM()

    def update_parameters(self, params: Dict[str, float]):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, float(v))

    def evaluate_metabolism(self) -> Dict[str, Any]:
        """
        Evaluates localized Kępiński Information Metabolism & Neuropsychiatric metrics.
        """
        # Effective BDNF Expression
        effective_BDNF = max(0.01, (1.0 - self.BDNF_methylation) * self.H3K9ac_acetylation)

        # Build input vector x_t
        x_t = np.array([self.DA, self.HT5, self.NE, self.GABA, self.Glu, effective_BDNF])
        lstm_out = self.lstm.step(x_t)

        h = np.array(lstm_out["hidden_state_h_t"])
        c = np.array(lstm_out["cell_memory_c_t"])

        # Functional Neuropsychiatric Diagnostic Metrics
        anhedonia_index = round(max(0.0, 1.0 - (self.DA * effective_BDNF) / max(0.1, self.NE * self.Glu)), 3)
        psychiatric_strain_index = round(float(np.std(x_t) * (1.0 + self.COMT_val158met) / max(0.1, self.HT5)), 3)
        information_metabolism_entropy = round(float(np.var(c) + np.var(h) + (self.NE / max(0.1, self.GABA))), 3)

        # Complex Axiom Shift vector derived from localized neuropsychiatry
        # Local ΔM, ΔV, Δμ ∈ ℂ
        delta_M = complex(round(float(h[0] * 0.5 + self.DA * 0.2), 3), round(float(h[1] * 0.3 - self.NE * 0.2), 3))
        delta_V = complex(round(float(h[2] * 0.5 + self.HT5 * 0.2), 3), round(float(h[3] * 0.3 - self.Glu * 0.2), 3))

        return {
            "node_id": self.node_id,
            "neurotransmitters": {
                "DA_dopamine": self.DA,
                "5HT_serotonin": self.HT5,
                "NE_norepinephrine": self.NE,
                "GABA": self.GABA,
                "Glu_glutamate": self.Glu
            },
            "epigenetics": {
                "COMT_val158met": self.COMT_val158met,
                "SERT_5httlpr": self.SERT_5httlpr,
                "BDNF_methylation": self.BDNF_methylation,
                "H3K9ac_acetylation": self.H3K9ac_acetylation,
                "effective_BDNF_expression": round(effective_BDNF, 3)
            },
            "lstm_cell_state": lstm_out,
            "diagnostic_metrics": {
                "anhedonia_index": anhedonia_index,
                "psychiatric_strain_index": psychiatric_strain_index,
                "information_metabolism_entropy": information_metabolism_entropy
            },
            "localized_axiom_shifts": {
                "delta_M": {"real": delta_M.real, "imag": delta_M.imag},
                "delta_V": {"real": delta_V.real, "imag": delta_V.imag}
            }
        }

if __name__ == "__main__":
    node_model = LocalizedNodeNeuropsychiatry("Saint-Saturnin")
    eval_res = node_model.evaluate_metabolism()
    print("Saint-Saturnin Neuropsychiatric Evaluation:")
    print("Anhedonia Index:", eval_res["diagnostic_metrics"]["anhedonia_index"])
    print("Information Metabolism Entropy:", eval_res["diagnostic_metrics"]["information_metabolism_entropy"])
    print("Localized ΔM:", eval_res["localized_axiom_shifts"]["delta_M"])
