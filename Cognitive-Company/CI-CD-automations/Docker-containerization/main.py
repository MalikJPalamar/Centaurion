#!/usr/bin/env python3
"""
Centaurion Framework - Main Entry Point
"""

import os
import sys
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8000))
START_TIME = datetime.now()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centaurion Framework</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
        }}
        .container {{
            text-align: center;
            padding: 3rem;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }}
        .logo {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .tagline {{
            font-size: 1.2rem;
            color: #94a3b8;
            margin-bottom: 2rem;
        }}
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            border-radius: 50px;
            color: #22c55e;
            font-weight: 600;
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .info {{
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #64748b;
            font-size: 0.9rem;
        }}
        .info span {{
            color: #00d4ff;
        }}
        .capabilities {{
            display: flex;
            gap: 0.75rem;
            justify-content: center;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }}
        .capability {{
            background: rgba(255,255,255,0.05);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.75rem;
            border: 1px solid rgba(255,255,255,0.1);
            color: #94a3b8;
        }}
        .api-link {{
            display: inline-block;
            margin-top: 1rem;
            color: #00d4ff;
            text-decoration: none;
            font-size: 0.85rem;
        }}
        .api-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" stroke="url(#grad)" stroke-width="3" fill="none"/>
                <circle cx="50" cy="50" r="30" stroke="url(#grad)" stroke-width="2" fill="none" opacity="0.6"/>
                <circle cx="50" cy="50" r="15" stroke="url(#grad)" stroke-width="2" fill="none" opacity="0.3"/>
                <circle cx="50" cy="50" r="5" fill="url(#grad)"/>
                <path d="M50 20 L50 35 M50 65 L50 80 M20 50 L35 50 M65 50 L80 50" stroke="url(#grad)" stroke-width="2" opacity="0.4"/>
                <path d="M30 30 L40 40 M60 60 L70 70 M30 70 L40 60 M60 40 L70 30" stroke="url(#grad)" stroke-width="2" opacity="0.4"/>
                <defs>
                    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#00d4ff"/>
                        <stop offset="100%" style="stop-color:#7c3aed"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <h1>Centaurion</h1>
        <p class="tagline">AI-Driven Cognitive Operating System</p>
        <div class="status">
            <span class="status-dot"></span>
            System Online
        </div>
        <div class="capabilities">
            <span class="capability">Market Intelligence</span>
            <span class="capability">AI Automation</span>
            <span class="capability">CI/CD Pipelines</span>
            <span class="capability">Monitoring</span>
        </div>
        <div class="info">
            <p>Started: <span>{START_TIME.strftime('%Y-%m-%d %H:%M:%S')}</span></p>
            <p>Version: <span>1.0.0</span></p>
            <a href="/status" class="api-link">View API Status</a>
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(response.encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                "status": "running",
                "started_at": START_TIME.isoformat(),
                "uptime_seconds": (datetime.now() - START_TIME).total_seconds(),
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(status, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>404 - Not Found</h1>")

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
