#!/usr/bin/env python3
"""
CloudOps Ninja - Multi-Cloud Portfolio Site
A fun SRE learning project combining Python, Bash, Linux, AWS, and GCP
"""

from flask import Flask, jsonify, render_template_string
from datetime import datetime
import os
import json

app = Flask(__name__)

# Simple in-memory storage (upgrade to database later)
deployments = []
servers = {
    "aws": {"count": 2, "status": "healthy", "cpu": 23, "memory": 45},
    "gcp": {"count": 2, "status": "healthy", "cpu": 18, "memory": 38},
}

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page - Portfolio dashboard"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudOps Ninja 🥷</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { color: #00ff00; text-align: center; }
            .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .card { background: #2a2a2a; padding: 15px; border-radius: 8px; border-left: 4px solid #00ff00; }
            .number { font-size: 2em; color: #00ff00; font-weight: bold; }
            button { background: #00ff00; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #00dd00; }
            a { color: #00ff00; text-decoration: none; margin: 10px 20px 10px 0; }
            .api-link { display: inline-block; margin: 5px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🥷 CloudOps Ninja Dashboard</h1>
            <p style="text-align:center;">Learning SRE the fun way - deploying everywhere, monitoring everything!</p>
            
            <div class="stats">
                <div class="card">
                    <h3>AWS Cloud</h3>
                    <p>Status: <span style="color: #00ff00;">●</span> Healthy</p>
                    <p>Instances: <span class="number">2</span></p>
                    <p>CPU Usage: 23% | Memory: 45%</p>
                </div>
                
                <div class="card">
                    <h3>GCP Cloud</h3>
                    <p>Status: <span style="color: #00ff00;">●</span> Healthy</p>
                    <p>Instances: <span class="number">2</span></p>
                    <p>CPU Usage: 18% | Memory: 38%</p>
                </div>
                
                <div class="card">
                    <h3>Total Deployments</h3>
                    <p>Count: <span class="number">''' + str(len(deployments)) + '''</span></p>
                    <p>Last: ''' + (deployments[-1]['timestamp'] if deployments else 'Never') + '''</p>
                </div>
                
                <div class="card">
                    <h3>Uptime</h3>
                    <p>AWS: <span class="number">99.9%</span></p>
                    <p>GCP: <span class="number">99.95%</span></p>
                </div>
            </div>
            
            <hr style="margin-top: 30px; border: 1px solid #444;">
            <h3>🔗 API Endpoints (Learn our API):</h3>
            <div class="api-link"><a href="/api/status">→ GET /api/status - System health</a></div>
            <div class="api-link"><a href="/api/servers">→ GET /api/servers - Cloud stats</a></div>
            <div class="api-link"><a href="/api/deployments">→ GET /api/deployments - Deployment history</a></div>
            <div class="api-link"><a href="/api/metrics">→ GET /api/metrics - Prometheus metrics</a></div>
            
            <hr style="margin-top: 30px; border: 1px solid #444;">
            <h3>🎯 Next Steps:</h3>
            <ul>
                <li>📖 Read the LEARNING_PATH.md to understand the project</li>
                <li>🐧 Start with Linux basics (Week 1)</li>
                <li>🔥 Learn Bash scripting (Week 2)</li>
                <li>🐍 Explore this Python app (Week 3)</li>
                <li>☁️ Deploy to AWS (Week 4)</li>
                <li>🏗️ Use Terraform (Week 5)</li>
                <li>🚀 Deploy to GCP (Week 6)</li>
                <li>📊 Set up monitoring (Week 7+)</li>
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/api/status')
def api_status():
    """System status endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "uptime_percentage": 99.92,
        "message": "CloudOps Ninja is running! 🥷"
    })


@app.route('/api/servers')
def api_servers():
    """Cloud infrastructure stats"""
    return jsonify({
        "clouds": servers,
        "total_instances": servers["aws"]["count"] + servers["gcp"]["count"],
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/deployments')
def api_deployments():
    """Deployment history"""
    return jsonify({
        "total": len(deployments),
        "deployments": deployments,
        "last_deployment": deployments[-1] if deployments else None
    })


@app.route('/api/metrics')
def api_metrics():
    """Prometheus-style metrics (basic version)"""
    metrics = f"""# HELP cloudops_deployments_total Total deployments
# TYPE cloudops_deployments_total counter
cloudops_deployments_total {len(deployments)}

# HELP cloudops_uptime_percent Uptime percentage
# TYPE cloudops_uptime_percent gauge
cloudops_uptime_percent 99.92

# HELP cloudops_aws_cpu_percent AWS CPU usage
# TYPE cloudops_aws_cpu_percent gauge
cloudops_aws_cpu_percent {servers['aws']['cpu']}

# HELP cloudops_gcp_cpu_percent GCP CPU usage
# TYPE cloudops_gcp_cpu_percent gauge
cloudops_gcp_cpu_percent {servers['gcp']['cpu']}

# HELP cloudops_aws_memory_percent AWS Memory usage
# TYPE cloudops_aws_memory_percent gauge
cloudops_aws_memory_percent {servers['aws']['memory']}

# HELP cloudops_gcp_memory_percent GCP Memory usage
# TYPE cloudops_gcp_memory_percent gauge
cloudops_gcp_memory_percent {servers['gcp']['memory']}
"""
    return metrics, 200, {'Content-Type': 'text/plain'}


@app.route('/api/deploy/<cloud>/<version>')
def deploy(cloud, version):
    """Simulate a deployment"""
    if cloud not in ["aws", "gcp"]:
        return jsonify({"error": "Invalid cloud"}), 400
    
    deployment = {
        "cloud": cloud,
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    deployments.append(deployment)
    
    return jsonify({
        "message": f"Deployed {version} to {cloud}",
        "deployment": deployment
    }), 201


@app.route('/health')
def health():
    """Health check endpoint (for load balancers)"""
    return jsonify({"status": "ok"}), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False") == "True"
    
    print("""
    ╔═══════════════════════════════════════╗
    ║     🥷 CloudOps Ninja Starting 🥷     ║
    ╚═══════════════════════════════════════╝
    
    📊 Dashboard: http://localhost:{port}
    📡 API Docs:  http://localhost:{port}/api/status
    
    💡 Tip: Change environment variables:
       export PORT=8000
       export DEBUG=True
       export ENVIRONMENT=production
    """.format(port=port))
    
    app.run(host='0.0.0.0', port=port, debug=debug)
