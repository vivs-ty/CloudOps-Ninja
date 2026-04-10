# Deployment Strategy

This document outlines the deployment strategy for CloudOps Ninja across different environments and cloud providers.

## Overview

CloudOps Ninja uses a multi-stage deployment pipeline:

```
Code Push → Testing → Build → Plan → Deploy → Verify
   ↓         ↓        ↓      ↓      ↓       ↓
  main      pytest   Docker Terraform AWS/GCP Live
```

---

## Environments

### Development (Local)
- **Setup**: `docker-compose up -d`
- **Testing**: `pytest tests/ -v`
- **Access**: http://localhost:5000
- **Monitoring**: Prometheus (9090), Grafana (3000)

### Staging (Optional)
- **Infrastructure**: AWS/GCP (via Terraform)
- **Automation**: Manual triggers available
- **Purpose**: Pre-production testing

### Production (AWS/GCP)
- **Trigger**: Automatic on push to `main`
- **Rollback**: Manual via Terraform or Git revert
- **Monitoring**: CloudWatch/StackDriver + Prometheus

---

## Deployment Channels

### 1. Local Development
```bash
# Clone and setup
git clone https://github.com/vivs-ty/CloudOps-Ninja.git
cd CloudOps-Ninja

# Run with Docker Compose
docker-compose up -d

# Run tests
cd backend
pytest tests/ -v

# Verify
curl http://localhost:5000/api/status
```

### 2. Docker Container
```bash
# Build locally
docker build -t cloudops-ninja:latest backend/

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  cloudops-ninja:latest

# Test
curl http://localhost:5000/api/status
```

### 3. GitHub Container Registry
```bash
# Pull pre-built image
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:latest

# Run
docker run -p 5000:5000 ghcr.io/vivs-ty/CloudOps-Ninja/backend:latest
```

### 4. Cloud Deployment (AWS)
```bash
# Initialize infrastructure
cd infrastructure/aws
terraform init

# Plan changes
terraform plan

# Apply deployment
terraform apply

# Get outputs
terraform output
```

### 5. Cloud Deployment (GCP)
```bash
# Initialize infrastructure  
cd infrastructure/gcp
terraform init

# Plan changes
terraform plan

# Apply deployment
terraform apply

# Get outputs
terraform output
```

---

## Deployment Flow

### On Code Push to Main

1. **GitHub Actions Triggered**
   - Workflow: .github/workflows/deploy.yml
   - Event: push to main branch

2. **Validation & Testing (5 min)**
   - Install dependencies
   - Lint Python code
   - Run 22 pytest tests
   - Validate Terraform
   - Check documentation

3. **Docker Build (10 min)**
   - Build Docker image
   - Tag with version/branch
   - Push to ghcr.io
   - Cache layers

4. **Terraform Plan (5 min)**
   - Plan AWS infrastructure changes
   - Plan GCP infrastructure changes
   - Upload plans as artifacts

5. **Deploy to Infrastructure (10 min)**
   - Apply Terraform AWS changes (if credentials available)
   - Apply Terraform GCP changes (if credentials available)
   - Update cloud resources

6. **Report (2 min)**
   - Generate test summary
   - Post workflow summary
   - Update deployment status

---

## Rollback Strategy

### Automatic Rollback
If deployment fails:
1. Check error in GitHub Actions logs
2. Fix the issue
3. Push fix to main (triggers new deployment)

### Manual Rollback

**Using Git:**
```bash
# Revert last commit
git revert HEAD
git push origin main
# This triggers a new deployment with the reverted code
```

**Using Terraform:**
```bash
# Rollback to previous state
cd infrastructure/aws
terraform apply -var-file="previous.tfvars"
```

**Using Docker:**
```bash
# Deploy previous version
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:v1.0.0
docker run -p 5000:5000 ghcr.io/vivs-ty/CloudOps-Ninja/backend:v1.0.0
```

---

## Configuration

### Environment Variables

**Flask Application:**
```bash
FLASK_ENV=production          # Environment mode
FLASK_DEBUG=0                 # Disable debug
SECRET_KEY=<strong-key>       # Session key
DATABASE_URL=<db-connection>  # Database URL
PORT=5000                     # Application port
```

