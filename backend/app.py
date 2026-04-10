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

# Create database tables
with app.app_context():
    db.create_all()

# Initialize servers if not exist
    if not Server.query.filter_by(cloud='aws').first():
        db.session.add(Server(cloud='aws', count=2, status='healthy', cpu=23, memory=45))
    if not Server.query.filter_by(cloud='gcp').first():
        db.session.add(Server(cloud='gcp', count=2, status='healthy', cpu=18, memory=38))
    
    # Initialize default user if not exist
    if not User.query.filter_by(username='admin').first():
        from werkzeug.security import generate_password_hash
        db.session.add(User(username='admin', password=generate_password_hash('password')))
    
    db.session.commit()

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
def api_metrics():
    """Prometheus-style metrics (basic version)"""
    aws_server = Server.query.filter_by(cloud='aws').first()
    gcp_server = Server.query.filter_by(cloud='gcp').first()
    aws_cpu = aws_server.cpu if aws_server else 0
    aws_memory = aws_server.memory if aws_server else 0
    gcp_cpu = gcp_server.cpu if gcp_server else 0
    gcp_memory = gcp_server.memory if gcp_server else 0
    metrics = f"""# HELP cloudops_deployments_total Total deployments
# TYPE cloudops_deployments_total counter
cloudops_deployments_total {Deployment.query.count()}

# HELP cloudops_uptime_percent Uptime percentage
# TYPE cloudops_uptime_percent gauge
cloudops_uptime_percent 99.92

# HELP cloudops_aws_cpu_percent AWS CPU usage
# TYPE cloudops_aws_cpu_percent gauge
cloudops_aws_cpu_percent {aws_cpu}

# HELP cloudops_gcp_cpu_percent GCP CPU usage
# TYPE cloudops_gcp_cpu_percent gauge
cloudops_gcp_cpu_percent {gcp_cpu}

# HELP cloudops_aws_memory_percent AWS Memory usage
# TYPE cloudops_aws_memory_percent gauge
cloudops_aws_memory_percent {aws_memory}

# HELP cloudops_gcp_memory_percent GCP Memory usage
# TYPE cloudops_gcp_memory_percent gauge
cloudops_gcp_memory_percent {gcp_memory}
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
