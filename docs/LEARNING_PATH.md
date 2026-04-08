# 🎓 CloudOps Ninja Learning Path

## Week-by-Week Roadmap to SRE Mastery

### **WEEK 1: Linux Foundation** 🐧

**Goal**: Get comfortable with Linux command line

#### Day 1-2: Basic Commands
```bash
# Essential commands to master
ls, cd, pwd, mkdir, touch, rm, cp, mv
cat, less, more, head, tail
grep, find, locate
chmod, chown
```

**Practice**:
```bash
# Create a project directory structure
mkdir -p ~/projects/cloudops/{app,config,logs}
cd ~/projects/cloudops
touch {app,config,logs}/.gitkeep
ls -la
```

#### Day 3-4: File Permissions & Users
- Understanding `chmod` (rwx permissions)
- User and group management
- sudo and privilege escalation
- Essential files: `/etc/passwd`, `/etc/sudoers`

**Challenge**: 
- Create a user, give them specific permissions, remove them

#### Day 5: Processes & Services
```bash
ps aux          # List processes
top             # Monitor resources
kill            # Terminate process
systemctl       # Manage services
journalctl      # View logs
```

#### Day 6-7: Networking Basics
```bash
ifconfig/ip     # Network config
netstat/ss      # Network connections
ping, tracert   # Network testing
curl, wget      # Download & test
ssh, scp        # Remote access
```

**Assignment**: Connect to a remote Linux VM via SSH

---

### **WEEK 2: Bash Scripting** 🔥

**Goal**: Write production-ready bash scripts

#### Day 1-2: Bash Fundamentals
```bash
#!/bin/bash
# Variables
VAR="value"
echo $VAR

# Conditionals
if [ condition ]; then
  echo "true"
else
  echo "false"
fi

# Loops
for i in {1..10}; do echo $i; done
while [ condition ]; do command; done
```

#### Day 3-4: Functions & Arguments
```bash
#!/bin/bash

function deploy() {
  SERVER=$1
  BRANCH=$2
  echo "Deploying $BRANCH to $SERVER"
}

# Usage
deploy "web-server" "main"

# Special variables
$0 - script name
$1, $2 - arguments
$@ - all arguments
$# - number of arguments
$? - exit code
```

#### Day 5: Error Handling & Debugging
```bash
#!/bin/bash
set -e    # Exit on error
set -u    # Exit on undefined variable
set -x    # Debug mode (print commands)

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Check exit codes
if [ $? -ne 0 ]; then
  echo "Command failed"
  exit 1
fi
```

#### Day 6-7: Practical Scripts
**Build these 3 scripts**:
1. **System Checker** (`check_system.sh`)
   - Check disk space, CPU, memory
   - Email alert if > 80% usage
   
2. **Backup Script** (`backup.sh`)
   - Back up files to a directory
   - Compress with timestamp
   - Clean up old backups (>7 days)

3. **Deployment Script** (`deploy.sh`)
   - Pull code from git
   - Run tests
   - Deploy to server
   - Rollback on failure

**Assignment**: Write all 3 scripts with error handling

---

### **WEEK 3: Python Fundamentals + Flask** 🐍

**Goal**: Build a working Flask web application

#### Day 1-2: Python Basics Review
```python
# Variables & types
name = "Cloud"
count = 42
is_ready = True

# Lists & Dictionaries
servers = ["web1", "web2", "web3"]
config = {"host": "localhost", "port": 5000}

# Functions
def deploy(server, version):
    return f"Deployed {version} to {server}"

# Classes
class Server:
    def __init__(self, name):
        self.name = name
    
    def status(self):
        return f"{self.name} is running"
```

#### Day 3-4: Flask Basics
```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Cloud is awesome!"})

@app.route('/api/status')
def status():
    return jsonify({
        "status": "healthy",
        "uptime": "99.9%",
        "timestamp": "2024-01-01"
    })

if __name__ == '__main__':
    app.run(debug=True)
```

**Run it**:
```bash
pip install flask
python app.py
# Visit http://localhost:5000
```

#### Day 5-6: Build a Real API
Create an API that returns:
- Server health status
- Cloud costs (mock data at first)
- Deployment history
- Infrastructure metrics

```python
@app.route('/api/servers')
def get_servers():
    return jsonify({
        "aws": {"count": 3, "status": "healthy"},
        "gcp": {"count": 2, "status": "healthy"}
    })
```

#### Day 7: Database Integration
```python
# With SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String(50))
    environment = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

**Assignment**: Build a Flask app with SQLite that tracks your "deployments"

---

### **WEEK 4: AWS - First Cloud Deployment** ☁️

**Goal**: Get comfortable with AWS basics and deploy your Flask app

#### Day 1-2: AWS Fundamentals
- **EC2**: Virtual machines
- **S3**: File storage
- **RDS**: Managed databases
- **IAM**: User permissions
- **VPC**: Networking
- **ALB**: Load balancer

**Free Tier**: Most of these are free for 12 months!

#### Day 3: Set Up AWS Account
1. Create AWS account
2. Set up IAM user (not root!)
3. Create access keys
4. Configure AWS CLI

```bash
pip install awscli
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Region: us-east-1
# - Output format: json
```

#### Day 4: Create First EC2 Instance
```bash
# Via CLI
aws ec2 run-instances \
  --image-id ami-0d527b8c289b4af7f \
  --instance-type t2.micro \
  --key-name my-key-pair

