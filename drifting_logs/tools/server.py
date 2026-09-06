"""
REST API Backend Server with Complex Axioms, Localized Neuropsychiatry & LSTM Memory,
Directed Relational Flow Dynamics, Holomorphic Manifold Geometry, Executable Prolog Axiom Programs,
Agent Personality Editing, and Epistemic Exploration Endpoints.
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
from drifting_logs.tools.epistemic_agents import create_agent_ensemble, load_all_logs_text

PORT = 8080
transformer_engine = AlgebraicModelTransformer()
explorer_engine = AutonomousEpistemicExplorer()
agent_ensemble = create_agent_ensemble()
raw_logs_context = load_all_logs_text()
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

        if self.path == '/api/get_agents':
            self._set_headers(200)
            agents_info = {
                k: {
                    "name": agent.name,
                    "lens": agent.lens,
                    "personality": agent.personality.to_dict()
                } for k, agent in agent_ensemble.items()
            }
            self.wfile.write(json.dumps(agents_info).encode())
            return

        if self.path == '/api/get_prolog_kb':
            self._set_headers(200)
            rules_str = transformer_engine.prolog_program.kb.get_all_rules_repr()
            self.wfile.write(json.dumps({"rules": rules_str}).encode())
            return

        if self.path == '/api/deduce_prolog':
            self._set_headers(200)
            prolog = transformer_engine.prolog_program
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
            flow_acceleration = float(req_data.get('flow_acceleration', 1.0))
            global_impedance = float(req_data.get('global_impedance', 1.0))
            node_overrides = req_data.get('node_overrides', None)

            M = complex(M_r, M_i)
            V = complex(V_r, V_i)
            mu = complex(mu_r, mu_i)
            Sigma = complex(Sigma_r, Sigma_i)

            transformed = transformer_engine.transform_model(
                M=M, V=V, mu=mu, Sigma=Sigma, node_overrides=node_overrides,
                use_prolog_deduction=use_prolog, flow_acceleration=flow_acceleration, global_impedance=global_impedance
            )
            self._set_headers(200)
            self.wfile.write(json.dumps(transformed).encode())
            return

        if self.path == '/api/update_agent_personality':
            agent_key = req_data.get('agent_key', 'kepinski')
            personality_traits = req_data.get('traits', {})
            if agent_key in agent_ensemble:
                agent_ensemble[agent_key].update_personality(personality_traits)
                analysis_res = agent_ensemble[agent_key].analyze(raw_logs_context)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "status": f"Agent {agent_key} personality updated successfully.",
                    "agent": agent_key,
                    "personality": agent_ensemble[agent_key].personality.to_dict(),
                    "analysis": analysis_res
                }).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Agent {agent_key} not found"}).encode())
            return

        if self.path == '/api/inject_prolog_fact':
            fact_name = req_data.get('fact_name', 'linked')
            args = req_data.get('args', ['node_a', 'node_b'])
            transformer_engine.prolog_program.inject_fact(fact_name, args)
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "Fact successfully injected", "rules": transformer_engine.prolog_program.kb.get_all_rules_repr()}).encode())
            return

        if self.path == '/api/retract_prolog_relation':
            head_name = req_data.get('head_name', '')
            head_args = req_data.get('head_args', None)
            count = transformer_engine.prolog_program.retract_relation(head_name, head_args)
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": f"Retracted {count} matching rules/facts", "rules": transformer_engine.prolog_program.kb.get_all_rules_repr()}).encode())
            return

        if self.path == '/api/query_prolog_custom':
            query_str = req_data.get('query', 'systemic_trap(?X, ?W)')
            res = transformer_engine.prolog_program.parse_and_query_string(query_str)
            self._set_headers(200)
            self.wfile.write(json.dumps({"query": query_str, "results": res}).encode())
            return

        if self.path == '/api/inject_prolog_rule':
            head_str = req_data.get('head_str', 'custom_rule')
            head_args = req_data.get('head_args', ['X', 'Y'])
            body_terms = req_data.get('body_terms', [])

            transformer_engine.prolog_program.inject_rule(head_str, head_args, body_terms)
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "Rule successfully injected into Prolog engine", "rules": transformer_engine.prolog_program.kb.get_all_rules_repr()}).encode())
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
