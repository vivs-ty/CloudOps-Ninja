# 🥷 CloudOps Ninja - Zero to Hero DevOps/SRE Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/vivs-ty/CloudOps-Ninja?style=social)](https://github.com/vivs-ty/CloudOps-Ninja)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Bash 4.0+](https://img.shields.io/badge/Bash-4.0%2B-green)](https://www.gnu.org/software/bash/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0%2B-purple)](https://www.terraform.io/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue?logo=docker)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange?logo=amazon-aws)](https://aws.amazon.com/free/)
[![GCP](https://img.shields.io/badge/GCP-Free%20Tier-red?logo=google-cloud)](https://cloud.google.com/free)

A **fun, practical project** to learn Python, Bash, Linux, AWS, GCP, and SRE concepts by building a real multi-cloud monitoring and deployment system!

## 📚 What You'll Learn

### **Phase 1: Foundation (Weeks 1-2)**
- ✅ Linux basics & command line
- ✅ Bash scripting fundamentals
- ✅ Python basics

### **Phase 2: Single Cloud (Weeks 3-4)**
- ✅ AWS basics (EC2, S3, IAM)
- ✅ Infrastructure as Code (Terraform)
- ✅ CI/CD pipelines

### **Phase 3: Multi-Cloud (Weeks 5-6)**
- ✅ GCP basics (Compute Engine, Cloud Storage)
- ✅ Deployment automation
- ✅ Cost optimization

### **Phase 4: SRE Mastery (Weeks 7+)**
- ✅ Monitoring & alerting (Prometheus, Grafana)
- ✅ Logging systems (ELK Stack)
- ✅ Incident response automation
- ✅ Chaos engineering

## 🎯 Project Overview

### The Mission
Build a **Personal Portfolio Site** hosted on both AWS and GCP that:
- Auto-scales based on traffic
- Monitors itself and sends alerts
- Has a cool dashboard showing cloud stats
- Deploys with a single command
- Recovers from failures automatically

### Architecture
```
┌─────────────────────────────────────────────────────┐
│              CloudOps Ninja Dashboard               │
│  (Shows costs, uptime, deployments across clouds)   │
└─────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
    AWS Cloud                       GCP Cloud
  ┌──────────────┐              ┌──────────────┐
  │ Portfolio    │              │ Portfolio    │
  │ Site (Flask) │              │ Site (Flask) │
  │ ALB          │              │ Load Bal     │
  │ Auto-scaling │              │ Auto-scaling │
  │ RDS/Cloud SQL│              │ Cloud SQL    │
  └──────────────┘              └──────────────┘
        ↓                               ↓
        └───────────────┬───────────────┘
                        ↓
        ┌───────────────────────────────┐
        │   Monitoring & Alerting       │
        │ - Prometheus (metrics)        │
        │ - Grafana (dashboards)        │
        │ - AlertManager (alerts)       │
        │ - Custom Python scripts       │
        └───────────────────────────────┘
```

## 📂 Project Structure

```
CloudOps-Ninja/
├── backend/                    # Python Flask app
│   ├── app.py                 # Main application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container image
│   └── config.py              # Configuration
│
├── infrastructure/            # Infrastructure as Code
│   ├── aws/                   # AWS Terraform
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── gcp/                   # GCP Terraform
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── terraform.tfvars       # Variable values
│
├── scripts/                   # Bash automation scripts
│   ├── deploy.sh              # Deploy to cloud
│   ├── destroy.sh             # Clean up resources
│   ├── health-check.sh        # Monitor health
│   ├── cost-analyzer.sh       # Analyze cloud costs
│   └── setup-linux.sh         # Linux environment setup
│
├── monitoring/                # SRE monitoring & alerting
│   ├── prometheus/            # Prometheus config
│   │   └── prometheus.yml
│   ├── grafana/               # Grafana dashboards
│   │   └── dashboard.json
│   ├── alerting/              # Custom alert scripts
│   │   ├── check_uptime.py
│   │   ├── alert_handler.py
│   │   └── incident_response.py
│   └── docker-compose.yml     # Local monitoring stack
│
├── docs/                      # Learning documentation
│   ├── LEARNING_PATH.md       # Step-by-step guide
│   ├── LINUX_BASICS.md        # Linux commands cheatsheet
│   ├── BASH_GUIDE.md          # Bash scripting guide
│   ├── PYTHON_GUIDE.md        # Python learning path
│   ├── AWS_GUIDE.md           # AWS setup guide
│   ├── GCP_GUIDE.md           # GCP setup guide
│   ├── SRE_CONCEPTS.md        # SRE fundamentals
│   └── TROUBLESHOOTING.md     # Common issues & fixes
│
├── .github/                   # GitHub CI/CD
│   └── workflows/
│       └── deploy.yml         # Automated deployment
│
├── Makefile                   # Quick commands
├── docker-compose.yml         # Local development
└── .gitignore
```

## 🚀 Quick Start

### 1. **Clone & Setup** (5 min)
```bash
cd CloudOps-Ninja
chmod +x scripts/*.sh
./scripts/setup-linux.sh
```

### 2. **Run Locally** (10 min)
```bash
docker-compose up -d
# App runs at http://localhost:5000
# Monitoring at http://localhost:3000 (Grafana)
```

### 3. **Deploy to AWS** (30 min)
```bash
make deploy-aws
```

### 4. **Deploy to GCP** (30 min)
```bash
make deploy-gcp
```

### 5. **Monitor Everything** (ongoing)
```bash
make dashboard
# Check Grafana at http://localhost:3000
```

## 💡 Learning Milestones

Before you jump to each cloud, check the learning path:

| Milestone | What You'll Do | Time |
|-----------|---------------|------|
| **Linux Ninja** | Master SSH, file systems, permissions | Week 1 |
| **Bash Master** | Write production scripts | Week 2 |
| **Python Dev** | Build the Flask app | Week 2-3 |
| **AWS Warrior** | EC2, S3, IAM, RDS, infrastructure | Week 3-4 |
| **GCP Expert** | Compute Engine, Cloud SQL, networking | Week 4-5 |
| **SRE Legend** | Monitoring, alerting, incident response | Week 5+ |

## 🎓 Resources Included

Each `docs/` file has:
- Cheatsheets
- Command references
- Common mistakes & fixes
- Real production examples
- Practice challenges with answers

## 📊 Key Features to Build

1. **Auto-deploying Portfolio Site**
   - Shows your projects
   - Tracks deployment count
   - Live status across clouds

2. **Multi-Cloud Cost Dashboard**
   - Real AWS/GCP costs via APIs
   - Cost predictions
   - Optimization suggestions

3. **Self-Healing Infrastructure**
   - Auto-restarts failed services
   - Auto-scales on high load
   - Automatic rollback on errors

4. **Monitoring & Alerts**
   - Custom metrics
   - Slack/Email notifications
   - On-call rotation simulation

5. **Chaos Engineering Playground**
   - Intentionally break things
   - Practice incident response
   - Learn what breaks and why

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+ (Flask) |
| **Scripts** | Bash 4.0+ |
| **Infrastructure** | Terraform |
| **Containers** | Docker & Docker Compose |
| **Deployment** | AWS + GCP |
| **Monitoring** | Prometheus + Grafana |
| **Logging** | ELK Stack (optional) |
| **CI/CD** | GitHub Actions |

## 🔑 Prerequisites

```bash
# You need:
- WSL2 or Linux VM (or macOS)
- Docker & Docker Compose
- AWS Account (free tier works!)
- GCP Account (free tier works!)
- Git
- Code editor (VS Code recommended)
```

## 📖 Recommended Learning Order

1. **Start here**: `docs/LEARNING_PATH.md`
2. **Then**: `docs/LINUX_BASICS.md`
3. **Then**: `docs/BASH_GUIDE.md`
4. **Code**: `docs/PYTHON_GUIDE.md`
5. **Deploy**: `docs/AWS_GUIDE.md`
6. **Multi-Cloud**: `docs/GCP_GUIDE.md`
7. **Monitor**: `docs/SRE_CONCEPTS.md`

## 🎮 Gamification

- **Badges**: Unlock SRE badges as you complete milestones
- **Challenges**: Try the chaos engineering challenges
- **Leaderboard**: Track your infrastructure score
- **Incidents**: Simulate and resolve real incidents

## 🤝 Next Steps

1. Read `LEARNING_PATH.md` for step-by-step guidance
2. Follow the Linux basics tutorial
3. Set up your local environment
4. Deploy your first app!

## 📝 Notes

- This project uses **free tier** of AWS & GCP (mostly)
- Estimated learning time: **6-8 weeks** for full mastery
- Each phase builds on the previous one
- Feel free to customize and extend!

## 🆘 Help

- Check `docs/TROUBLESHOOTING.md` for common issues
- Review code comments for explanations
- Use `make help` to see available commands

---

**Let's build something awesome! 🚀**
