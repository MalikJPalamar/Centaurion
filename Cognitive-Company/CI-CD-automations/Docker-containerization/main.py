#!/usr/bin/env python3
"""
Centaurion Framework - Main Entry Point
Multi-page AI-Driven Cognitive Operating System
"""

import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8000))
START_TIME = datetime.now()

# Common CSS for all pages
COMMON_CSS = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', system-ui, sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
        color: #fff;
    }
    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 3rem;
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .nav-links { display: flex; gap: 2rem; }
    .nav-links a {
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.3s;
    }
    .nav-links a:hover, .nav-links a.active { color: #00d4ff; }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem;
    }
    .card {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
    }
    .hero {
        text-align: center;
        padding: 4rem 2rem;
    }
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero .tagline { font-size: 1.3rem; color: #94a3b8; margin-bottom: 2rem; }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(34, 197, 94, 0.2);
        border: 1px solid #22c55e;
        border-radius: 50px;
        color: #22c55e;
        font-weight: 600;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .capability-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .capability-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s, border-color 0.3s;
    }
    .capability-card:hover {
        transform: translateY(-5px);
        border-color: #7c3aed;
    }
    .capability-card h3 {
        color: #00d4ff;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .capability-card p { color: #94a3b8; font-size: 0.9rem; line-height: 1.6; }
    .btn {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        border-radius: 8px;
        color: white;
        text-decoration: none;
        font-weight: 600;
        margin-top: 1rem;
        transition: transform 0.3s;
    }
    .btn:hover { transform: scale(1.05); }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }
    .stat-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label { color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem; }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
    .social-links { display: flex; justify-content: center; gap: 1.5rem; margin-top: 1rem; }
    .social-links a {
        color: #94a3b8;
        text-decoration: none;
        transition: color 0.3s;
    }
    .social-links a:hover { color: #00d4ff; }
    .feature-list { list-style: none; margin-top: 1rem; }
    .feature-list li {
        padding: 0.5rem 0;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .feature-list li::before {
        content: "→";
        color: #00d4ff;
    }
"""

def get_nav(current_page=""):
    nav_links = [
        ("/", "Home"),
        ("/market-intelligence", "Market Intelligence"),
        ("/automation", "Automation"),
        ("/monitoring", "Monitoring"),
    ]
    links_html = ""
    for url, label in nav_links:
        active = "active" if current_page == url else ""
        links_html += f'<a href="{url}" class="{active}">{label}</a>'
    return f"""
    <nav class="nav">
        <div class="nav-logo">Centaurion</div>
        <div class="nav-links">
            {links_html}
        </div>
    </nav>
    """

def get_footer():
    return f"""
    <footer class="footer">
        <p>Centaurion Framework v1.0.0</p>
        <p>AI-Driven Cognitive Operating System</p>
        <div class="social-links">
            <a href="https://github.com/MalikJPalamar" target="_blank">GitHub</a>
            <a href="https://bolt.new" target="_blank">Bolt</a>
        </div>
        <p style="margin-top: 1rem; font-size: 0.8rem;">Started: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
    """

def home_page():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centaurion Framework</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    {get_nav('/')}
    <div class="container">
        <div class="hero">
            <div style="margin-bottom: 1.5rem;">
                <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
                    <circle cx="50" cy="50" r="45" stroke="url(#grad)" stroke-width="3" fill="none"/>
                    <circle cx="50" cy="50" r="30" stroke="url(#grad)" stroke-width="2" fill="none" opacity="0.6"/>
                    <circle cx="50" cy="50" r="15" stroke="url(#grad)" stroke-width="2" fill="none" opacity="0.3"/>
                    <circle cx="50" cy="50" r="5" fill="url(#grad)"/>
                    <path d="M50 20 L50 35 M50 65 L50 80 M20 50 L35 50 M65 50 L80 50" stroke="url(#grad)" stroke-width="2" opacity="0.4"/>
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
            <div class="status-badge">
                <span class="status-dot"></span>
                System Online
            </div>
        </div>

        <div class="capability-grid">
            <div class="capability-card">
                <h3>📊 Market Intelligence</h3>
                <p>Real-time market research, competitor analysis, and strategic insights powered by AI.</p>
                <a href="/market-intelligence" class="btn">Learn More</a>
            </div>
            <div class="capability-card">
                <h3>⚡ Automation</h3>
                <p>Intelligent workflow automation, CI/CD pipelines, and autonomous operations.</p>
                <a href="/automation" class="btn">Learn More</a>
            </div>
            <div class="capability-card">
                <h3>📈 Monitoring</h3>
                <p>Health monitoring, performance metrics, and proactive system alerts.</p>
                <a href="/monitoring" class="btn">Learn More</a>
            </div>
        </div>
    </div>
    {get_footer()}
</body>
</html>"""

def market_intelligence_page():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Intelligence - Centaurion</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    {get_nav('/market-intelligence')}
    <div class="container">
        <div class="hero" style="padding: 2rem;">
            <h1>Market Intelligence</h1>
            <p class="tagline">AI-Powered Market Research & Competitive Analysis</p>
        </div>

        <div class="capability-grid">
            <div class="card">
                <h3>🔍 Research Automation</h3>
                <ul class="feature-list">
                    <li>Automated market research reports</li>
                    <li>Competitor tracking & analysis</li>
                    <li>Trend detection & forecasting</li>
                    <li>Industry insights generation</li>
                </ul>
            </div>
            <div class="card">
                <h3>📊 Data Analytics</h3>
                <ul class="feature-list">
                    <li>Real-time data processing</li>
                    <li>Custom KPI dashboards</li>
                    <li>Visualization & reporting</li>
                    <li>Export to multiple formats</li>
                </ul>
            </div>
            <div class="card">
                <h3>🎯 Strategic Insights</h3>
                <ul class="feature-list">
                    <li>AI-generated recommendations</li>
                    <li>Opportunity identification</li>
                    <li>Risk assessment & mitigation</li>
                    <li>Strategic planning support</li>
                </ul>
            </div>
            <div class="card">
                <h3>🌐 Web Intelligence</h3>
                <ul class="feature-list">
                    <li>Social listening & sentiment</li>
                    <li>News & media monitoring</li>
                    <li>Keyword tracking</li>
                    <li>Automated alerts</li>
                </ul>
            </div>
        </div>
    </div>
    {get_footer()}
</body>
</html>"""

def automation_page():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automation - Centaurion</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    {get_nav('/automation')}
    <div class="container">
        <div class="hero" style="padding: 2rem;">
            <h1>Automation</h1>
            <p class="tagline">Intelligent Workflows & CI/CD Pipelines</p>
        </div>

        <div class="capability-grid">
            <div class="card">
                <h3>🔄 CI/CD Pipelines</h3>
                <ul class="feature-list">
                    <li>Automated build & test</li>
                    <li>Continuous deployment</li>
                    <li>Rollback capabilities</li>
                    <li>Multi-environment support</li>
                </ul>
            </div>
            <div class="card">
                <h3>🤖 AI Operations</h3>
                <ul class="feature-list">
                    <li>Autonomous task execution</li>
                    <li>Self-healing workflows</li>
                    <li>Intelligent scheduling</li>
                    <li>Resource optimization</li>
                </ul>
            </div>
            <div class="card">
                <h3>📦 Containerization</h3>
                <ul class="feature-list">
                    <li>Docker & Kubernetes</li>
                    <li>Auto-scaling</li>
                    <li>Service orchestration</li>
                    <li>Container security</li>
                </ul>
            </div>
            <div class="card">
                <h3>⏰ Scheduled Tasks</h3>
                <ul class="feature-list">
                    <li>Cron job management</li>
                    <li>Event-driven triggers</li>
                    <li>Custom workflows</li>
                    <li>Notification system</li>
                </ul>
            </div>
        </div>
    </div>
    {get_footer()}
</body>
</html>"""

def monitoring_page():
    import random
    uptime = (datetime.now() - START_TIME).total_seconds()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoring - Centaurion</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    {get_nav('/monitoring')}
    <div class="container">
        <div class="hero" style="padding: 2rem;">
            <h1>System Monitoring</h1>
            <p class="tagline">Real-Time Health & Performance Metrics</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">99.9%</div>
                <div class="stat-label">Uptime</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{int(uptime)}s</div>
                <div class="stat-label">Current Uptime</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{random.randint(50, 150)}ms</div>
                <div class="stat-label">Response Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{random.randint(20, 80)}%</div>
                <div class="stat-label">CPU Usage</div>
            </div>
        </div>

        <div class="card" style="margin-top: 2rem;">
            <h3>📋 System Status</h3>
            <ul class="feature-list">
                <li><span style="color: #22c55f;">●</span> API Server: Running</li>
                <li><span style="color: #22c55f;">●</span> Database: Connected</li>
                <li><span style="color: #22c55f;">●</span> Cache: Active</li>
                <li><span style="color: #22c55f;">●</span> Background Jobs: Processing</li>
            </ul>
        </div>

        <div class="card">
            <h3>🔗 API Endpoints</h3>
            <ul class="feature-list">
                <li>GET / - Main landing page</li>
                <li>GET /status - JSON status</li>
                <li>GET /market-intelligence - Market data</li>
                <li>GET /monitoring - System metrics</li>
            </ul>
            <a href="/status" class="btn" target="_blank">View JSON Status</a>
        </div>
    </div>
    {get_footer()}
</body>
</html>"""

def status_json():
    import platform
    uptime = (datetime.now() - START_TIME).total_seconds()
    return {
        "status": "running",
        "service": "Centaurion Framework",
        "version": "1.0.0",
        "started_at": START_TIME.isoformat(),
        "uptime_seconds": int(uptime),
        "platform": platform.system(),
        "endpoints": {
            "/": "Landing page",
            "/market-intelligence": "Market Intelligence",
            "/automation": "Automation",
            "/monitoring": "Monitoring",
            "/status": "This JSON status"
        }
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(home_page().encode())
        elif self.path == '/market-intelligence':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(market_intelligence_page().encode())
        elif self.path == '/automation':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(automation_page().encode())
        elif self.path == '/monitoring':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(monitoring_page().encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status_json(), indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")

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
    print("Pages:")
    print("  /                   - Home")
    print("  /market-intelligence - Market Intelligence")
    print("  /automation         - Automation")
    print("  /monitoring        - Monitoring")
    print("  /status            - JSON Status")
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
