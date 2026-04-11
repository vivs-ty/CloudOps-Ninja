# Terraform Modules Documentation

## Overview

CloudOps Ninja now uses reusable Terraform modules to manage AWS infrastructure components. This modular approach allows you to:

- **Reuse** infrastructure configurations across projects
- **Maintain** consistent infrastructure standards
- **Scale** easier with proven, tested components
- **Learn** Terraform best practices for module design

## Module Structure

```
infrastructure/
├── modules/
│   ├── vpc/
│   │   └── main.tf              # VPC, subnets, internet gateway, route tables
│   ├── security_group/
│   │   └── main.tf              # Security groups with configurable rules
│   ├── ec2/
│   │   └── main.tf              # EC2 instances with customizable settings
│   ├── elastic_ip/
│   │   └── main.tf              # Elastic IPs for static addresses
│   └── load_balancer/
│       └── main.tf              # Application Load Balancer with target groups
└── aws/
    ├── main.tf                  # Main configuration using modules
    ├── variables.tf             # Input variables
    └── outputs.tf               # Output values
```

## Available Modules

### 1. VPC Module

Creates a complete Virtual Private Cloud with subnets, internet gateway, and routing.

**Location:** `infrastructure/modules/vpc/main.tf`

**Key Variables:**

- `vpc_cidr` (default: "10.0.0.0/16") - VPC CIDR block
- `subnet_cidrs` (default: ["10.0.1.0/24", "10.0.2.0/24"]) - Subnet CIDR blocks
- `availability_zones` (default: ["us-east-1a", "us-east-1b"]) - AZs for subnets
- `environment` (default: "development") - Environment name
- `project_name` (default: "cloudops") - Project name for resource naming

**Outputs:**

- `vpc_id` - VPC ID
- `subnet_ids` - List of subnet IDs
- `internet_gateway_id` - Internet Gateway ID
- `route_table_id` - Route Table ID

**Example Usage:**

```hcl
module "vpc" {
  source = "../modules/vpc"
  
  vpc_cidr           = "10.0.0.0/16"
  subnet_cidrs       = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]
  environment        = "development"
  project_name       = "cloudops"
}
```

### 2. Security Group Module

Creates security groups with configurable ingress and egress rules.

**Location:** `infrastructure/modules/security_group/main.tf`

**Key Variables:**

- `vpc_id` - VPC ID (required)
- `security_group_name` (default: "web-sg") - Security group name
- `allowed_ssh_cidrs` (default: ["0.0.0.0/0"]) - SSH allowed CIDR blocks
- `allowed_http_cidrs` (default: ["0.0.0.0/0"]) - HTTP allowed CIDR blocks
- `allowed_https_cidrs` (default: ["0.0.0.0/0"]) - HTTPS allowed CIDR blocks
- `allowed_app_cidrs` (default: ["0.0.0.0/0"]) - Port 5000 allowed CIDR blocks
- `enable_ssh` (default: true) - Enable SSH rule
- `enable_http` (default: true) - Enable HTTP rule
- `enable_https` (default: true) - Enable HTTPS rule
- `enable_app_port` (default: true) - Enable port 5000 rule

**Outputs:**

- `security_group_id` - Security Group ID
- `security_group_name` - Security Group Name
- `security_group_arn` - Security Group ARN

**Example Usage:**

```hcl
module "security_group" {
  source = "../modules/security_group"
  
  vpc_id              = module.vpc.vpc_id
  security_group_name = "web-sg"
  allowed_ssh_cidrs   = ["192.168.1.0/24"]  # Restrict SSH
  enable_ssh          = true
  enable_http         = true
  enable_https        = true
  enable_app_port     = true
}
```

### 3. EC2 Module

Creates EC2 instances with configurable settings.

**Location:** `infrastructure/modules/ec2/main.tf`

**Key Variables:**

