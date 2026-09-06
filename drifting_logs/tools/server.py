"""
REST API Backend Server with Complex Axioms, Localized Neuropsychiatry & LSTM Memory,
Holomorphic Manifold Geometry, Executable Prolog Axiom Programs, and Epistemic Exploration Endpoints.
"""

import os
import json
import sys
import cmath
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from drifting_logs.tools.algebraic_model_transformer import AlgebraicModelTransformer
from drifting_logs.tools.prolog_engine import PrologAxiomProgram, Term
from drifting_logs.tools.autonomous_explorer import AutonomousEpistemicExplorer

PORT = 8080
transformer_engine = AlgebraicModelTransformer()
explorer_engine = AutonomousEpistemicExplorer()
step_counter = 0

class PsychogeographicalServer(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path == '/' or self.path == '/webgl_map.html':
            self._set_headers(200, "text/html")
            try:
                with open('drifting_logs/webgl_map.html', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(f"<h1>Error loading webgl_map.html: {str(e)}</h1>".encode())
            return

        if self.path == '/api/full_nodes':
            self._set_headers(200)
            try:
                with open('drifting_logs/full_extracted_dataset.json', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        if self.path == '/api/deduce_prolog':
            self._set_headers(200)
            prolog = PrologAxiomProgram()
            traps = prolog.kb.query(Term("systemic_trap", [Term("X"), Term("W")]))
            axiom_vals = prolog.evaluate_axiom_values()
            res = {
                "systemic_traps": traps,
                "derived_axiom_values": {k: {"real": v.real, "imag": v.imag} for k, v in axiom_vals.items()}
            }
            self.wfile.write(json.dumps(res).encode())
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_POST(self):
        global step_counter
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b'{}'

        try:
            req_data = json.loads(post_body.decode('utf-8'))
        except Exception:
            req_data = {}

        if self.path == '/api/axiom_transform':
            use_prolog = req_data.get('use_prolog_deduction', False)
            M_r = float(req_data.get('M_r', 1.5))
            M_i = float(req_data.get('M_i', 0.8))
            V_r = float(req_data.get('V_r', 2.2))
            V_i = float(req_data.get('V_i', -0.5))
            mu_r = float(req_data.get('mu_r', 0.7))
            mu_i = float(req_data.get('mu_i', 1.1))
            Sigma_r = float(req_data.get('Sigma_r', 1.2))
            Sigma_i = float(req_data.get('Sigma_i', 0.4))
            node_overrides = req_data.get('node_overrides', None)

            M = complex(M_r, M_i)
            V = complex(V_r, V_i)
            mu = complex(mu_r, mu_i)
            Sigma = complex(Sigma_r, Sigma_i)

            transformed = transformer_engine.transform_model(
                M=M, V=V, mu=mu, Sigma=Sigma, node_overrides=node_overrides, use_prolog_deduction=use_prolog
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(transformed).encode())
            return

        if self.path == '/api/inject_prolog_rule':
            head_str = req_data.get('head_str', 'custom_rule')
            head_args = req_data.get('head_args', ['X', 'Y'])
            body_terms = req_data.get('body_terms', [])

            transformer_engine.prolog_program.inject_rule(head_str, head_args, body_terms)
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "Rule successfully injected into Prolog engine"}).encode())
            return

        if self.path == '/api/node_neuropsychiatry_transform':
            node_id = req_data.get('node_id', 'Saint-Saturnin')
            neuro_params = req_data.get('params', {})

            node_model = transformer_engine.get_or_create_node_neuropsychiatry(node_id)
            node_model.update_parameters(neuro_params)
            eval_res = node_model.evaluate_metabolism()

            self._set_headers(200)
            self.wfile.write(json.dumps(eval_res).encode())
            return

        if self.path == '/api/autonomous_step':
            step_counter += 1
            res = explorer_engine.execute_exploration_step(step_counter)
            self._set_headers(200)
            self.wfile.write(json.dumps(res).encode())
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Post Endpoint not found"}).encode())

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, PsychogeographicalServer)
    print(f"Psychogeographical API Server listening on port {PORT}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
