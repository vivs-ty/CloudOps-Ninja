# GCP Zero to Hero - Complete Setup Guide

> **Note**: This guide assumes you have a GCP account. Sign up at https://cloud.google.com/free (get $300 free credits!)

## Step 1: Create a GCP Account

1. Visit [cloud.google.com/free](https://cloud.google.com/free)
2. Click "Start free"
3. Fill in your information
4. Verify your email and payment method
5. **Get $300 credits for 90 days!**

## Step 2: Create a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the project dropdown (top-left)
3. Click "New Project"
4. Name: `cloudops-ninja`
5. Click "Create"

## Step 3: Enable Required APIs

```bash
# Install Google Cloud SDK
# macOS:
brew install --cask google-cloud-sdk

# Or follow: https://cloud.google.com/sdk/docs/install

# Initialize
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable cloudsql.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable cloudrun.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Step 4: Create Service Account for Terraform

```bash
# Create service account
gcloud iam service-accounts create cloudops-sa \
  --display-name="CloudOps Ninja Service Account"

# Grant roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:cloudops-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/editor"

# Create key
gcloud iam service-accounts keys create ~/.gcp/cloudops-key.json \
  --iam-account=cloudops-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/cloudops-key.json"
```

## Step 5: Deploy with Terraform

```bash
# Navigate to infrastructure
cd infrastructure/gcp

# Create terraform.tfvars
cat > terraform.tfvars << EOF
project_id = "YOUR_PROJECT_ID"
region      = "us-central1"
zone        = "us-central1-a"
EOF

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply
```

After deployment, outputs will show:
```
instance_external_ip = "35.xxx.xxx.xxx"
```

## Step 6: Connect to Your Instance

```bash
# SSH into the instance
gcloud compute ssh cloudops-web --zone=us-central1-a

# Or manually
ssh -i ~/.ssh/google_compute_engine user@35.xxx.xxx.xxx
```

Once connected:
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip docker.io -y

# Clone and deploy
git clone <YOUR_REPO_URL>
cd CloudOps-Ninja/backend
pip3 install -r requirements.txt
python3 app.py
```

## GCP Key Services

### Compute Engine
```bash
# List instances
gcloud compute instances list

# Create instance
gcloud compute instances create my-instance \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-micro \
  --zone=us-central1-a

# Delete instance
gcloud compute instances delete my-instance --zone=us-central1-a
```

### Cloud Storage (GCS)
```bash
# Create bucket
gsutil mb gs://cloudops-ninja-bucket/

# Upload file
gsutil cp file.txt gs://cloudops-ninja-bucket/

# Download file
gsutil cp gs://cloudops-ninja-bucket/file.txt .

# Delete bucket
gsutil -m rm -r gs://cloudops-ninja-bucket/
```

### Cloud SQL
```bash
# Create instance
gcloud sql instances create cloudops-db \
  --database-version=POSTGRES_12 \
  --tier=db-f1-micro \
  --region=us-central1

# Connect
gcloud sql connect cloudops-db --user=postgres

# Backup
gcloud sql backups create --instance=cloudops-db

# Delete
gcloud sql instances delete cloudops-db
```

### Cloud Run (Serverless)
```bash
# Deploy Flask app to Cloud Run
gcloud run deploy cloudops-ninja \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# View logs
gcloud run services describe cloudops-ninja --platform managed --region us-central1

# Delete
gcloud run services delete cloudops-ninja --platform managed --region us-central1
```

### Cloud Build (CI/CD)
```bash
# Create cloudbuild.yaml
cat > cloudbuild.yaml << 'EOF'
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/cloudops:latest', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/cloudops:latest']
  
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - 'run'
      - '--filename=.'
      - '--image=gcr.io/$PROJECT_ID/cloudops:latest'
      - '--location=us-central1'
      - '--cluster=cloudops-cluster'
EOF

# Submit build
gcloud builds submit
```

## GCP vs AWS Comparison

| Feature | GCP | AWS |
|---------|-----|-----|
| **Compute** | Compute Engine | EC2 |
| **Storage** | Cloud Storage | S3 |
| **Database** | Cloud SQL | RDS |
| **Kubernetes** | GKE | EKS |
| **Serverless** | Cloud Run | Lambda |
| **CI/CD** | Cloud Build | CodePipeline |
| **Pricing** | Per-minute (better for short tasks) | Per-hour |
| **Free Tier** | $300 for 90 days | 12 months free |

## GCP Best Practices

### 1. Use Managed Services
```
❌ Don't: Manage your own Kubernetes cluster
✅ Do: Use GKE with auto-scaling
```

### 2. Enable VPC Service Controls
```bash
# Secure your resources
gcloud access-context-manager policies create \
  --display-name="cloudops-policy"
```

### 3. Use IAM Properly
```bash
# Don't grant Editor to service accounts
# Use least-privilege principle
gcloud iam roles create custom-cloudops-role \
  --title="CloudOps Role" \
  --permissions=compute.instances.get,compute.instances.list
```

### 4. Monitor Costs
```bash
# Setup budget alerts
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --display-name="CloudOps Budget" \
  --budget-amount=50
```

### 5. Use Cloud Monitoring
```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com

# Create policy
gcloud alpha monitoring policies create
```

## Cleanup - Don't Forget!

**Important**: Free trial credits expire after 90 days!

```bash
# List all resources
gcloud compute instances list
gsutil ls
gcloud sql instances list

# Delete everything
gcloud compute instances delete $(gcloud compute instances list --format='value(name)')
gsutil -m rm -r gs://cloudops-ninja-bucket/
gcloud sql instances delete cloudops-db

# Clean up Terraform
cd infrastructure/gcp
terraform destroy
```

## Learning Projects

### Project 1: Basic Web App Deployment
**Time**: 1-2 hours

1. Create Compute Engine instance
2. Install Docker
3. Deploy Flask app
4. Assign Static IP
5. Access via browser

```bash
# Quick deployment
gcloud compute instances create cloudops-web \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-micro \
  --zone=us-central1-a \
  --metadata startup-script='#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip docker.io
git clone <REPO_URL>
cd CloudOps-Ninja/backend
pip3 install -r requirements.txt
python3 app.py'
```

### Project 2: Multi-Region Deployment
**Time**: 3-4 hours

1. Deploy in us-central1
2. Deploy in europe-west1
3. Set up Cloud Load Balancing
4. Test failover

```bash
# Create load balancer
gcloud compute backend-services create cloudops-backend \
  --global \
  --protocol=HTTP

gcloud compute url-maps create cloudops-lb \
  --default-service=cloudops-backend

gcloud compute target-http-proxies create cloudops-proxy \
  --url-map=cloudops-lb

gcloud compute forwarding-rules create cloudops-fw \
  --global \
  --target-http-proxy=cloudops-proxy \
  --address=cloudops-ip \
  --ports=80
```

### Project 3: Containerized App on Cloud Run
**Time**: 2-3 hours

1. Create Dockerfile (already done!)
2. Push to Container Registry
3. Deploy to Cloud Run
4. Set up CI/CD with Cloud Build

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cloudops-ninja

# Deploy to Cloud Run
gcloud run deploy cloudops-ninja \
  --image gcr.io/YOUR_PROJECT_ID/cloudops-ninja \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --allow-unauthenticated
```

### Project 4: Database with Cloud SQL
**Time**: 2-3 hours

1. Create Cloud SQL instance
2. Create database and tables
3. Connect from Compute Engine
4. Set up daily backups

```bash
# Create database
gcloud sql instances create cloudops-db \
  --database-version=POSTGRES_12 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --backup-start-time=03:00

# Create database
gcloud sql databases create cloudops \
  --instance=cloudops-db

# Connect and load data
gcloud sql connect cloudops-db --user=postgres
```

### Project 5: Monitoring & Logging
**Time**: 2-3 hours

1. Enable Cloud Logging
2. Create custom metrics
3. Set up alerts
4. Build dashboards

```bash
# Create log sink
gcloud logging create-sink cloudops-sink \
  storage.googleapis.com/cloudops-logs

# Create metric
gcloud logging metrics create app_errors \
  --description="Count of app errors" \
  --log-filter='severity="ERROR"'
```

## Resources

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest)
- [Google Cloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [GCP Free Tier](https://cloud.google.com/free/docs/gcp-free-tier)
- [Cloud Skills Boost](https://www.cloudskillsboost.google/) - Free training

## Troubleshooting

### API not enabled
```bash
gcloud services enable REQUIRED_API
```

### Permission denied
```bash
# Check IAM
gcloud iam service-accounts list

# Grant role to user
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member=user:EMAIL \
  --role=roles/editor
```

### Quota exceeded
Check quotas in Console: IAM & Admin → Quotas

### High costs
- Check: Billing → Reports
- Set budget alerts
- Use committed-use discounts
- Delete unused resources

---

**Congratulations! You're now a GCP user! 🎉**

Next: Deploy to both AWS and GCP simultaneously!
