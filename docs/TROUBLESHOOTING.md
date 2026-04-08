# 🆘 Troubleshooting Guide

## Common Issues & Solutions

### Port Already in Use

**Problem**: Cannot start application because port 5000 is already in use

```bash
# Find what's using the port
lsof -i :5000
# or
netstat -tuln | grep 5000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=8000 python3 app.py
```

### Docker Permission Denied

**Problem**: `permission denied while trying to connect to Docker daemon`

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes immediately
newgrp docker

# Or logout and login again

# Verify it works
docker ps
```

### Python Package Not Found

**Problem**: `ModuleNotFoundError: No module named 'flask'`

```bash
# Install missing package
pip3 install flask

# Or install all requirements
pip3 install -r backend/requirements.txt

# Create virtual environment (best practice)
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Git Repository Issues

**Problem**: `fatal: not a git repository`

```bash
# Initialize git repository
git init

# Add remote
git remote add origin https://github.com/yourusername/CloudOps-Ninja.git

# Stage and commit
git add .
git commit -m "Initial commit"

# Push
git push -u origin main
```

### Terraform Errors

**Problem**: `Error: Failed to read state file`

```bash
# Reinitialize Terraform
cd infrastructure/aws
rm -rf .terraform .terraform.lock.hcl

# Reinit
terraform init

# Try again
terraform plan
```

### SSH Connection Refused

**Problem**: Cannot SSH to AWS/GCP instance

```bash
# 1. Check security group allows SSH
# AWS: Security Group should allow port 22 from your IP

# 2. Check you're using correct key
ssh -i path/to/key.pem ubuntu@YOUR_IP

# 3. Check key permissions
chmod 400 key.pem

# 4. Try with verbose output
ssh -vvv -i key.pem ubuntu@YOUR_IP
```

### Docker Compose Error

**Problem**: `docker-compose: command not found`

```bash
# Check if installed
docker-compose --version

# Install if missing
pip3 install docker-compose

# Or on newer systems
sudo apt install docker-compose
# or
brew install docker-compose
```

### Flask Application Not Starting

**Problem**: Flask app crashes or won't start

```bash
# Check for syntax errors
python3 -m py_compile backend/app.py

# Run with more verbose output
python3 -u app.py 2>&1 | head -50

# Check if port is listening
netstat -tuln | grep 5000

# Test the endpoint
curl http://localhost:5000/health || curl http://localhost:5000/
```

### Memory/Disk Issues

**Problem**: System running out of space or memory

```bash
# Check disk usage
df -h

# Find large files
find / -type f -size +100M

# Check memory
free -h

# Stop containers to free memory
docker-compose down

# Clean up Docker
docker system prune -af
```

### Prometheus Not Scraping Metrics

**Problem**: No data in Prometheus

```bash
# 1. Check prometheus.yml syntax
cat monitoring/prometheus/prometheus.yml

# 2. Verify targets are accessible
curl http://localhost:5000/api/metrics

# 3. Check container logs
docker-compose logs prometheus

# 4. Reload Prometheus
# Hit the `-` button in Prometheus UI or restart:
docker-compose restart prometheus
```

### Grafana Login Issues

