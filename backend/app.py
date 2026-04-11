#!/usr/bin/env python3
"""
CloudOps Ninja - Multi-Cloud Portfolio Site
A fun SRE learning project combining Python, Bash, Linux, AWS, and GCP
"""

from flask import Flask, jsonify, render_template_string, request, redirect, url_for, flash
from datetime import datetime
import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from health_check import HealthCheck

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'dev-secret-key-change-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Prometheus metrics
DEPLOYMENTS_TOTAL = Counter('cloudops_deployments_total', 'Total deployments', ['cloud'])
UPTIME_PERCENT = Gauge('cloudops_uptime_percent', 'Uptime percentage')
AWS_CPU_PERCENT = Gauge('cloudops_aws_cpu_percent', 'AWS CPU usage')
AWS_MEMORY_PERCENT = Gauge('cloudops_aws_memory_percent', 'AWS Memory usage')
GCP_CPU_PERCENT = Gauge('cloudops_gcp_cpu_percent', 'GCP CPU usage')
GCP_MEMORY_PERCENT = Gauge('cloudops_gcp_memory_percent', 'GCP Memory usage')

# Initialize metrics with current values
UPTIME_PERCENT.set(99.92)

# Database models
class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cloud = db.Column(db.String(10), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='success')

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cloud = db.Column(db.String(10), unique=True, nullable=False)
    count = db.Column(db.Integer, default=2)
    status = db.Column(db.String(20), default='healthy')
    cpu = db.Column(db.Integer, default=20)
    memory = db.Column(db.Integer, default=40)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create database tables and initialize data (skip in testing)
def initialize_app_data():
    """Initialize default application data"""
    # Initialize servers if not exist
    aws_server = Server.query.filter_by(cloud='aws').first()
    if not aws_server:
        aws_server = Server(cloud='aws', count=2, status='healthy', cpu=23, memory=45)
        db.session.add(aws_server)
    gcp_server = Server.query.filter_by(cloud='gcp').first()
    if not gcp_server:
        gcp_server = Server(cloud='gcp', count=2, status='healthy', cpu=18, memory=38)
        db.session.add(gcp_server)
    
    # Update Prometheus metrics with server data
    AWS_CPU_PERCENT.set(aws_server.cpu if aws_server else 23)
    AWS_MEMORY_PERCENT.set(aws_server.memory if aws_server else 45)
    GCP_CPU_PERCENT.set(gcp_server.cpu if gcp_server else 18)
    GCP_MEMORY_PERCENT.set(gcp_server.memory if gcp_server else 38)
    
    # Initialize default user if not exist
    if not User.query.filter_by(username='admin').first():
        from werkzeug.security import generate_password_hash
        db.session.add(User(username='admin', password=generate_password_hash('password')))
    
    # Initialize Prometheus metrics with current data
    aws_deployments = Deployment.query.filter_by(cloud='aws').count()
    gcp_deployments = Deployment.query.filter_by(cloud='gcp').count()
    DEPLOYMENTS_TOTAL.labels(cloud='aws').inc(aws_deployments)
    DEPLOYMENTS_TOTAL.labels(cloud='gcp').inc(gcp_deployments)
    
    db.session.commit()

if not app.config.get('TESTING'):
    with app.app_context():
        db.create_all()
        initialize_app_data()

# Simple in-memory storage (upgrade to database later) - REMOVED, now using DB

