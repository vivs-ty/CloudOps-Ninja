# Terraform Modules for CloudOps Ninja

This directory contains reusable Terraform modules for AWS infrastructure.

## Quick Start

Each module is standalone and can be used independently:

```hcl
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr     = "10.0.0.0/16"
  project_name = "my-project"
}
```

## Available Modules

| Module | Purpose | Status |
|--------|---------|--------|
| [vpc](./vpc/main.tf) | VPC, subnets, IGW, routing | ✅ Available |
| [security_group](./security_group/main.tf) | Security groups with rules | ✅ Available |
| [ec2](./ec2/main.tf) | EC2 instances | ✅ Available |
| [elastic_ip](./elastic_ip/main.tf) | Elastic IPs | ✅ Available |
| [load_balancer](./load_balancer/main.tf) | Application Load Balancer | ✅ Available |

## Module Structure

Each module contains:
- **main.tf** - Resource definitions, variables, and outputs
- **Documentation in comments** - Inline documentation

Terraform best practice: Keep modules focused and reusable.

## Using Modules

### From Same Directory

```hcl
module "my_vpc" {
  source = "./modules/vpc"
}
```

### From Different Directory

```hcl
module "my_vpc" {
  source = "../modules/vpc"
}
```

### From Remote Repository

```hcl
module "my_vpc" {
  source = "git::https://github.com/vivs-ty/CloudOps-Ninja.git//infrastructure/modules/vpc"
  version = "~> 1.0"
}
```

## Module Inputs and Outputs

### View Module Documentation

```bash
cd vpc
cat main.tf | grep "variable\|output" -A 2
```

### Example: VPC Module

**Inputs:**
- `vpc_cidr` - VPC CIDR block
- `subnet_cidrs` - List of subnet CIDR blocks
- `environment` - Environment name

**Outputs:**
- `vpc_id` - VPC ID
- `subnet_ids` - List of subnet IDs
- `internet_gateway_id` - IGW ID

## Creating a New Module

1. Create directory: `mkdir my_module`
2. Create main.tf with:
   - `terraform` block
   - `variable` blocks
   - `resource` blocks
   - `output` blocks

Example template:

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

variable "example" {
  description = "Example variable"
  type        = string
  default     = "default"
}

resource "aws_example" "main" {
  name = "${var.example}-resource"
  
  tags = {
    Name = "example"
  }
}

output "example_id" {
  value = aws_example.main.id
}
```

## Best Practices

✅ **Do:**
- Use descriptive variable names
- Provide sensible defaults
- Include comprehensive documentation
- Use consistent naming conventions
- Add helpful comments
- Include tags for resource tracking

❌ **Don't:**
- Hard-code values
- Skip input validation
- Forget outputs
- Mix concerns in one module
- Over-complicate modules

## Testing

To test a module:

```bash
cd modules/vpc
terraform init
terraform plan
```

## Dependencies

Some modules may depend on others:
- `ec2` requires `vpc` and `security_group`
- `elastic_ip` requires `ec2`
- `load_balancer` requires `vpc` and `security_group`

The main configuration handles these dependencies automatically.

## Documentation

Full documentation: [docs/TERRAFORM_MODULES.md](../docs/TERRAFORM_MODULES.md)

## Support

For issues or questions:
1. Check the module's main.tf comments
2. Review examples in `../aws/main.tf`
3. Consult Terraform docs: https://www.terraform.io/docs/modules
