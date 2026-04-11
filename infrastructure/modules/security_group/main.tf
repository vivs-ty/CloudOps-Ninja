# Security Group Module - Reusable security group configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "security_group_name" {
  description = "Name of the security group"
  type        = string
  default     = "web-sg"
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

variable "allowed_ssh_cidrs" {
  description = "CIDR blocks allowed for SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_http_cidrs" {
  description = "CIDR blocks allowed for HTTP"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_https_cidrs" {
  description = "CIDR blocks allowed for HTTPS"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_app_cidrs" {
  description = "CIDR blocks allowed for application port (5000)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_ssh" {
  description = "Enable SSH access"
  type        = bool
  default     = true
}

variable "enable_http" {
  description = "Enable HTTP access"
  type        = bool
  default     = true
}

variable "enable_https" {
  description = "Enable HTTPS access"
  type        = bool
  default     = true
}

variable "enable_app_port" {
  description = "Enable application port (5000) access"
  type        = bool
  default     = true
}

# Security Group
resource "aws_security_group" "main" {
  name   = "${var.project_name}-${var.security_group_name}"
  vpc_id = var.vpc_id

  tags = {
    Name        = "${var.project_name}-${var.security_group_name}"
    Environment = var.environment
  }
}

# SSH Ingress Rule
resource "aws_vpc_security_group_ingress_rule" "ssh" {
  count             = var.enable_ssh ? 1 : 0
  security_group_id = aws_security_group.main.id

  from_port   = 22
  to_port     = 22
  ip_protocol = "tcp"
  cidr_ipv4   = "0.0.0.0/0"

  description = "SSH access"
  tags = {
    Name = "ssh"
  }
}

# HTTP Ingress Rule
resource "aws_vpc_security_group_ingress_rule" "http" {
  count             = var.enable_http ? 1 : 0
  security_group_id = aws_security_group.main.id

  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
  cidr_ipv4   = "0.0.0.0/0"

  description = "HTTP access"
  tags = {
    Name = "http"
  }
}

# HTTPS Ingress Rule
resource "aws_vpc_security_group_ingress_rule" "https" {
  count             = var.enable_https ? 1 : 0
  security_group_id = aws_security_group.main.id

  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
  cidr_ipv4   = "0.0.0.0/0"

  description = "HTTPS access"
  tags = {
    Name = "https"
  }
}

# Application Port Ingress Rule (5000)
resource "aws_vpc_security_group_ingress_rule" "app_port" {
  count             = var.enable_app_port ? 1 : 0
  security_group_id = aws_security_group.main.id

  from_port   = 5000
  to_port     = 5000
  ip_protocol = "tcp"
  cidr_ipv4   = "0.0.0.0/0"

  description = "Application port (Flask)"
  tags = {
    Name = "app-port"
  }
}

# Egress Rule (allow all outbound)
resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.main.id

  from_port   = 0
  to_port     = 0
  ip_protocol = "-1"
  cidr_ipv4   = "0.0.0.0/0"

  description = "Allow all outbound traffic"
  tags = {
    Name = "all-outbound"
  }
}

# Outputs
output "security_group_id" {
  description = "Security Group ID"
  value       = aws_security_group.main.id
}

output "security_group_name" {
  description = "Security Group Name"
  value       = aws_security_group.main.name
}

output "security_group_arn" {
  description = "Security Group ARN"
  value       = aws_security_group.main.arn
}
