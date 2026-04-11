# Terraform Deployment Checklist

## Current Status
✅ **Configuration Status**: Valid and ready for deployment
- terraform init: SUCCESS
- terraform validate: SUCCESS
- terraform plan: Requires AWS credentials

## Prerequisites for Deployment

### 1. AWS Credentials
Set up AWS credentials using ONE of these methods:

**Option A: Environment Variables (Quick)**
```powershell
$env:AWS_ACCESS_KEY_ID = "your-access-key"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-key"
$env:AWS_DEFAULT_REGION = "us-east-1"
```

**Option B: AWS Profile**
```powershell
$env:AWS_PROFILE = "your-profile-name"
```

**Option C: AWS Credentials File**
Create `~/.aws/credentials` file or use AWS CLI:
```bash
aws configure
```

### 2. Configuration File
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings
```

### 3. Key Settings (terraform.tfvars)
- `aws_region`: AWS region (e.g., "us-east-1")
- `environment`: Environment name (e.g., "development")
- `instance_type`: EC2 instance type (e.g., "t2.micro" for free tier)
- `allowed_ssh_cidrs`: Your IP address for SSH access (e.g., "203.0.113.0/32")

## Deployment Steps

1. **Configure credentials** (see Prerequisites)

2. **Set up variables:**
   ```powershell
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars
   ```

3. **Review plan:**
   ```powershell
   terraform plan
   ```

4. **Deploy:**
   ```powershell
   terraform apply
   ```

5. **Get outputs:**
   ```powershell
   terraform output
   ```

## What Gets Deployed

### Resources (without Load Balancer)
- **VPC**: Virtual Private Cloud with 2 subnets
- **Internet Gateway**: For external connectivity
- **Route Tables**: For network routing
- **Security Group**: SSH, HTTP, HTTPS access
- **EC2 Instance**: Web server (t2.micro = free tier eligible)
- **Elastic IP**: Static public IP address
- **Network Interfaces**: VPC networking

### Resources (with Load Balancer)
Everything above PLUS:
- **Application Load Balancer**: Distributes traffic
- **Target Group**: For managing instances
- **Listener**: HTTP traffic handling

## Estimated Costs

### Free Tier (first 12 months)
- t2.micro EC2: FREE
- VPC/subnets: FREE
- Elastic IP: FREE (while in use)
- Data transfer: Limited FREE

**Total: ~$0/month** (if under free tier limits)

### Production (t3.small)
- t3.small EC2: ~$0.025/hour = ~$18/month
- Load Balancer: ~$16/month
- Data transfer: ~$0.02/GB
- Storage (20GB): ~$2/month

**Total: ~$36+/month**

## Deployment Time
- Plan: 10-15 seconds
- Apply: 2-3 minutes
- Destroy: 1-2 minutes

## Next Steps After Deployment

1. **Connect to instance:**
   ```bash
   ssh -i "your-key.pem" ubuntu@<IP_ADDRESS>
   ```

2. **Deploy Flask app:**
   ```bash
   git clone <repo> /app
   cd /app/backend
   pip install -r requirements.txt
   python app.py
   ```

3. **Check health:**
   ```bash
   curl http://<IP_ADDRESS>/api/health
   ```

4. **Enable load balancer (if needed):**
   ```powershell
   terraform apply -var="enable_load_balancer=true"
   ```

## Rollback
If something goes wrong:
```powershell
terraform destroy
```

This will delete all AWS resources.

## Troubleshooting

### "No valid credential sources found"
**Solution**: Set AWS credentials (see Prerequisites)

### "Error: resource already exists"
**Solution**: Check the resource doesn't already exist in AWS, or use terraform import

### "Timeout waiting for resource"
**Solution**: May be a security group rule issue; check AWS console firewall rules

## Support
- Full documentation: [infrastructure/aws/USAGE_GUIDE.md](USAGE_GUIDE.md)
- Module guide: [docs/TERRAFORM_MODULES.md](../../docs/TERRAFORM_MODULES.md)
- Terraform docs: https://www.terraform.io/docs

## Important: Free Tier Warning ⚠️
After 12 months, t2.micro becomes ~$10/month. Consider:
- Shutting down unused resources
- Using spot instances for dev environments
- Setting up cost alerts in AWS