# Or use AWS Console (easier first time)
```

**Connect to it**:
```bash
ssh -i my-key-pair.pem ec2-user@YOUR_IP
```

#### Day 5: Deploy Flask App to EC2
```bash
# On the EC2 instance
git clone <your-repo>
cd CloudOps-Ninja/backend
pip install -r requirements.txt
python app.py
```

#### Day 6: Add Load Balancer & Auto Scaling
- Create Application Load Balancer
- Set up Auto Scaling group
- Configure health checks

#### Day 7: Add RDS Database
```bash
# Create managed PostgreSQL/MySQL
aws rds create-db-instance \
  --db-instance-identifier cloudops-db \
  --engine postgres \
  --db-instance-class db.t2.micro
```

**Assignment**: Get your Flask app running on AWS EC2 with a real database

---

### **WEEK 5: Infrastructure as Code (Terraform)** 🏗️

**Goal**: Use Terraform to automate infrastructure creation

#### Day 1-2: Terraform Basics
```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0d527b8c289b4af7f"
  instance_type = "t2.micro"
  
  tags = {
    Name = "cloudops-web"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-cloudops-data"
}
```

**Commands**:
```bash
terraform init          # Initialize
terraform plan          # Preview changes
terraform apply         # Create resources
terraform destroy       # Delete resources
terraform state show    # View current state
```

#### Day 3-4: Build AWS Infrastructure
Create `infrastructure/aws/main.tf` with:
- VPC and networking
- EC2 instances
- RDS database
- S3 buckets
- Load balancer

#### Day 5-6: Variables & Outputs
```hcl
# variables.tf
variable "environment" {
  type = string
}

variable "instance_count" {
  default = 2
}

# outputs.tf
output "dns_name" {
  value = aws_lb.main.dns_name
}
```

#### Day 7: State Management
- Understand `terraform.tfstate`
- Remote state with S3/TF Cloud
- Team collaboration tips

**Assignment**: Deploy all AWS infrastructure with Terraform

---

### **WEEK 6: GCP - Multi-Cloud Mastery** 🚀

**Goal**: Repeat Week 5 but on GCP

#### Day 1-2: GCP Basics
- **Compute Engine**: Virtual machines (like EC2)
- **Cloud Storage**: File storage (like S3)
- **Cloud SQL**: Managed database (like RDS)
- **Load Balancing**: Distribute traffic
- **IAM**: Permissions management

#### Day 3-4: Set Up GCP
```bash
# Install Google Cloud SDK
# Then authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Day 5: Deploy on GCP with Terraform
Same Terraform code, but use GCP provider:

```hcl
provider "google" {
  project = "my-project"
  region  = "us-central1"
}

resource "google_compute_instance" "web" {
  name         = "cloudops-web"
  machine_type = "e2-micro"
  zone         = "us-central1-a"
}
```

#### Day 6: Multi-Cloud Challenges
- Deploy same app to both AWS and GCP
- Compare costs
- Compare performance
- Learn differences

#### Day 7: Terraform Modules
```hcl
module "aws_web" {
  source = "./modules/web_server"
  providers = { aws = aws }
}

module "gcp_web" {
  source = "./modules/web_server"
  providers = { google = google }
}
```

**Assignment**: Deploy to both clouds with one Terraform config

---

### **WEEK 7+: SRE - Site Reliability Engineering** 🔥

**Goal**: Learn to operate systems reliably

#### Phase 1: Monitoring (Day 1-3)
```bash
# Set up Prometheus
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Add custom metrics from your Flask app
from prometheus_client import Counter, Histogram

requests_total = Counter("requests_total", "Total requests")
request_duration = Histogram("request_duration", "Request duration")
```

#### Phase 2: Alerting (Day 4-5)
- Set up AlertManager
- Create alert rules
- Send to Slack/email
- Practice on-call rotation

```yaml
# prometheus_rules.yml
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: rate(errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
```

#### Phase 3: Incident Response (Day 6-7)
```python
# incident_response.py
def handle_alert(alert):
    if alert.severity == "critical":
        # 1. Create incident ticket
        # 2. Page on-call engineer
        # 3. Start runbook
        # 4. Scale infrastructure
        # 5. Notify stakeholders
        pass
```

**Assignment**: Create a complete monitoring & alerting system

#### Advanced Topics (Week 8+)
- Logging (ELK Stack)
- Tracing (Jaeger/Zipkin)
- Cost optimization
- Chaos engineering
- Disaster recovery
- Capacity planning

---

## 🎯 Practice Challenges

### Easy
- [ ] Deploy Flask app locally
- [ ] Create 3 bash scripts
- [ ] Make your app talk to a database

### Medium
- [ ] Deploy to AWS EC2
- [ ] Use Terraform to create AWS infrastructure
- [ ] Set up basic monitoring

### Hard
- [ ] Deploy to both AWS and GCP simultaneously
- [ ] Set up complete monitoring and alerting
- [ ] Create a self-healing infrastructure
- [ ] Simulate an incident and resolve it

### Extreme
- [ ] Multi-region deployment
- [ ] Disaster recovery automation
- [ ] Cost optimization across clouds
- [ ] Chaos engineering experiments

---

## ✅ Success Criteria

By the end of Week 7, you should be able to:

- [✓] Write production bash scripts
- [✓] Build Python applications with Flask
- [✓] Deploy infrastructure with Terraform
- [✓] Manage resources on AWS and GCP
- [✓] Monitor, alert, and respond to incidents
- [✓] Troubleshoot issues in production
- [✓] Automate deployments
- [✓] Scale applications automatically

---

## 📚 Additional Resources

- **Linux**: `man` command, online tutorials
- **Bash**: ShellCheck (code quality tool)
- **Python**: Real Python, Flask docs
- **AWS**: AWS documentation, A Cloud Guru
- **GCP**: Google Cloud tutorials
- **SRE**: Google SRE Book (free online)

---

**Keep going! You've got this! 🚀**
