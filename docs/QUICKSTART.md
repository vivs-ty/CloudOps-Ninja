# 🚀 Getting Started - Quick Start Guide

## 5-Minute Setup

### Step 1: Clone/Download the Project
Already done! You're reading this from inside `CloudOps-Ninja/`

### Step 2: Install Prerequisites
```bash
# Make setup scripts executable
chmod +x scripts/*.sh

# Run setup (installs Python, Docker, AWS CLI, Terraform, etc)
./scripts/setup-linux.sh
```

### Step 3: Run Locally (5 minutes)
```bash
# Option A: Simple Python development mode
cd backend
python3 app.py
# Visit: http://localhost:5000

# Option B: Full stack with Docker (recommended)
docker-compose up -d
# Visit: http://localhost:5000 (App)
# Visit: http://localhost:3000 (Grafana) - user: admin, pass: admin
# Visit: http://localhost:9090 (Prometheus)
```

### Step 4: Explore
```bash
# Run health checks
./scripts/health-check.sh

# View logs
docker-compose logs -f app

# Stop containers
docker-compose down
```

## What You Have Now

### 📁 Project Structure
```
CloudOps-Ninja/
├── 🐍 backend/              # Python Flask application
├── 🏗️ infrastructure/        # AWS & GCP Terraform code
├── 📝 scripts/              # Bash automation scripts
├── 📊 monitoring/           # Prometheus & Grafana config
├── 📚 docs/                 # Learning guides
└── 🐳 docker-compose.yml    # Local dev environment
```

### 🎯 What Each Part Teaches