- `subnet_id` - Subnet ID (required)
- `security_group_ids` - List of security group IDs (required)
- `instance_type` (default: "t2.micro") - EC2 instance type
- `instance_name` (default: "web-server") - Instance name
- `user_data` (default: "") - User data script
- `root_volume_size` (default: 20) - Root volume size in GB
- `root_volume_type` (default: "gp3") - Root volume type
- `monitoring_enabled` (default: false) - Enable detailed monitoring
- `ami_id` (default: "") - Custom AMI ID (uses latest Ubuntu if empty)

**Outputs:**

- `instance_id` - EC2 Instance ID
- `instance_public_ip` - Public IP (if assigned)
- `instance_private_ip` - Private IP
- `instance_public_dns` - Public DNS name
- `instance_arn` - Instance ARN

**Example Usage:**

```hcl
module "web_server" {
  source = "../modules/ec2"
  
  subnet_id          = module.vpc.subnet_ids[0]
  security_group_ids = [module.security_group.security_group_id]
  instance_type      = "t2.micro"
  instance_name      = "web-server"
  
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install flask
  EOF
}
```

### 4. Elastic IP Module

Creates Elastic IPs for static public addresses.

**Location:** `infrastructure/modules/elastic_ip/main.tf`

**Key Variables:**

- `instance_id` - EC2 Instance ID (required)
- `vpc_id` - VPC ID (required)
- `eip_name` (default: "eip") - Elastic IP name
- `environment` (default: "development") - Environment name
- `project_name` (default: "cloudops") - Project name

**Outputs:**

- `elastic_ip_id` - Elastic IP ID
- `elastic_ip_address` - Elastic IP address
- `elastic_ip_arn` - Elastic IP ARN
- `elastic_ip_domain` - Elastic IP domain (vpc)

**Example Usage:**

```hcl
module "web_eip" {
  source = "../modules/elastic_ip"
  
  instance_id  = module.web_server.instance_id
  vpc_id       = module.vpc.vpc_id
  eip_name     = "web-eip"
  environment  = "development"
  project_name = "cloudops"
}
```

### 5. Load Balancer Module

Creates Application Load Balancers with target groups and listeners.

**Location:** `infrastructure/modules/load_balancer/main.tf`

**Key Variables:**

- `vpc_id` - VPC ID (required)
- `subnet_ids` - List of subnet IDs (required)
- `security_group_ids` - Security group IDs (required)
- `alb_name` (default: "alb") - ALB name
- `load_balancer_type` (default: "application") - Load balancer type
- `enable_deletion_protection` (default: false) - Enable deletion protection
- `enable_http2` (default: true) - Enable HTTP/2
- `enable_cross_zone_load_balancing` (default: true) - Cross-zone balancing
- `idle_timeout` (default: 60) - Idle timeout in seconds

**Outputs:**

- `alb_id` - ALB ID
- `alb_arn` - ALB ARN
- `alb_dns_name` - ALB DNS name
- `target_group_arn` - Target Group ARN
- `listener_arn` - Listener ARN

**Example Usage:**

```hcl
module "load_balancer" {
  source = "../modules/load_balancer"
  
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.subnet_ids
  security_group_ids = [module.security_group.security_group_id]
  alb_name           = "web-alb"
  load_balancer_type = "application"
}
```

## Current AWS Configuration

The main AWS configuration (`infrastructure/aws/main.tf`) uses all these modules together:

```hcl
# VPC with two subnets
module "vpc" {
  source = "../modules/vpc"
  ...
}

# Security group for web traffic
module "security_group" {
  source = "../modules/security_group"
  vpc_id = module.vpc.vpc_id
  ...
}

# EC2 web server
module "web_server" {
  source = "../modules/ec2"
  subnet_id = module.vpc.subnet_ids[0]
  security_group_ids = [module.security_group.security_group_id]
  ...
}

# Elastic IP for static address
module "web_eip" {
  source = "../modules/elastic_ip"
  instance_id = module.web_server.instance_id
  ...
}

# Optional: Load balancer
module "load_balancer" {
  count = var.enable_load_balancer ? 1 : 0
  source = "../modules/load_balancer"
  ...
}
```

