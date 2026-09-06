"""
REST API Backend Server with Algebraic Geometry, Prolog Deduction,
and Dynamic Model Transformer Endpoints for Psychogeographical Exploration.
"""

import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure drifting_logs root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from drifting_logs.tools.algebraic_model_transformer import AlgebraicModelTransformer
from drifting_logs.tools.prolog_engine import build_psychogeographical_kb, Term
from drifting_logs.tools.etiological_listening_center import EtiologicalListeningCenter

PORT = 8080
transformer_engine = AlgebraicModelTransformer()

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

        if self.path == '/api/data':
            self._set_headers(200)
            try:
                with open('drifting_logs/multidimensional_psychogeographical_map.json', 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        if self.path == '/api/deduce_prolog':
            self._set_headers(200)
            kb = build_psychogeographical_kb()
            traps = kb.query(Term("systemic_trap", [Term("X"), Term("W")]))
            corridors = kb.query(Term("entropic_corridor", [Term("X"), Term("Z")]))
            self.wfile.write(json.dumps({
                "systemic_traps": traps,
                "entropic_corridors": corridors
            }).encode())
            return

        if self.path == '/api/diagnosis':
            self._set_headers(200)
            center = EtiologicalListeningCenter()
            diag = center.run_full_diagnosis()
            self.wfile.write(json.dumps(diag).encode())
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b'{}'

        try:
            req_data = json.loads(post_body.decode('utf-8'))
        except Exception:
            req_data = {}

        if self.path == '/api/axiom_transform':
            M = float(req_data.get('M', 1.0))
            V = float(req_data.get('V', 2.0))
            mu = float(req_data.get('mu', 0.5))
            Sigma = float(req_data.get('Sigma', 1.0))

            transformed = transformer_engine.transform_model(M=M, V=V, mu=mu, Sigma=Sigma)
            self._set_headers(200)
            self.wfile.write(json.dumps(transformed).encode())
            return

        if self.path == '/api/reorganize':
            query = req_data.get('query', 'Reorganize nodes')
            M = float(req_data.get('M', 1.0))
            V = float(req_data.get('V', 2.0))
            mu = float(req_data.get('mu', 0.5))
            Sigma = float(req_data.get('Sigma', 1.0))

            transformed = transformer_engine.transform_model(M=M, V=V, mu=mu, Sigma=Sigma)

            res_summary = {
                "meta_summary": f"Symbolic Algebraic Transformation executed for query: '{query}' under axioms M={M}, V={V}, mu={mu}, Sigma={Sigma}.",
                "algebraic_scheme": transformed["algebraic_scheme"],
                "prolog_deductions": transformed["prolog_deductions"],
                "reorganized_nodes": transformed["rebuilt_nodes"]
            }
            self._set_headers(200)
            self.wfile.write(json.dumps({"result": res_summary}).encode())
            return

        if self.path == '/api/epistemic_brake':
            status = req_data.get('status', 'engaged')
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "epistemic_brake_status": status,
                "message": f"Anti-Autofac Epistemic Brake status toggled to {status}."
            }).encode())
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
