# EC2 Module - Reusable EC2 instance configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "subnet_id" {
  description = "Subnet ID for EC2 instance"
  type        = string
}

variable "security_group_ids" {
  description = "List of security group IDs"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name of the EC2 instance"
  type        = string
  default     = "web-server"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "cloudops"
}

variable "user_data" {
  description = "User data script to run on instance startup"
  type        = string
  default     = ""
}

variable "root_volume_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 20
}

variable "root_volume_type" {
  description = "Root volume type"
  type        = string
  default     = "gp3"
}

variable "monitoring_enabled" {
  description = "Enable detailed monitoring"
  type        = bool
  default     = false
}

variable "ami_id" {
  description = "AMI ID (if not provided, will use latest Ubuntu)"
  type        = string
  default     = ""
}

# Get latest Ubuntu AMI if not provided
data "aws_ami" "ubuntu" {
  count       = var.ami_id == "" ? 1 : 0
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# EC2 Instance
resource "aws_instance" "main" {
  ami                    = var.ami_id != "" ? var.ami_id : data.aws_ami.ubuntu[0].id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_group_ids
  monitoring             = var.monitoring_enabled

  # User data
  user_data = var.user_data != "" ? base64encode(var.user_data) : null

  # Root volume configuration
  root_block_device {
    volume_type           = var.root_volume_type
    volume_size           = var.root_volume_size
    delete_on_termination = true

    tags = {
      Name        = "${var.project_name}-root-volume"
      Environment = var.environment
    }
  }

  # Enable public IP assignment
  associate_public_ip_address = true

  tags = {
    Name        = "${var.project_name}-${var.instance_name}"
    Environment = var.environment
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Outputs
output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.main.id
}

output "instance_public_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.main.public_ip
}

output "instance_private_ip" {
  description = "Private IP of the instance"
  value       = aws_instance.main.private_ip
}

output "instance_public_dns" {
  description = "Public DNS of the instance"
  value       = aws_instance.main.public_dns
}

output "instance_private_dns" {
  description = "Private DNS of the instance"
  value       = aws_instance.main.private_dns
}

output "instance_arn" {
  description = "ARN of the instance"
  value       = aws_instance.main.arn
}
