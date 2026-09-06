"""
REST API Backend Server with Complex Axioms, Holomorphic Manifold Geometry,
Prolog Inferences, Singular Locus Analysis, and Autonomous Epistemic Exploration Endpoints.
"""

import os
import json
import sys
import cmath
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from drifting_logs.tools.algebraic_model_transformer import AlgebraicModelTransformer
from drifting_logs.tools.prolog_engine import build_psychogeographical_kb, Term
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
            kb = build_psychogeographical_kb()
            traps = kb.query(Term("systemic_trap", [Term("X"), Term("W")]))
            self.wfile.write(json.dumps({"systemic_traps": traps}).encode())
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
            M_r = float(req_data.get('M_r', 1.5))
            M_i = float(req_data.get('M_i', 0.8))
            V_r = float(req_data.get('V_r', 2.2))
            V_i = float(req_data.get('V_i', -0.5))
            mu_r = float(req_data.get('mu_r', 0.7))
            mu_i = float(req_data.get('mu_i', 1.1))
            Sigma_r = float(req_data.get('Sigma_r', 1.2))
            Sigma_i = float(req_data.get('Sigma_i', 0.4))

            M = complex(M_r, M_i)
            V = complex(V_r, V_i)
            mu = complex(mu_r, mu_i)
            Sigma = complex(Sigma_r, Sigma_i)

            transformed = transformer_engine.transform_model(M=M, V=V, mu=mu, Sigma=Sigma)
            self._set_headers(200)
            self.wfile.write(json.dumps(transformed).encode())
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
