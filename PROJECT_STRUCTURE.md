#!/bin/bash
# CloudOps Ninja - Project Structure Guide
# This file explains what each part does

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                     🥷 CloudOps Ninja - Project Structure                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

📂 ROOT DIRECTORY
├── 🐍 backend/ - Python Flask Application
│   ├── app.py                 The main application (what the user sees)
│   ├── requirements.txt        List of Python dependencies
│   ├── Dockerfile             Containerization recipe
│   └── config.py              Configuration (create this as needed)
│
├── 🏗️ infrastructure/ - Infrastructure as Code
│   ├── aws/                  Terraform for Amazon Web Services
│   │   ├── main.tf           AWS resources definition
│   │   ├── variables.tf       Input variables
│   │   └── outputs.tf         Output values
│   ├── gcp/                  Terraform for Google Cloud Platform
│   │   ├── main.tf           GCP resources definition
│   │   └── ...               (similar to aws/)
│   └── terraform.tfvars      Variable values (shared)
│
├── 🔧 scripts/ - Bash Automation Scripts
│   ├── setup-linux.sh         Initial environment setup
│   ├── deploy.sh              Deploy to AWS/GCP
│   ├── health-check.sh        Monitor system health
│   ├── cost-analyzer.sh       Analyze cloud costs (future)
│   └── destroy.sh             Clean up resources (future)
│
├── 📊 monitoring/ - Prometheus & Grafana Configuration
│   ├── prometheus/
│   │   └── prometheus.yml     What to monitor
│   ├── grafana/
│   │   └── dashboard.json     Visualization config
│   ├── alertmanager/          Alert routing (future)
│   └── docker-compose.yml     Start monitoring stack
│
├── 📚 docs/ - Learning Materials
│   ├── README.md              Project overview (this)
│   ├── LEARNING_PATH.md       Week-by-week guide
│   ├── QUICKSTART.md          5-minute setup
│   ├── LINUX_BASICS.md        Linux commands
│   ├── BASH_GUIDE.md          Bash scripting
│   ├── PYTHON_GUIDE.md        Python for SRE
│   ├── AWS_GUIDE.md           AWS setup (to create)
│   ├── GCP_GUIDE.md           GCP setup (to create)
│   ├── SRE_CONCEPTS.md        Monitoring & alerting
│   └── TROUBLESHOOTING.md     Common issues & fixes
│
├── 🐳 docker-compose.yml      Start full stack locally
├── 📝 Makefile                Quick commands (make help)
├── .gitignore                 What not to commit
└── .github/                   CI/CD configuration (future)
    └── workflows/
        └── deploy.yml         GitHub Actions

═══════════════════════════════════════════════════════════════════════════════

🚀 QUICK COMMANDS

