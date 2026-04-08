# Variables for AWS Terraform

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type (free tier: t2.micro)"
  type        = string
  default     = "t2.micro"
}

variable "allowed_ssh_cidrs" {
  description = "CIDR blocks allowed for SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # WARNING: Open to all! Restrict this!
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}
