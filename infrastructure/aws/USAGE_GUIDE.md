# Using Terraform Modules - Quick Guide

## Overview

CloudOps Ninja AWS infrastructure is now built with reusable Terraform modules. This guide shows you how to use them.

## Directory Structure

```
infrastructure/
├── modules/           # Reusable modules
│   ├── vpc/
│   ├── security_group/
│   ├── ec2/
│   ├── elastic_ip/
│   ├── load_balancer/
│   └── README.md
├── aws/               # Main configuration
│   ├── main.tf        # Uses modules
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
└── gcp/               # GCP configuration
```

## Quick Start

### 1. Initialize

```bash
cd infrastructure/aws
terraform init
```

This will download the AWS provider and initialize modules.

### 2. Configure Variables

```bash
# Copy example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your settings
vim terraform.tfvars
```

### 3. Plan

```bash
terraform plan
```

This shows what infrastructure will be created/modified.

### 4. Apply

```bash
terraform apply
```

Type `yes` when prompted to create infrastructure.

### 5. View Outputs

```bash
terraform output
```

Shows important information like:
- Instance public IP
- Web URL
- SSH connection command

## Configuration Examples

### Minimal Configuration (Free Tier)

**terraform.tfvars:**
```hcl
aws_region = "us-east-1"
instance_type = "t2.micro"
```

### Production Configuration

**terraform.tfvars:**
```hcl
aws_region = "us-east-1"
environment = "production"
instance_type = "t3.small"
enable_load_balancer = true

# Restrict SSH access
allowed_ssh_cidrs = ["203.0.113.0/24"]

# Multiple subnets for high availability
subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]
```

### High Security Configuration

**terraform.tfvars:**
```hcl
aws_region = "us-west-2"
environment = "prod-secure"
instance_type = "t3.medium"

# Restrict to your IP only
allowed_ssh_cidrs = ["YOUR.IP.ADDRESS/32"]

# Restrict application access
allowed_app_cidrs = ["10.0.0.0/8"]  # Internal only

# Enable load balancer for distribution
enable_load_balancer = true
```

## Using Individual Modules

You can use modules independently:

### Just VPC

```hcl
module "my_vpc" {
  source = "../modules/vpc"
  
  vpc_cidr       = "192.168.0.0/16"
  subnet_cidrs   = ["192.168.1.0/24"]
  project_name   = "custom-project"
}

output "vpc_id" {
  value = module.my_vpc.vpc_id
}
```

### VPC + Security Group

```hcl
module "vpc" {
  source = "../modules/vpc"
}

module "sg" {
  source = "../modules/security_group"
  
  vpc_id = module.vpc.vpc_id
  enable_https = true
}

output "security_group_id" {
  value = module.sg.security_group_id
}
```

### Full Stack

The default `infrastructure/aws/main.tf` includes all modules:
- VPC with subnets
- Security groups
- EC2 instance
- Elastic IP
- Optional: Load Balancer

## Common Commands

### View Current Infrastructure

```bash
terraform state list
```

### Show Resource Details

```bash
terraform state show 'module.vpc.aws_vpc.main'
```

### Destroy Infrastructure

```bash
# Preview what will be destroyed
terraform destroy -auto-approve

# Safer: review first
terraform plan -destroy
terraform destroy
```

### Format Code

```bash
terraform fmt -recursive
```

### Validate Configuration

```bash
terraform validate
```

### View Outputs

```bash
terraform output
terraform output vpc_id
terraform output web_url
```

## Module Variables Reference

### VPC Module

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| vpc_cidr | string | "10.0.0.0/16" | VPC CIDR block |
| subnet_cidrs | list | ["10.0.1.0/24", "10.0.2.0/24"] | Subnet CIDRs |
| availability_zones | list | ["us-east-1a", "us-east-1b"] | Availability zones |
| environment | string | "development" | Environment name |
| project_name | string | "cloudops" | Project name |

### Security Group Module

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| vpc_id | string | - | VPC ID (required) |
| security_group_name | string | "web-sg" | SG name |
| allowed_ssh_cidrs | list | ["0.0.0.0/0"] | SSH allowed CIDRs |
| allow_http | bool | true | Enable HTTP |
| allow_https | bool | true | Enable HTTPS |
| enable_app_port | bool | true | Enable port 5000 |

### EC2 Module

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| subnet_id | string | - | Subnet ID (required) |
| security_group_ids | list | - | Security groups (required) |
| instance_type | string | "t2.micro" | Instance type |
| instance_name | string | "web-server" | Instance name |
| user_data | string | "" | Startup script |
| root_volume_size | number | 20 | Root volume GB |

### Elastic IP Module

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| instance_id | string | - | Instance ID (required) |
| vpc_id | string | - | VPC ID (required) |
| eip_name | string | "eip" | EIP name |

### Load Balancer Module

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| vpc_id | string | - | VPC ID (required) |
| subnet_ids | list | - | Subnet IDs (required) |
| security_group_ids | list | - | Security groups (required) |
| alb_name | string | "alb" | ALB name |
| enable_deletion_protection | bool | false | Deletion protection |
| idle_timeout | number | 60 | Idle timeout seconds |

## Troubleshooting

### Module not found

```
Error: module not found
```

**Solution:** Check relative paths in configuration.

### Invalid variable type

```
Error: Incorrect attribute value type
```

**Solution:** Verify variable types (list vs string, etc.)

### Authentication failed

```
Error: error configuring Terraform AWS Provider
```

**Solution:** Configure AWS credentials:
```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"

# Option 2: AWS profile
export AWS_PROFILE="your-profile"

# Option 3: AWS credentials file
# ~/.aws/credentials
```

### State lock error

```
Error: Error acquiring the state lock
```

**Solution:** 
```bash
terraform force-unlock LOCK_ID
```

## Next Steps

1. **Deploy infrastructure:**
   ```bash
   terraform apply
   ```

2. **Connect to instance:**
   ```bash
   ssh -i <your-key.pem> ubuntu@<IP_ADDRESS>
   ```

3. **Access web server:**
   ```bash
   curl http://<IP_ADDRESS>
   ```

4. **Enable load balancer:**
   ```bash
   terraform apply -var="enable_load_balancer=true"
   ```

## Documentation

- [Full Module Documentation](../../docs/TERRAFORM_MODULES.md)
- [AWS Guide](../../docs/AWS_GUIDE.md)
- [Terraform Official Docs](https://www.terraform.io/docs)

## Best Practices

✅ **Do:**
- Use terraform.tfvars for configuration
- Store state in version control (*.tfstate)
- Restrict SSH access in security groups
- Use meaningful variable values
- Document custom configurations

❌ **Don't:**
- Hard-code sensitive values
- Commit AWS credentials
- Ignore terraform.tfvars.example
- Use 0.0.0.0/0 for SSH in production
- Skip terraform plan review

## Support

For issues:
1. Check variable names match documentation
2. Run `terraform validate`
3. Review `terraform plan` output
4. Check module documentation in `infrastructure/modules/*/main.tf`
