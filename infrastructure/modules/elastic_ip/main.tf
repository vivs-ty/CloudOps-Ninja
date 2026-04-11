# Elastic IP Module - Reusable Elastic IP configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "instance_id" {
  description = "Instance ID to associate with Elastic IP"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "eip_name" {
  description = "Name of the Elastic IP"
  type        = string
  default     = "eip"
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

variable "network_interface_id" {
  description = "Network interface ID (optional, alternative to instance_id)"
  type        = string
  default     = ""
}

# Elastic IP
resource "aws_eip" "main" {
  instance    = var.instance_id != "" ? var.instance_id : null
  network_interface = var.network_interface_id != "" ? var.network_interface_id : null
  domain      = "vpc"

  tags = {
    Name        = "${var.project_name}-${var.eip_name}"
    Environment = var.environment
  }

  depends_on = []
}

# Outputs
output "elastic_ip_id" {
  description = "Elastic IP ID"
  value       = aws_eip.main.id
}

output "elastic_ip_address" {
  description = "Elastic IP address"
  value       = aws_eip.main.public_ip
}

output "elastic_ip_arn" {
  description = "Elastic IP ARN"
  value       = aws_eip.main.arn
}

output "elastic_ip_domain" {
  description = "Elastic IP domain"
  value       = aws_eip.main.domain
}
