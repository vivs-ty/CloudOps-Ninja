# CloudOps Projects - Learn by Building 🏗️

This directory contains hands-on projects to practice DevOps/SRE concepts across AWS, GCP, and hybrid setups.

## Project Progression

```
Beginner (Week 1-2)
├── P1: Hello World Deployment
├── P2: Multi-Region Awareness
└── P3: Basic Monitoring

Intermediate (Week 3-4)
├── P4: Auto-Scaling Setup
├── P5: Database Integration
└── P6: CI/CD Pipeline

Advanced (Week 5+)
├── P7: Multi-Cloud Replication
├── P8: Disaster Recovery
└── P9: Chaos Engineering
```

## Project 1: Hello World Deployment 🌍

**Difficulty**: ⭐ Easy | **Time**: 2 hours | **Skills**: Cloud basics, Compute

### Objective
Deploy the CloudOps Ninja Flask app to AWS and GCP

### What You'll Learn
- Creating compute instances
- Assigning IP addresses
- Basic networking
- SSH access

### Steps

**AWS:**
```bash
cd infrastructure/aws
terraform apply
# Get the instance IP from outputs
ssh -i ~/.ssh/cloudops-key.pem ubuntu@INSTANCE_IP
```

**GCP:**
```bash
cd infrastructure/gcp
terraform apply
gcloud compute ssh cloudops-web --zone=us-central1-a
```

### Success Criteria
- [ ] Instance running in AWS
- [ ] Instance running in GCP
- [ ] Both accessible via SSH
- [ ] App running on both (python3 app.py)
- [ ] Can access via browser

---

## Project 2: Multi-Region Awareness 🌐

**Difficulty**: ⭐⭐ Intermediate | **Time**: 4 hours | **Skills**: Multi-region, Load balancing

### Objective
Deploy app in multiple regions with health awareness

### What You'll Learn
- Multi-region deployment
- Health checks
- Traffic routing
- Cross-region communication

### Architecture
```
┌──────────────────┐
│  Global Load     │
│   Balancer       │
└────────┬─────────┘
    ┌────┴────┐
    ↓         ↓
 US-East   EU-West
  (AWS)      (GCP)
```

### Steps

1. **Deploy to us-east-1 (AWS)**
```bash
aws ec2 run-instances \
  --image-id ami-0d527b8c289b4af7f \
  --instance-type t2.micro \
  --region us-east-1
```

2. **Deploy to europe-west1 (GCP)**
```bash
gcloud compute instances create cloudops-eu \
  --zone=europe-west1-b \
  --region=europe-west1
```

3. **Configure health checks**
```bash
# Both should respond to:
curl http://INSTANCE_IP/health
```