# ==================== AUTH ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - CloudOps Ninja</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; text-align: center; }
            form { background: #2a2a2a; padding: 20px; border-radius: 8px; max-width: 300px; margin: 0 auto; }
            input { display: block; width: 100%; margin: 10px 0; padding: 10px; }
            button { background: #00ff00; color: #000; padding: 10px; border: none; width: 100%; }
        </style>
    </head>
    <body>
        <h1>🥷 CloudOps Ninja Login</h1>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p>Default: admin / password</p>
    </body>
    </html>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==================== ROUTES ====================

@app.route('/')
@login_required
def home():
    """Home page - Portfolio dashboard"""
    # Get data from database
    aws_server = Server.query.filter_by(cloud='aws').first()
    gcp_server = Server.query.filter_by(cloud='gcp').first()
    total_deployments = Deployment.query.count()
    last_deployment = Deployment.query.order_by(Deployment.timestamp.desc()).first()
    last_timestamp = last_deployment.timestamp.isoformat() if last_deployment else 'Never'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudOps Ninja 🥷</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ color: #00ff00; text-align: center; }}
            .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .card {{ background: #2a2a2a; padding: 15px; border-radius: 8px; border-left: 4px solid #00ff00; }}
            .number {{ font-size: 2em; color: #00ff00; font-weight: bold; }}
            button {{ background: #00ff00; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
            button:hover {{ background: #00dd00; }}
            a {{ color: #00ff00; text-decoration: none; margin: 10px 20px 10px 0; }}
            .api-link {{ display: inline-block; margin: 5px 0; }}
            .user-info {{ text-align: right; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="user-info">
                Welcome, {current_user.username}! <a href="/logout">Logout</a>
            </div>
            <h1>🥷 CloudOps Ninja Dashboard</h1>
            <p style="text-align:center;">Learning SRE the fun way - deploying everywhere, monitoring everything!</p>
            
            <div class="stats">
                <div class="card">
                    <h3>AWS Cloud</h3>
                    <p>Status: <span style="color: #00ff00;">●</span> Healthy</p>
                    <p>Instances: <span class="number">{aws_server.count if aws_server else 0}</span></p>
                    <p>CPU Usage: {aws_server.cpu if aws_server else 0}% | Memory: {aws_server.memory if aws_server else 0}%</p>
                </div>
                
                <div class="card">
                    <h3>GCP Cloud</h3>
                    <p>Status: <span style="color: #00ff00;">●</span> Healthy</p>
                    <p>Instances: <span class="number">{gcp_server.count if gcp_server else 0}</span></p>
                    <p>CPU Usage: {gcp_server.cpu if gcp_server else 0}% | Memory: {gcp_server.memory if gcp_server else 0}%</p>
                </div>
                
                <div class="card">
                    <h3>Total Deployments</h3>
                    <p>Count: <span class="number">{total_deployments}</span></p>
                    <p>Last: {last_timestamp}</p>
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
            <div class="api-link"><a href="/api/health">→ GET /api/health - Comprehensive health check</a></div>
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


@app.route('/api/health')
def api_health():
    """Comprehensive health check endpoint
    
    Returns detailed health information about:
    - Database connectivity
    - System resources (CPU, memory, disk)
    - External service dependencies
    - Application status
    """
    health_checker = HealthCheck(db=db)
    health_report = health_checker.perform_all_checks()
    
    # Return appropriate HTTP status based on health
    http_status = 200 if health_report['status'] == 'healthy' else (503 if health_report['status'] == 'unhealthy' else 200)
    
    return jsonify(health_report), http_status


@app.route('/api/servers')
def api_servers():
    """Cloud infrastructure stats"""
    servers_data = {}
    total_instances = 0
    for server in Server.query.all():
        servers_data[server.cloud] = {
            "count": server.count,
            "status": server.status,
            "cpu": server.cpu,
            "memory": server.memory
        }
        total_instances += server.count
    return jsonify({
        "clouds": servers_data,
        "total_instances": total_instances,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/deployments')
def api_deployments():
    """Deployment history"""
    deployments_list = []
    for dep in Deployment.query.order_by(Deployment.timestamp.desc()).all():
        deployments_list.append({
            "cloud": dep.cloud,
            "version": dep.version,
            "timestamp": dep.timestamp.isoformat(),
            "status": dep.status
        })
    return jsonify({
        "total": len(deployments_list),
        "deployments": deployments_list,
        "last_deployment": deployments_list[0] if deployments_list else None
    })


@app.route('/api/metrics')
@login_required
def api_metrics():
    """Prometheus-style metrics (basic version)"""
    # Get current values from database (more reliable than Prometheus metrics)
    total_deployments = Deployment.query.count()
    
    metrics = f"""# HELP cloudops_deployments_total Total deployments
# TYPE cloudops_deployments_total counter
cloudops_deployments_total {total_deployments}

# HELP cloudops_uptime_percent Uptime percentage
# TYPE cloudops_uptime_percent gauge
cloudops_uptime_percent {UPTIME_PERCENT._value}

# HELP cloudops_aws_cpu_percent AWS CPU usage
# TYPE cloudops_aws_cpu_percent gauge
cloudops_aws_cpu_percent {AWS_CPU_PERCENT._value}

# HELP cloudops_aws_memory_percent AWS Memory usage
# TYPE cloudops_aws_memory_percent gauge
cloudops_aws_memory_percent {AWS_MEMORY_PERCENT._value}

# HELP cloudops_gcp_cpu_percent GCP CPU usage
# TYPE cloudops_gcp_cpu_percent gauge
cloudops_gcp_cpu_percent {GCP_CPU_PERCENT._value}

# HELP cloudops_gcp_memory_percent GCP Memory usage
# TYPE cloudops_gcp_memory_percent gauge
cloudops_gcp_memory_percent {GCP_MEMORY_PERCENT._value}
"""
    return metrics, 200, {'Content-Type': 'text/plain'}


@app.route('/api/deploy/<cloud>/<version>')
@login_required
def deploy(cloud, version):
    """Simulate a deployment"""
    if cloud not in ["aws", "gcp"]:
        return jsonify({"error": "Invalid cloud"}), 400
    
    new_deployment = Deployment(cloud=cloud, version=version, status='success')
    db.session.add(new_deployment)
    db.session.commit()
    
    # Update Prometheus metrics
    DEPLOYMENTS_TOTAL.labels(cloud=cloud).inc()
    
    deployment_data = {
        "cloud": new_deployment.cloud,
        "version": new_deployment.version,
        "timestamp": new_deployment.timestamp.isoformat(),
        "status": new_deployment.status
    }
    
    return jsonify({
        "message": f"Deployed {version} to {cloud}",
        "deployment": deployment_data
    }), 201


@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint for scraping"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


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