Setup:
  chmod +x scripts/*.sh
  ./scripts/setup-linux.sh
  make setup

Development:
  make dev                    # Run Flask locally
  make run                    # Start Docker containers
  make stop                   # Stop containers

Deployment:
  make deploy-aws             # Deploy to AWS
  make deploy-gcp             # Deploy to GCP
  make terraform-init         # Initialize Terraform

Monitoring:
  make monitor                # Open Grafana
  make logs                   # Tail app logs
  make health                 # Check health

═══════════════════════════════════════════════════════════════════════════════

📖 LEARNING PROGRESSION

Week 1: Linux Foundation
  Read: docs/LINUX_BASICS.md
  Do:   Practice essential commands

Week 2: Bash Scripting
  Read: docs/BASH_GUIDE.md
  Do:   Write scripts/*.sh enhancements

Week 3: Python
  Read: docs/PYTHON_GUIDE.md
  Do:   Run and modify backend/app.py

Week 4: AWS Deployment
  Read: docs/AWS_GUIDE.md (create this)
  Do:   Deploy infrastructure using Terraform

Week 5: Terraform & IaC
  Read: infrastructure/aws/main.tf comments
  Do:   Create GCP infrastructure as code

Week 6: Multi-Cloud
  Read: infrastructure/gcp/main.tf
  Do:   Deploy same app to both clouds

Week 7: SRE & Monitoring
  Read: docs/SRE_CONCEPTS.md
  Do:   Set up Prometheus/Grafana (make run)

Weeks 8+: Advanced Topics
  Do:   Incident simulation, Chaos engineering, CI/CD

═══════════════════════════════════════════════════════════════════════════════

💡 KEY CONCEPTS

What You'll Learn:

  🐧 Linux    - Operating system fundamentals & commands
  🔥 Bash     - Shell scripting for automation
  🐍 Python   - General-purpose programming
  🌐 Flask    - Web framework for building APIs
  ☁️ AWS      - Amazon's cloud platform
  🚀 GCP      - Google's cloud platform
  🏗️ Terraform - Infrastructure as Code
  🐳 Docker   - Containerization
  📊 SRE      - Reliability engineering

═══════════════════════════════════════════════════════════════════════════════

🎯 WHAT EACH COMPONENT TEACHES

backend/app.py
  • Python programming
  • Flask web development
  • REST API design
  • JSON handling
  • Error handling
  • HTTP methods (GET, POST, etc.)

scripts/deploy.sh
  • Bash scripting
  • User input validation
  • Error handling with set -e
  • File structure navigation
  • Terraform integration

infrastructure/aws/main.tf
  • Terraform syntax
  • AWS resource creation
  • Infrastructure as Code concepts
  • VPC, subnets, security groups
  • Network architecture
  • Provisioning automation

docker-compose.yml
  • Multi-container applications
  • Service dependencies
  • Network configuration
  • Volume management
  • Environment variables
  • Health checks

monitoring/prometheus/prometheus.yml
  • Metrics collection
  • Data scraping
  • Time-series databases
  • Monitoring configuration

═══════════════════════════════════════════════════════════════════════════════

🔄 TYPICAL WORKFLOW

1. New Developer Joins
   git clone <repo>
   cd CloudOps-Ninja
   make setup

2. Learn Foundations
   read docs/LEARNING_PATH.md
   make dev                    # Run app locally
   make run                    # Run with Docker

3. Make Changes
   cd backend
   # Edit app.py
   docker-compose restart app  # Or save, Flask auto-reloads in debug

4. Deploy to Cloud
   terraform plan -out=tfplan
   terraform apply tfplan

5. Monitor in Production
   make monitor                # View Grafana

6. Troubleshoot Issues
   ref docs/TROUBLESHOOTING.md
   make logs
   make health

═══════════════════════════════════════════════════════════════════════════════

📊 PROJECT STATUS

Implemented ✅:
  ✓ Flask application with multiple endpoints
  ✓ Prometheus metrics endpoint
  ✓ Dockerfile for containerization
  ✓ Docker Compose for local development
  ✓ AWS Terraform configuration
  ✓ GCP Terraform configuration
  ✓ Bash deployment script
  ✓ Comprehensive learning guides
  ✓ Makefile with quick commands

TODO (Fun Challenges):
  ☐ Add CI/CD with GitHub Actions
  ☐ Create cost analyzer script
  ☐ Implement blue-green deployments
  ☐ Add chaos engineering experiments
  ☐ Create WebUI dashboard
  ☐ Add monitoring dashboards
  ☐ Implement auto-scaling
  ☐ Add disaster recovery setup

═══════════════════════════════════════════════════════════════════════════════

🎓 MINI CHALLENGES

Easy (1 hour):
  1. Start the app: make dev
  2. View dashboard: http://localhost:5000
  3. Test API: curl http://localhost:5000/api/status

Medium (2 hours):
  1. Read docs/BASH_GUIDE.md
  2. Add new endpoint to backend/app.py
  3. Modify scripts/health-check.sh

Hard (4 hours):
  1. Deploy to AWS: make deploy-aws
  2. Access instance via SSH
  3. Start app on EC2

Extreme (8+ hours):
  1. Deploy to both AWS and GCP
  2. Set up monitoring with Prometheus
  3. Create Grafana dashboard
  4. Simulate a failure and practice incident response

═══════════════════════════════════════════════════════════════════════════════

🆘 HELP

If stuck:
  1. Check docs/TROUBLESHOOTING.md
  2. Run: make logs
  3. Run: make health
  4. Read the error message carefully!
  5. Google the error

═══════════════════════════════════════════════════════════════════════════════

Ready to start? 🚀

  Step 1: Read docs/QUICKSTART.md
  Step 2: Run ./scripts/setup-linux.sh
  Step 3: Run make dev
  Step 4: Visit http://localhost:5000

Good luck! You've got this! 🥷

═══════════════════════════════════════════════════════════════════════════════

EOF

# Make this script executable
chmod +x "$(basename "$0")"