4. **Add to load balancer** (use cloud provider's LB)

---

## Project 3: Basic Monitoring & Alerts 📊

**Difficulty**: ⭐⭐ Intermediate | **Time**: 3 hours | **Skills**: Monitoring, Alerting

### Objective
Set up Prometheus + Grafana to monitor both deployments

### What You'll Learn
- Metrics collection
- Dashboard creation
- Alert rules
- Notification setup

### Setup

```bash
# Prometheus monitors both:
# - AWS instance metrics
# - GCP instance metrics
# - Flask app endpoints

# Grafana displays:
# - CPU usage per region
# - HTTP request rates
# - Error rates
# - Custom business metrics
```

### Alerts to Create
- [ ] High CPU (> 80%)
- [ ] High memory (> 80%)
- [ ] High error rate (> 1%)
- [ ] Service down (no response)

---

## Project 4: Auto-Scaling Setup 📈

**Difficulty**: ⭐⭐⭐ Advanced | **Time**: 4-5 hours | **Skills**: Auto-scaling, Load testing

### Objective
Set up auto-scaling groups that respond to load

### Metrics to Scale On
- [ ] CPU utilization
- [ ] Memory usage
- [ ] Request count
- [ ] Custom metrics

### Load Testing

```bash
# Generate load to trigger scaling
ab -n 10000 -c 100 http://your-instance/api/status

# Or use:
wrk -t4 -c100 -d30s http://your-instance/
```

### Success Criteria
- [ ] New instance created on high load
- [ ] Instance terminated when load drops
- [ ] Minimum 2 instances running
- [ ] Maximum 4 instances (cost control)

---

## Project 5: Database Integration 🗄️

**Difficulty**: ⭐⭐ Intermediate | **Time**: 3 hours | **Skills**: Databases, Migrations

### Objective
Add persistent data layer (AWS RDS + GCP Cloud SQL)

### Components

**AWS** → PostgreSQL RDS
```bash
aws rds create-db-instance \
  --db-instance-identifier cloudops-db \
  --engine postgres \
  --db-instance-class db.t2.micro
```

**GCP** → Cloud SQL
```bash
gcloud sql instances create cloudops-db \
  --database-version=POSTGRES_12 \
  --tier=db-f1-micro
```

### Application Updates
- [ ] Update Flask app to use database
- [ ] Create migrations
- [ ] Set up connection pooling
- [ ] Add database backups

---

## Project 6: CI/CD Pipeline 🔄

**Difficulty**: ⭐⭐⭐ Advanced | **Time**: 5-6 hours | **Skills**: CI/CD, GitHub Actions, Testing

### Objective
Automated testing and deployment on every push

### Pipeline Stages

1. **Test** - Run unit tests
2. **Build** - Create Docker image
3. **Push** - Upload to registries
4. **Deploy** - Update cloud instances
5. **Monitor** - Check health

### GitHub Actions Setup

```yaml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test
        run: make test
      - name: Build
        run: make build
      - name: Deploy
        run: make deploy
```

---

## Project 7: Multi-Cloud Replication 🔁

**Difficulty**: ⭐⭐⭐ Advanced | **Time**: 5-6 hours | **Skills**: Replication, Consistency

### Objective
Keep data synchronized across AWS and GCP

### Architecture
```
App in AWS
    ↓
  RDS
    ↓
Database Replication
    ↓
Cloud SQL in GCP
    ↓
App in GCP
```

### Implementation
- [ ] Set up database replication streams
- [ ] Monitor replication lag
- [ ] Test failover
- [ ] Implement conflict resolution

---

## Project 8: Disaster Recovery Plan 🚨

**Difficulty**: ⭐⭐⭐⭐ Hard | **Time**: 6-8 hours | **Skills**: DR, RTO/RPO

### Objective
Design and implement recovery procedures

### Scenarios to Handle
- [ ] Region outage (entire region down)
- [ ] Instance failure (single instance down)
- [ ] Database corruption (restore from backup)
- [ ] Network partition (cross-region split)

### Recovery Targets
- **RTO** (Recovery Time): Max 15 minutes
- **RPO** (Recovery Point): Max 5 minutes of data loss

### Testing
- [ ] Scheduled failover drills monthly
- [ ] Document procedures
- [ ] Time all recovery steps

---

## Project 9: Chaos Engineering Experiments 💣

**Difficulty**: ⭐⭐⭐⭐ Hard | **Time**: 4-5 hours per experiment | **Skills**: Resilience, Debugging

### Experiments to Run

**Experiment 1: Instance Failure**
```bash
# Terminate a running instance
aws ec2 terminate-instances --instance-ids i-xxx

# Measure:
# - Time to detect failure
# - Time to auto-recover
# - Impact on users
```

**Experiment 2: Network Latency**
```bash
# Introduce 500ms latency
tc qdisc add dev eth0 root netem delay 500ms

# Measure impact on:
# - User experience
# - Error rates
# - Application behavior
```

**Experiment 3: High Memory Usage**
```bash
# Consume memory
stress-ng --vm 1 --vm-bytes 80% --timeout 300s

# Measure:
# - Triggering of alerts
# - Auto-scaling response
# - Performance degradation
```

**Experiment 4: Persistent Disk Failure**
```bash
# Simulate disk errors
# Test backup/restore procedures
# Verify data integrity
```

---

## Bonus: Build Your Own Project! 🎨

Use this template:

```markdown
# Project: [Your Idea]

## Difficulty: ⭐ to ⭐⭐⭐⭐
## Time: X hours
## Skills: [List 3-5 skills you'll use]

## Objective
[What is the goal?]

## What You'll Learn
- [Skill 1]
- [Skill 2]
- [Skill 3]

## Architecture
[Diagram or description]

## Steps
1. [Step 1]
2. [Step 2]
...

## Success Criteria
- [ ] Done
- [ ] Working
- [ ] Tested
```

---

## Resources

- AWS Documentation: https://docs.aws.amazon.com/
- GCP Documentation: https://cloud.google.com/docs
- Terraform: https://www.terraform.io/
- Docker: https://docs.docker.com/
- Kubernetes: https://kubernetes.io/docs/

---

**Happy building! 🚀**