**Problem**: Cannot login to Grafana (http://localhost:3000)

```bash
# Default credentials
username: admin
password: admin

# If you forgot:
# Stop container
docker-compose down

# Restart with clean state
docker volume rm cloudops_grafana-data
docker-compose up

# Default creds again
```

### Linux Line Endings Issue (CRLF)

**Problem**: `unexpected token $'do\r'` when running bash script

```bash
# This is usually from editing on Windows (CRLF endings)

# Fix for single file
dos2unix script.sh

# Or convert manually
sed -i 's/\r$//' script.sh

# Or when cloning
git config --global core.autocrlf input
```

---

## Debugging Techniques

### Enable Debug Logging

```bash
# Python Flask
export DEBUG=True
python3 app.py

# Bash scripts
bash -x script.sh

# Verbose Docker
docker-compose -v up
```

### Check Services Status

```bash
# All containers
docker-compose ps

# Container logs (realtime)
docker-compose logs -f app

# Specific container logs
docker logs <container_id>

# Container inspect
docker inspect <container_id>
```

### Network Debugging

```bash
# Test connectivity
ping google.com

# DNS resolution
nslookup google.com
dig google.com

# Check open ports
ss -tuln
netstat -tuln

# Test connection to specific port
telnet localhost 5000
# or
nc -zv localhost 5000

# Trace network packets
tcpdump -i eth0 -A "tcp port 5000"
```

### System Resource Monitoring

```bash
# Real-time monitoring
top

# Better version with colors
htop

# Memory details
free -h

# Disk I/O
iostat -x 1

# Network stats
ifstat

# Process tree
pstree

# What's using the most resources
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

---

## Performance Issues

### Application Running Slow

```bash
# Check if CPU is maxed
top

# Check disk I/O
iostat -x

# Check network
iftop

# Check Flask app with profiler
# In app.py:
from werkzeug.middleware.profiler import ProfilerMiddleware
app = ProfilerMiddleware(app)
```

### Database Slow

```bash
# Check database connections
lsof -i :5432  # For PostgreSQL

# Check running queries (depends on DB)
psql -U postgres -c "SELECT * FROM pg_stat_activity"

# Check indices
psql -U postgres -c "\d+ your_table"

# Vacuum database (cleanup)
psql -U postgres -c "VACUUM"
```

---

## AWS-Specific Issues

### Cannot Connect to EC2

```bash
# 1. Check security group
aws ec2 describe-security-groups

# 2. Check instance is running
aws ec2 describe-instances

# 3. Check key pair
aws ec2 describe-key-pairs

# 4. Try connecting with full debugging
ssh -vvv -i key.pem ubuntu@IP
```

### Terraform State Issues

```bash
# View state
terraform state show

# List resources
terraform state list

# Remove resource from state (don't destroy actual resource)
terraform state rm aws_instance.web

# Back up state
cp terraform.tfstate terraform.tfstate.backup
```

---

## GCP-Specific Issues

### gcloud not configured

```bash
# Initialize
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID

# Authenticate
gcloud auth login

# Set default zone
gcloud config set compute/zone us-central1-a
```

### SSH to GCP instance

```bash
# Easier method
gcloud compute ssh instance-name

# Get external IP
gcloud compute instances list

# Manual SSH
ssh -i ~/.ssh/google_compute_engine user@EXTERNAL_IP
```

---

## Getting Help

1. **Check logs**: `docker-compose logs -f`
2. **Check status**: `docker-compose ps`
3. **Read error message carefully** - Python stack traces are usually helpful
4. **Google the error** - Most errors are common and have solutions
5. **Check documentation**:
   - Flask: https://flask.palletsprojects.com
   - Terraform: https://www.terraform.io/docs
   - Docker: https://docs.docker.com
5. **Ask in communities**:
   - Stack Overflow
   - GitHub issues
   - Reddit r/devops, r/sre

---

## Preventive Measures

### 1. Use `.env` Files

```bash
# Don't commit secrets!
echo ".env" >> .gitignore

# Create .env
cat > .env << EOF
DEBUG=True
DATABASE_URL=postgres://localhost/mydb
SECRET_KEY=your-secret-key
EOF

# Use in Python
from dotenv import load_dotenv
load_dotenv()
debug = os.getenv("DEBUG")
```

### 2. Validate Before Deploying

```bash
# Python syntax check
python3 -m py_compile backend/app.py

# Terraform plan (don't apply)
terraform plan -out=tfplan

# Docker build test
docker build -t test:latest backend/
docker run --rm test:latest

# Bash script syntax check
bash -n script.sh
```

### 3. Version Control Everything

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. Log Everything

```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Use it
logger.info("App started")
logger.error(f"Failed: {exception}")
```

---

**Still stuck?** Try these resources:
- Project README: [README.md](../README.md)
- Learning Path: [LEARNING_PATH.md](LEARNING_PATH.md)
- Check your specific technology guide (AWS_GUIDE.md, etc.)

**Remember**: Every error is a learning opportunity! 🚀
