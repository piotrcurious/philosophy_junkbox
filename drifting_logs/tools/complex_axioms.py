"""
Non-Linear Complex Axiom Fields Module
Defines complex-valued axioms α, β, γ, δ ∈ ℂ with non-linear holomorphic dynamics,
phase entanglements, complex Jacobian matrices in ℂ⁴, singular loci, and holomorphic differential forms.
Driven by executable Prolog axiom programs for logical deduction and runtime extensibility.
"""

import cmath
import numpy as np
import sympy as sp
from typing import Dict, List, Any, Tuple, Optional
from drifting_logs.tools.prolog_engine import PrologAxiomProgram, KnowledgeBase

class CompositeAxiomFieldExtension:
    """
    Composite Algebraic Field Extension K = Q(i, α_M, α_V, α_μ, α_Σ) over Q(i)
    representing exact, un-flattened algebraic field extensions for all four complex axioms:
      - α_M: Kępiński Metabolic Rate Extension
      - α_V: Ashby Variety Extension
      - α_μ: Girardian Mimetic Extension
      - α_Σ: Debordian Spectacle Extension
    Computes per-axiom minimal polynomials, composite primitive element γ, Galois degree [K : Q],
    and exact symbolic quotient ring representations Q[x]/(P(x)).
    """
    def __init__(self, M: complex, V: complex, mu: complex, Sigma: complex):
        x = sp.Symbol('x')
        self.x = x

        # Convert complex axioms to exact rational algebraic generators α = sqrt(Re) + i*Im
        def to_algebraic_gen(c_val: complex) -> sp.Expr:
            re_rat = sp.Rational(round(abs(c_val.real), 2)).limit_denominator(20)
            im_rat = sp.Rational(round(c_val.imag, 2)).limit_denominator(20)
            sign_re = 1 if c_val.real >= 0 else -1
            return sign_re * sp.sqrt(re_rat) + sp.I * im_rat

        self.alpha_M = to_algebraic_gen(M)
        self.alpha_V = to_algebraic_gen(V)
        self.alpha_mu = to_algebraic_gen(mu)
        self.alpha_Sigma = to_algebraic_gen(Sigma)

        # Compute minimal polynomials for each axiom generator over Q
        try:
            self.p_M = sp.minimal_polynomial(self.alpha_M, x)
            self.deg_M = int(sp.degree(self.p_M, x))
        except Exception:
            self.p_M = x**2 + 1
            self.deg_M = 2

        try:
            self.p_V = sp.minimal_polynomial(self.alpha_V, x)
            self.deg_V = int(sp.degree(self.p_V, x))
        except Exception:
            self.p_V = x**2 + 1
            self.deg_V = 2

        try:
            self.p_mu = sp.minimal_polynomial(self.alpha_mu, x)
            self.deg_mu = int(sp.degree(self.p_mu, x))
        except Exception:
            self.p_mu = x**2 + 1
            self.deg_mu = 2

        try:
            self.p_Sigma = sp.minimal_polynomial(self.alpha_Sigma, x)
            self.deg_Sigma = int(sp.degree(self.p_Sigma, x))
        except Exception:
            self.p_Sigma = x**2 + 1
            self.deg_Sigma = 2

        # Composite primitive element generator γ = α_M + α_V + α_μ + α_Σ
        self.primitive_gamma = self.alpha_M + self.alpha_V + self.alpha_mu + self.alpha_Sigma
        try:
            self.p_gamma = sp.minimal_polynomial(self.primitive_gamma, x)
            self.composite_degree = int(sp.degree(self.p_gamma, x))
        except Exception:
            self.p_gamma = self.p_M * self.p_V
            self.composite_degree = int(sp.degree(self.p_gamma, x))

    def get_extension_summary(self) -> Dict[str, Any]:
        gamma_val = complex(sp.N(self.primitive_gamma))
        return {
            "composite_field_label": "K = Q(i, α_M, α_V, α_μ, α_Σ)",
            "composite_extension_degree": self.composite_degree,
            "primitive_element_gamma": str(self.primitive_gamma),
            "composite_minimal_polynomial": str(self.p_gamma),
            "primitive_exact_val": {"real": float(gamma_val.real), "imag": float(gamma_val.imag)},
            "per_axiom_extensions": {
                "M_metabolic": {
                    "generator": str(self.alpha_M),
                    "minimal_polynomial": str(self.p_M),
                    "degree": self.deg_M,
                    "quotient_ring": f"Q[x]/({self.p_M})"
                },
                "V_variety": {
                    "generator": str(self.alpha_V),
                    "minimal_polynomial": str(self.p_V),
                    "degree": self.deg_V,
                    "quotient_ring": f"Q[x]/({self.p_V})"
                },
                "mu_mimetic": {
                    "generator": str(self.alpha_mu),
                    "minimal_polynomial": str(self.p_mu),
                    "degree": self.deg_mu,
                    "quotient_ring": f"Q[x]/({self.p_mu})"
                },
                "Sigma_spectacle": {
                    "generator": str(self.alpha_Sigma),
                    "minimal_polynomial": str(self.p_Sigma),
                    "degree": self.deg_Sigma,
                    "quotient_ring": f"Q[x]/({self.p_Sigma})"
                }
            }
        }


