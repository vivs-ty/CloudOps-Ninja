# AWS Setup Guide

> **Note**: This guide assumes you have an AWS account. Sign up at https://aws.amazon.com (free tier available!)

## Step 1: Create an AWS Account

1. Visit [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Fill in your information
4. Choose **Free Tier** to avoid charges
5. Verify your email and payment method

## Step 2: Create an IAM User

❌ **DO NOT use ROOT account** - it's less secure!

1. Go to [IAM Console](https://console.aws.amazon.com/iam)
2. Click "Users" → "Create user"
3. Name: `cloudops-user`
4. Attach policy: `AdministratorAccess` (for learning only!)
5. Create access key (save the CSV!)

### Save Your Credentials Securely!
```
Access Key ID:     AKIA...
Secret Access Key: ABCDef...
```

⚠️ **NEVER share these! Keep them private!**

## Step 3: Install AWS CLI

```bash
# Install
pip3 install awscli

# Verify
aws --version

# Configure (use credentials from Step 2)
aws configure

# You'll be prompted:
# AWS Access Key ID: [paste from CSV]
# AWS Secret Access Key: [paste from CSV]
# Default region name: us-east-1
# Default output format: json
```

Test it works:
```bash
aws ec2 describe-instances
# Should return something (empty list if no instances yet)
```

## Step 4: Create SSH Key Pair

```bash
# Create key pair in AWS
aws ec2 create-key-pair --key-name cloudops-key --query 'KeyMaterial' --output text > ~/.ssh/cloudops-key.pem

# Set permissions
chmod 400 ~/.ssh/cloudops-key.pem

# Test
ls -la ~/.ssh/cloudops-key.pem
```

## Step 5: Deploy with Terraform

```bash
# Navigate to infrastructure
cd infrastructure/aws

# Initialize (downloads Terraform plugins)
terraform init

# See what will be created
terraform plan

# If everything looks good:
terraform apply

# You'll be prompted - type: yes
```

After deployment, Terraform will output:
```
Outputs:

instance_public_ip = "54.123.45.67"
instance_public_dns = "ec2-54-123-45-67.compute-1.amazonaws.com"
```

## Step 6: Connect to Your Instance

```bash
# SSH into the instance
ssh -i ~/.ssh/cloudops-key.pem ubuntu@54.123.45.67

# Or use the DNS name
ssh -i ~/.ssh/cloudops-key.pem ubuntu@ec2-54-123-45-67.compute-1.amazonaws.com

# You're now on the AWS server!
```

Once connected, you can:
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip -y

# Clone your project
git clone <YOUR_REPO_URL>

# Install dependencies
cd CloudOps-Ninja/backend
pip3 install -r requirements.txt

# Run the app
python3 app.py
```

Then from your local machine:
```bash
# Access your app!
curl http://54.123.45.67:5000/api/status

# Or in browser
open http://54.123.45.67:5000
```

## Step 7: Monitor Costs

AWS Free Tier is free for 12 months, but you should still monitor:

```bash
# Check current month's costs
aws ce list-cost-allocation-tags

# Or view in console
# https://console.aws.amazon.com/cost-management/home
```

## Common AWS Resources You'll Use

### EC2 - Virtual Machines
```bash
# List instances
aws ec2 describe-instances

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Terminate (DELETE!) instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### Security Groups - Firewall Rules
```bash
# Authorize incoming traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --port 5000 \
  --protocol tcp \
  --cidr 0.0.0.0/0
```

### Elastic IP - Static IPs
```bash
# Allocate
aws ec2 allocate-address

# Associate with instance
aws ec2 associate-address --instance-id i-1234567890abcdef0 --allocation-id eipalloc-12345678
```

## Cleanup - Don't Forget!

❌ **Important**: Free Tier is free but ONLY if you clean up!

```bash
# Destroy everything Terraform created
cd infrastructure/aws
terraform destroy

# Type: yes when prompted

# Stop any remaining instances
aws ec2 stop-instances --instance-ids <INSTANCE_ID>

# Delete key pair
aws ec2 delete-key-pair --key-name cloudops-key
```

## Troubleshooting

### Cannot connect via SSH
- Check security group allows SSH (port 22)
- Check you're using correct key file
- Check instance is running: `aws ec2 describe-instances`

### Terraform apply fails
- Check AWS credentials: `aws sts get-caller-identity`
- Check region is set: `echo $AWS_DEFAULT_REGION`
- Check you have permissions

### Instance is running but app won't start
```bash
# SSH into instance
ssh -i ~/.ssh/cloudops-key.pem ubuntu@IP

# Install Python & dependencies
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Try running app
python3 app.py

# Check logs
tail -f nohup.out
```

## Next Steps

1. ✅ Deploy to AWS (you just did!)
2. Deploy to GCP (see GCP_GUIDE.md)
3. Set up monitoring (docs/SRE_CONCEPTS.md)
4. Automate deployments (GitHub Actions)
5. Practice incident response

## Resources

- AWS Documentation: https://docs.aws.amazon.com/
- Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/latest
- AWS CLI Reference: https://docs.aws.amazon.com/cli/latest/reference/
- AWS Free Tier: https://aws.amazon.com/free/

---

**Congratulations! You're now in the cloud! 🎉**

Next: Deploy to GCP and compare!
