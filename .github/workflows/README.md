# CloudOps Ninja - CI/CD Pipeline

This directory contains GitHub Actions workflows for automated testing, building, and deployment of the CloudOps Ninja project.

## Workflows

### 1. Deploy CloudOps Ninja (`deploy.yml`)

The main CI/CD pipeline that runs on every push to main and pull requests. It consists of 5 stages:

#### **Stage 1: Validate & Test** 
- ✅ Python dependency installation  
- ✅ Python syntax linting
- ✅ Automated test suite (pytest) with 22 tests
- ✅ Terraform configuration validation
- ✅ Documentation link verification

**Triggers on:** Every push to main, every PR, and tags matching `v*`

#### **Stage 2: Build Docker Image**
- 🐳 Build containerized Flask application
- 🏷️ Tag with branch, semantic version, and commit SHA
- 📤 Push to GitHub Container Registry (`ghcr.io`)
- 💾 Cache Docker layers for faster rebuilds

**Pushes only on:** Pushes to main (PRs build without pushing)

#### **Stage 3: Terraform Plan (Preview)**
- 📋 Initialize Terraform for AWS and GCP
- 📊 Generate infrastructure change plans
- 💾 Artifacts uploaded for review

**Runs on:** All pushes to main and PRs (non-blocking)

#### **Stage 4: Deploy to AWS/GCP**
- 🚀 Applies Terraform changes to AWS infrastructure
- 🌍 Applies Terraform changes to GCP infrastructure  
- 🔐 Requires AWS and GCP credentials in secrets
- ⚠️ Runs only on direct pushes to main (not PRs)

**Requirements:**
- `AWS_ACCESS_KEY_ID` secret
- `AWS_SECRET_ACCESS_KEY` secret
- `GCP_PROJECT_ID` secret
- `GCP_CREDENTIALS` secret (JSON key file)

#### **Stage 5: Generate Report**
- 📊 Downloads and summarizes test results
- 📝 Posts summary to GitHub Actions workflow summary
- 📚 Provides deployment guidelines

---

## Setup Instructions

### 1. Enable GitHub Actions
Workflows are automatically enabled for public repositories. For private repos, enable via:
- Repository Settings → Actions → General → Allow actions

### 2. Add Deployment Secrets (Optional)
For automated deployment to AWS/GCP, add these secrets:
- Go to: Settings → Secrets and variables → Actions
- Add:
  - `AWS_ACCESS_KEY_ID`: Your AWS access key
  - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
  - `GCP_PROJECT_ID`: Your GCP project ID
  - `GCP_CREDENTIALS`: GCP service account JSON key content

### 3. Docker Registry Credentials (Optional)
GitHub Container Registry (`ghcr.io`) uses `GITHUB_TOKEN` automatically. No setup needed!

---

## Running Workflows

### Manual Trigger (if configured)
```bash
# Trigger deployment from the web UI
# Repository → Actions → Deploy CloudOps Ninja → Run workflow
```

### Automatic Triggers
| Event | Condition | Stages Run |
|-------|-----------|-----------|
| Push to main | Any | All (1-5) |
| Pull Request | To main | Testing only (1-3) |
| Tag push | `v*` pattern | All (1-5) |

---

## Artifacts

The pipeline generates and stores artifacts:

- **test-results**: JUnit XML test report (retention: 5 days)
- **tfplan-aws**: Terraform plan for AWS (retention: 5 days)
- **tfplan-gcp**: Terraform plan for GCP (retention: 5 days)

Access via: Actions → Workflow run → Artifacts

---

## Docker Images

Built images are available at:
```bash
# Latest version
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:latest

# By branch
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:main

# By semantic version (v1.2.3)
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:v1.2.3

# By commit SHA
docker pull ghcr.io/vivs-ty/CloudOps-Ninja/backend:main-abc1234
```

---

## Monitoring & Debugging

### View Workflow Runs
- Repository → Actions → Select workflow

### View Logs
Click on a workflow run to see detailed logs for each job and step.

### Common Issues

**Tests failing:**
- Check test logs: Actions → Workflow → validate-and-test job
- Run tests locally: `cd backend && pytest tests/ -v`

**Docker build failing:**
- Verify Dockerfile: `backend/Dockerfile`
- Check Docker build context

**Terraform errors:**
- Validate locally: `terraform -chdir=infrastructure/aws validate`
- Check secret credentials are correctly set

**Deployment not running:**
- Ensure you pushed to `main` branch (not pull request)
- Check environment is set to `production`
- Verify AWS/GCP credentials are in repository secrets

---

## Security Best Practices

✅ **Implemented:**
- Secrets are masked in logs
- Docker images signed and verified
- Terraform state recommendations in comments
- Separate test and production environments

⚠️ **Recommended for Production:**
- Use branch protection rules
- Require approval before deployment steps
- Implement Snyk or similar for security scanning
- Store Terraform state in remote backend (S3/GCS)
- Enable audit logging for all deployments

---

## Customization

To modify the pipeline:

1. Edit `.github/workflows/deploy.yml`
2. Common customizations:
   - Change Python version: `python-version: '3.12'`
   - Add more test commands in validate-and-test job
   - Modify Docker image registry/names in env section
   - Add notification steps (Slack, email, etc.)
   - Adjust retention periods for artifacts

---

## Performance Tips

- Cache dependencies between runs
- Use workflow concurrency to avoid redundant runs
- Clean up old artifacts regularly
- Use self-hosted runners for faster Docker builds (future enhancement)

---

## Support

For issues or questions about CI/CD:
- Check GitHub Actions logs for error messages
- Review this documentation
- Check repository issues for similar problems
- Consult GitHub Actions documentation: https://docs.github.com/en/actions