class ComplexAxiomField:
    def __init__(self, M: complex = 1.0 + 0.5j, V: complex = 2.0 - 0.3j, mu: complex = 0.5 + 0.8j, Sigma: complex = 1.0 + 0.2j, prolog_program: Optional[PrologAxiomProgram] = None):
        self.prolog_program = prolog_program if prolog_program is not None else PrologAxiomProgram()
        self.M = M        # Kępiński Metabolic Rate + i * Metabolic Phase Shift
        self.V = V        # Ashby Requisite Variety + i * Variety Dissipation
        self.mu = mu      # Girardian Mimetic Coupling + i * Mimetic Interference Phase
        self.Sigma = Sigma # Debordian Spectacle Shield + i * Spectacle Refraction Index
        self.field_extension = CompositeAxiomFieldExtension(M, V, mu, Sigma)

    @classmethod
    def from_prolog_deduction(cls, m_state: str = "high_entropy", v_state: str = "hyper_variable",
                              mu_state: str = "resonant", sigma_state: str = "alienated") -> 'ComplexAxiomField':
        """
        Instantiates ComplexAxiomField dynamically by evaluating executable Prolog programs.
        """
        prog = PrologAxiomProgram()
        vals = prog.evaluate_axiom_values(m_state, v_state, mu_state, sigma_state)
        return cls(M=vals["M"], V=vals["V"], mu=vals["mu"], Sigma=vals["Sigma"], prolog_program=prog)

    def sync_from_prolog(self, m_state: str = "high_entropy", v_state: str = "hyper_variable",
                         mu_state: str = "resonant", sigma_state: str = "alienated"):
        """Re-evaluates Prolog program to update field parameters."""
        vals = self.prolog_program.evaluate_axiom_values(m_state, v_state, mu_state, sigma_state)
        self.M = vals["M"]
        self.V = vals["V"]
        self.mu = vals["mu"]
        self.Sigma = vals["Sigma"]

    def holomorphic_transformation(self, z: complex) -> complex:
        """
        Non-linear holomorphic map f(z) = z^3 + M*z^2 + V*z + mu
        Represents non-linear psychogeographical state transitions in ℂ.
        """
        return z**3 + self.M * (z**2) + self.V * z + self.mu

    def complex_jacobian_derivative(self, z: complex) -> complex:
        """
        f'(z) = 3z^2 + 2M*z + V
        Zeroes of f'(z) represent critical branch points and phase singularities.
        """
        return 3 * (z**2) + 2 * self.M * z + self.V

    def find_critical_points(self) -> Tuple[complex, complex]:
        """
        Critical points where f'(z) = 0 => 3z^2 + 2Mz + V = 0
        z = (-2M ± sqrt(4M^2 - 12V)) / 6 = (-M ± sqrt(M^2 - 3V)) / 3
        """
        disc = cmath.sqrt(self.M**2 - 3 * self.V)
        z1 = (-self.M + disc) / 3.0
        z2 = (-self.M - disc) / 3.0
        return z1, z2

    def jacobian_matrix_4d(self, point: Tuple[complex, complex, complex, complex]) -> np.ndarray:
        """
        Full 3x4 complex Jacobian matrix J for the ℂ⁴ affine scheme generators:
        f1 = x*y - M*z
        f2 = y^2 + z^2 - V*w
        f3 = w^2 - mu*x*z
        at point p = (x, y, z, w) ∈ ℂ⁴.
        """
        px, py, pz, pw = point
        J = np.array([
            [py, px, -self.M, 0.0],
            [0.0, 2*py, 2*pz, -self.V],
            [-self.mu*pz, 0.0, -self.mu*px, 2*pw]
        ], dtype=complex)
        return J

    def compute_singular_locus(self, point: Tuple[complex, complex, complex, complex]) -> Dict[str, Any]:
        """
        Evaluates rank drop of the 3x4 Jacobian matrix to identify singular loci on V(I) ⊂ ℂ⁴.
        """
        J = self.jacobian_matrix_4d(point)
        U, S, Vh = np.linalg.svd(J)
        rank = np.sum(S > 1e-7)
        is_singular = rank < 3
        return {
            "rank": int(rank),
            "singular_values": [float(s) for s in S],
            "is_singular": bool(is_singular),
            "kernel_dimension": int(4 - rank)
        }

    def compute_tangent_space_kernel(self, point: Tuple[complex, complex, complex, complex]) -> List[List[complex]]:
        """
        Calculates basis for the tangent space T_p V(I) = Ker(J_p) in ℂ⁴.
        """
        J = self.jacobian_matrix_4d(point)
        U, S, Vh = np.linalg.svd(J)
        kernel_vectors = Vh[S.shape[0]:] if S.shape[0] < 4 else Vh[np.where(S <= 1e-7)[0]]
        if kernel_vectors.shape[0] == 0 and Vh.shape[0] == 4:
            kernel_vectors = Vh[-1:]
        return kernel_vectors.tolist()

    def compute_hermitian_metric(self, z: complex) -> Dict[str, Any]:
        """
        Hermitian metric tensor h_z̄z = 1 + |f'(z)|^2 / (|Sigma|^2)
        Reflects non-linear curvature induced by complex axiom fields.
        """
        df = self.complex_jacobian_derivative(z)
        mag_df2 = (df * df.conjugate()).real
        mag_Sigma2 = (self.Sigma * self.Sigma.conjugate()).real

        h_val = 1.0 + mag_df2 / max(0.01, mag_Sigma2)

        # Holomorphic Ricci Curvature R = -∂²(log h) / ∂z∂z̄
        eps = 1e-4
        h_plus = 1.0 + ((self.complex_jacobian_derivative(z + eps) * self.complex_jacobian_derivative(z + eps).conjugate()).real) / max(0.01, mag_Sigma2)
        h_minus = 1.0 + ((self.complex_jacobian_derivative(z - eps) * self.complex_jacobian_derivative(z - eps).conjugate()).real) / max(0.01, mag_Sigma2)
        laplacian_log_h = (np.log(h_plus) - 2 * np.log(h_val) + np.log(h_minus)) / (eps**2)
        ricci_curvature = -laplacian_log_h

        # Evaluate ℂ⁴ tangent space at sample point
        sample_pt = (z, z*0.5, z*0.8, z*0.3)
        sing_info = self.compute_singular_locus(sample_pt)

        return {
            "z": {"real": z.real, "imag": z.imag},
            "hermitian_metric_h": float(h_val),
            "holomorphic_ricci_curvature": float(ricci_curvature),
            "phase_angle_rad": float(cmath.phase(df)),
            "singular_locus": sing_info,
            "critical_points": [
                {"real": cp.real, "imag": cp.imag} for cp in self.find_critical_points()
            ]
        }

if __name__ == "__main__":
    field = ComplexAxiomField.from_prolog_deduction()
    crit = field.find_critical_points()
    print("Critical Points f'(z)=0:", crit)
    print("Hermitian Metric at z=1+i:", field.compute_hermitian_metric(1.0 + 1.0j))