**Terraform (AWS):**
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
```

**Terraform (GCP):**
```bash
GCP_PROJECT_ID=<project-id>
GCP_CREDENTIALS=<service-account-json>
```

### Secrets Management

For GitHub Actions, add these secrets:
- Go to: Settings → Secrets and variables → Actions
- Add deployment credentials (see .github/workflows/README.md)

---

## Database Management

### Local Development
- SQLite database: `instance/cloudops.db`
- Auto-created on first run
- Data persists between restarts

### Production
- Consider migration to PostgreSQL/MySQL
- Store credentials in cloud secrets manager
- Enable automated backups
- Implement connection pooling

### Database Backup

```bash
# Before deployment
sqlite3 instance/cloudops.db ".dump" > backup.sql

# After deployment (if needed)
sqlite3 instance/cloudops.db < backup.sql
```

---

## Monitoring & Logging

### Application Logs
```bash
# View Flask logs
docker logs cloudops-ninja-app

# View GitHub Actions logs
# Dashboard → Actions → Workflow run
```

### Metrics Collection
- Prometheus endpoint: `/metrics`
- Metrics pushed to monitoring service
- Dashboard available via Grafana

### Health Checks
```bash
# API status endpoint
curl http://localhost:5000/api/status

# Docker health check
docker ps | grep cloudops-ninja-app
```

---

## Performance Optimization

### Caching
- Docker layer caching in GitHub Actions
- Terraform plan caching
- Python dependency caching

### Parallel Execution
- AWS and GCP Terraform plans run in parallel
- Multiple test suites run concurrently
- Docker build uses BuildKit

### Resource Limits
- GitHub Actions: 3 concurrent jobs (free tier)
- Docker build timeout: 15 minutes
- Terraform apply timeout: 30 minutes

---

## Disaster Recovery

### Backup Strategy
1. **Code**: Git repository (automatic)
2. **Database**: Daily SQLite dumps to cloud storage
3. **Infrastructure**: Terraform state in version control
4. **Configuration**: Secrets in GitHub Secrets

### Recovery Procedures

**Application Crash:**
```bash
# Restart container
docker restart cloudops-ninja-app

# Or redeploy
git push origin main  # Triggers CI/CD
```

**Database Corruption:**
```bash
# Restore from backup
sqlite3 instance/cloudops.db < backup.sql
docker restart cloudops-ninja-app
```

**Infrastructure Issues:**
```bash
# Redeploy infrastructure
cd infrastructure/aws
terraform apply
```

---

## Security Considerations

✅ **Implemented:**
- All secrets masked in logs
- Docker images use non-root user
- Terraform state secured
- GitHub Actions RBAC via environment

⚠️ **Recommended:**
- Enable HTTPS/TLS in production
- Implement rate limiting
- Use API keys for external access
- Enable audit logging
- Regular security scanning
- Update dependencies regularly

---

## Troubleshooting

### Deployment Fails at Testing
```bash
# Run tests locally
cd backend
pytest tests/ -v

# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip install -r requirements.txt
```

### Docker Build Fails
```bash
# Check Dockerfile
cat backend/Dockerfile

# Build locally
docker build -t test backend/

# Check logs for specific error
```

### Terraform Errors
```bash
# Validate configuration
terraform -chdir=infrastructure/aws validate

# Check credentials
echo $AWS_ACCESS_KEY_ID

# Review state
terraform state list
```

### Application Not Accessible
```bash
# Check if running
curl http://localhost:5000/health

# Check ports
netstat -an | grep 5000

# View logs
docker logs cloudops-ninja-app
```

---

## Next Steps

1. **Add SSL/TLS certificates** for HTTPS
2. **Set up monitoring dashboard** for production metrics
3. **Implement automated backups** to cloud storage
4. **Add deployment notifications** (Slack, email)
5. **Set up log aggregation** (CloudWatch, Stackdriver)
6. **Implement auto-scaling** for cloud deployments
7. **Add blue-green deployment** strategy
8. **Enable multi-region deployment**

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