| Part | What You Learn | Time |
|------|---|---|
| **backend/app.py** | Python, Flask, APIs | 1 hour |
| **scripts/*.sh** | Bash scripting, automation | 2 hours |
| **infrastructure/** | Terraform, IaC | 3 hours |
| **monitoring/** | Prometheus, Grafana, SRE | 4 hours |
| **docs/** | Complete learning path | Throughout |

## Quick Commands (Makefile)

```bash
make help               # Show all commands
make dev               # Run Flask directly
make run               # Start Docker containers
make deploy-aws        # Deploy to AWS
make deploy-gcp        # Deploy to GCP
make monitor           # Open Grafana
make health            # Check system health
make clean             # Cleanup
```

## 🎓 Recommended Learning Path

### Day 1: Foundation (2 hours)
```bash
# Read these in order:
1. README.md                    # This project overview
2. docs/LEARNING_PATH.md        # Full learning roadmap
3. docs/LINUX_BASICS.md         # Essential Linux commands
```

### Day 2: Python Deep Dive (3 hours)
```bash
# Run the app and understand it
cd backend
python3 app.py

# Read the code comments in app.py
# Try the API endpoints:
# - http://localhost:5000/
# - http://localhost:5000/api/status
# - http://localhost:5000/api/servers
```

### Day 3: Bash Scripting (3 hours)
```bash
# Read and practice
docs/BASH_GUIDE.md

# Look at these scripts:
scripts/health-check.sh         # Great example
scripts/deploy.sh               # More advanced
scripts/setup-linux.sh          # Full-featured

# Practice writing your own!
```

### Week 2: Docker & Local Deployment (5 hours)
```bash
# Start Docker containers
make run

# Understand what's running
docker-compose ps

# Check logs
docker-compose logs -f

# View Grafana
make monitor
```

### Week 3: AWS Deployment (8 hours)
```bash
# Prerequisites:
# 1. AWS Account (free tier)
# 2. AWS CLI configured: aws configure
# 3. Read: docs/AWS_GUIDE.md

# Deploy
make deploy-aws

# Monitor costs with:
# aws ce get-cost-and-usage ...
```

### Week 4: GCP & Multi-Cloud (8 hours)
```bash
# Prerequisites:
# 1. Google Cloud Account (free tier)
# 2. gcloud CLI configured
# 3. Read: docs/GCP_GUIDE.md

# Deploy
make deploy-gcp

# Now you're on both clouds! 🎉
```

## 🔥 First Real Challenge

### Challenge 1: Modify the Python App
**Objective**: Add a new API endpoint

```bash
# Edit backend/app.py and add:
@app.route('/api/hello/<name>')
def hello(name):
    return jsonify({"message": f"Hello, {name}!"})

# Test it:
# http://localhost:5000/api/hello/CloudOps
```

### Challenge 2: Write a Bash Script
**Objective**: Create a script that counts running processes

```bash
#!/bin/bash
PROCESS_COUNT=$(ps aux | wc -l)
echo "Running processes: $PROCESS_COUNT"
```

### Challenge 3: Deploy with Docker
**Objective**: Build and run the app in Docker

```bash
# Build the image
docker build -t myapp:1.0 backend/

# Run it
docker run -p 5000:5000 myapp:1.0

# Access at http://localhost:5000
```

## 🆘 Troubleshooting

### Python not found
```bash
# Install Python 3
apt install python3 -y

# Or on macOS
brew install python3
```

### Docker permission denied
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply new group
newgrp docker

# Or restart your terminal
```

### Port already in use
```bash
# Find what's using port 5000
lsof -i :5000
# or
netstat -tuln | grep 5000

# Kill it
kill -9 <PID>

# Or use different port
PORT=8000 make dev
```

### Docker Compose not found
```bash
# Install via pip
pip3 install docker-compose

# Or on macOS
brew install docker-compose
```

## 📚 Learning Resources

### Built-in Guides
- [LINUX_BASICS.md](LINUX_BASICS.md) - Command foundation
- [BASH_GUIDE.md](BASH_GUIDE.md) - Scripting mastery
- [PYTHON_GUIDE.md](PYTHON_GUIDE.md) - Python learning
- [AWS_GUIDE.md](AWS_GUIDE.md) - AWS setup
- [GCP_GUIDE.md](GCP_GUIDE.md) - GCP setup
- [SRE_CONCEPTS.md](SRE_CONCEPTS.md) - Site reliability

### External Resources
- **Linux**: `man` command (e.g., `man ls`)
- **Bash**: ShellCheck, Bash scripting tutorials
- **Python**: Real Python, Flask documentation
- **AWS**: AWS documentation, A Cloud Guru
- **GCP**: Google Cloud tutorials, Qwiklabs
- **SRE**: Google SRE Book (free: sre.google)

## 🎮 Gamification Ideas

Try these challenges:

- [ ] Run the app locally
- [ ] Modify the Python app (add endpoint)
- [ ] Write a bash script (50+ lines)
- [ ] Deploy to AWS
- [ ] Deploy to GCP
- [ ] Set up monitoring
- [ ] Handle an "incident" (simulate failures)
- [ ] Implement auto-scaling
- [ ] Set up CI/CD pipeline
- [ ] Run chaos engineering experiments

## 🎯 Success Milestones

After each week, you should be able to:

**Week 1**: SSH into a Linux server, use grep/find, write basic shell commands

**Week 2**: Write bash scripts with functions, error handling, and logging

**Week 3**: Build a Flask API with multiple endpoints and database

**Week 4**: Deploy to AWS EC2 with RDS database

**Week 5**: Automate infrastructure with Terraform

**Week 6**: Deploy multi-region setup across AWS and GCP

**Week 7**: Monitor systems with Prometheus and respond to alerts

## 🚀 Next Steps

1. **Read** [LEARNING_PATH.md](LEARNING_PATH.md) for detailed week-by-week guide
2. **Start** with [LINUX_BASICS.md](LINUX_BASICS.md)
3. **Run** `make dev` and explore the Python app
4. **Practice** the bash guide examples
5. **Deploy** to AWS following [AWS_GUIDE.md](AWS_GUIDE.md)

---

**You've got this! Let's go learn 🥷**

Questions? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