## Deploying Infrastructure

### Initialize Terraform

```bash
cd infrastructure/aws
terraform init
```

### Plan Changes

```bash
terraform plan
```

### Apply Changes

```bash
terraform apply
```

### Enable Load Balancer

To enable the load balancer:

```bash
terraform apply -var="enable_load_balancer=true"
```

### View Outputs

```bash
terraform output
```

Example outputs:
```
instance_public_ip = "54.123.45.67"
web_url = "http://54.123.45.67"
connect_command = "ssh -i <your-key.pem> ubuntu@54.123.45.67"
```

## Creating New Modules

To create a new module:

1. **Create module directory:**
   ```bash
   mkdir -p infrastructure/modules/my_module
   ```

2. **Create main.tf with:**
   - Variable definitions
   - Resource definitions
   - Output definitions

3. **Use best practices:**
   - All inputs should be variables
   - Include sensible defaults
   - Always include tags
   - Document variables and outputs
   - Keep modules focused and single-purpose

**Module Template:**

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Input variables
variable "example_var" {
  description = "Description of the variable"
  type        = string
  default     = "default_value"
}

# Resources
resource "aws_example_resource" "main" {
  # ... configuration
  
  tags = {
    Name = "example"
  }
}

# Outputs
output "example_output" {
  description = "Description of output"
  value       = aws_example_resource.main.id
}
```

## Module Best Practices

### 1. **Use Consistent Naming**

```hcl
# Good
resource "aws_security_group" "main" {
  tags = {
    Name = "${var.project_name}-sg"
  }
}

# Avoid
resource "aws_security_group" "randomly_named_group" {
  # ...
}
```

### 2. **Provide Sensible Defaults**

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"  # Free tier option
}
```

### 3. **Document Everything**

```hcl
variable "vpc_cidr" {
  description = "CIDR block for VPC (e.g., 10.0.0.0/16)"
  type        = string
  default     = "10.0.0.0/16"
}
```

### 4. **Use Meta-Arguments**

```hcl
resource "aws_instance" "main" {
  # ...
  
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
  }
  
  depends_on = [
    aws_internet_gateway.main
  ]
}
```

### 5. **Validate Inputs**

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  
  validation {
    condition     = can(regex("^t[2-3]\\.(micro|small|medium)$", var.instance_type))
    error_message = "Instance type must be t2 or t3 micro/small/medium."
  }
}
```

## Troubleshooting

### Module Not Found

**Error:** `Error: module not found`

**Solution:**
```bash
# Ensure correct relative path
# From: infrastructure/aws/
# To: infrastructure/modules/vpc/
source = "../modules/vpc"
```

### Variable Type Mismatch

**Error:** `Error: Incorrect attribute value type`

**Solution:** Check variable types match expected types:
```hcl
# Correct
subnet_ids = module.vpc.subnet_ids  # List of strings

# Wrong
subnet_ids = "subnet-123"  # String instead of list
```

### Outputs Not Available

**Error:** `Error: unsupported attribute`

**Solution:** Check module outputs are defined correctly:
```bash
terraform output -json  # View all outputs
```

## File Organization

```
infrastructure/
├── modules/
│   ├── vpc/
│   │   └── main.tf
│   ├── security_group/
│   │   └── main.tf
│   ├── ec2/
│   │   └── main.tf
│   ├── elastic_ip/
│   │   └── main.tf
│   └── load_balancer/
│       └── main.tf
├── aws/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars (optional)
└── gcp/
    └── (GCP-specific modules)
```

## Next Steps

1. **Create additional modules** for:
   - RDS database
   - S3 buckets
   - CloudFront distribution
   - Route 53 DNS

2. **Implement module versioning** with tags

3. **Add validation rules** for inputs

4. **Create module tests** with Terratest

5. **Document module dependencies** graph

## Related Documentation

- [Terraform Official Documentation](https://www.terraform.io/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Infrastructure as Code Guide](./IaC_GUIDE.md)
- [AWS Guide](./AWS_GUIDE.md)
