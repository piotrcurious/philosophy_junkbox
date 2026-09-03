#!/usr/bin/env python3
"""
server.py - REST API Server for Interactive 3D WebGL Psychogeographical Map,
LLM Semantic Reorganization, and Epistemic Agents.
"""

import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from epistemic_agents import LLMInterface, create_agent_ensemble
from etiological_listening_center import EtiologicalListeningCenter
from psychogeographical_mapper import extract_drift_data

class PsychogeographicalAPIHandler(BaseHTTPRequestHandler):
    llm_engine = LLMInterface()
    listening_center = EtiologicalListeningCenter()

    def do_CorsHeaders(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.do_CorsHeaders()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/data':
            nodes, edges = extract_drift_data()
            response = {"status": "success", "nodes": nodes, "edges": edges}
            self._send_json(response)
        elif parsed.path == '/api/diagnosis':
            diagnosis = self.listening_center.listen_and_diagnose("Saint-Saturnin A75 BMW medical desert")
            self._send_json(diagnosis)
        elif parsed.path == '/' or parsed.path == '/webgl_map.html':
            try:
                with open('drifting_logs/webgl_map.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.do_CorsHeaders()
                self.end_headers()
                self.write(content)
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            payload = json.loads(post_data) if post_data else {}
        except Exception:
            payload = {}

        if parsed.path == '/api/reorganize':
            query = payload.get('query', 'Default semantic reorganization')
            nodes, _ = extract_drift_data()
            result = self.llm_engine.reorganize_semantics(query, nodes)
            self._send_json({"status": "success", "result": result})
        elif parsed.path == '/api/epistemic_brake':
            status = payload.get('status', 'engaged')
            self._send_json({
                "status": "success",
                "epistemic_brake": status,
                "message": f"Epistemic brake state set to '{status}'. Goal function loops evaluated."
            })
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.do_CorsHeaders()
        self.end_headers()
        self.wfile.write(body)

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PsychogeographicalAPIHandler)
    print(f"Psychogeographical API & WebGL Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
