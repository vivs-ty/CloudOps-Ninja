# CloudOps Ninja - AWS Infrastructure using Reusable Modules
# Learn Infrastructure as Code with modular Terraform

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source = "../modules/vpc"

  vpc_cidr           = var.vpc_cidr
  subnet_cidrs       = var.subnet_cidrs
  availability_zones = var.availability_zones
  environment        = var.environment
  project_name       = var.project_name
  enable_dns         = true
}

# Security Group Module
module "security_group" {
  source = "../modules/security_group"

  vpc_id                = module.vpc.vpc_id
  security_group_name   = "web-sg"
  environment           = var.environment
  project_name          = var.project_name
  allowed_ssh_cidrs     = var.allowed_ssh_cidrs
  enable_ssh            = true
  enable_http           = true
  enable_https          = true
  enable_app_port       = true
}

# EC2 Module
module "web_server" {
  source = "../modules/ec2"

  subnet_id        = module.vpc.subnet_ids[0]
  security_group_ids = [module.security_group.security_group_id]
  instance_type    = var.instance_type
  instance_name    = "web-server"
  environment      = var.environment
  project_name     = var.project_name
  root_volume_size = 20
  monitoring_enabled = false

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip docker.io git
    pip3 install flask
    echo "CloudOps Ninja Server - Running on $(hostname)" > /var/www/html/index.html
  EOF
}

# Elastic IP Module
module "web_eip" {
  source = "../modules/elastic_ip"

  instance_id   = module.web_server.instance_id
  vpc_id        = module.vpc.vpc_id
  eip_name      = "web-eip"
  environment   = var.environment
  project_name  = var.project_name
}

# Optional: Load Balancer Module
module "load_balancer" {
  count = var.enable_load_balancer ? 1 : 0
  source = "../modules/load_balancer"

  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.subnet_ids
  security_group_ids  = [module.security_group.security_group_id]
  alb_name            = "web-alb"
  environment         = var.environment
  project_name        = var.project_name
  load_balancer_type  = "application"
}

