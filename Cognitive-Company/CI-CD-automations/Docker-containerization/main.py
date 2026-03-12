#!/usr/bin/env python3
"""
Centaurion Framework - Main Entry Point
"""

import os
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8000))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"""
        <html>
        <head><title>Centaurion Framework</title></head>
        <body>
        <h1>Centaurion Framework</h1>
        <p>AI-Driven Cognitive Operating System</p>
        <hr>
        <p>Started: {datetime.now()}</p>
        <p>Status: Running</p>
        </body>
        </html>
        """
        self.wfile.write(response.encode())

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    print("=" * 50)
    print("Centaurion Framework")
    print("AI-Driven Cognitive Operating System")
    print("=" * 50)
    print(f"Started at: {datetime.now()}")
    print(f"Port: {PORT}")
    print("-" * 50)

    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"Server running at http://0.0.0.0:{PORT}")
    print("-" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
