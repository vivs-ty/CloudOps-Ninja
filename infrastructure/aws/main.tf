# Basic Terraform for AWS
# Learn Infrastructure as Code

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

# VPC - Your network on AWS
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "cloudops-vpc"
  }
}

# Subnet - Part of the network
resource "aws_subnet" "web" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "cloudops-subnet"
  }
}

# Internet Gateway - Connection to internet
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "cloudops-igw"
  }
}

# Route Table - Traffic rules
resource "aws_route_table" "web" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "cloudops-rt"
  }
}

resource "aws_route_table_association" "web" {
  subnet_id      = aws_subnet.web.id
  route_table_id = aws_route_table.web.id
}

# Security Group - Firewall
resource "aws_security_group" "web" {
  name   = "cloudops-sg"
  vpc_id = aws_vpc.main.id

  # Allow HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH from your IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
  }

  # Allow outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cloudops-sg"
  }
}

# EC2 Instance - Virtual machine
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.web.id
  vpc_security_group_ids = [aws_security_group.web.id]
  associate_public_ip_address = true

  # User data script - runs on startup
  user_data = base64encode(<<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip docker.io
    pip3 install flask
    echo "CloudOps Ninja Server" > index.html
  EOF
  )

  tags = {
    Name = "cloudops-web"
  }
}

# Get latest Ubuntu AMI ID
data "aws_ami" "ubuntu" {
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

# Elastic IP - Static public IP
resource "aws_eip" "web" {
  instance = aws_instance.web.id
  domain   = "vpc"

  tags = {
    Name = "cloudops-eip"
  }

  depends_on = [aws_internet_gateway.main]
}

# Output - Show results after terraform apply
output "instance_public_ip" {
  description = "Public IP of the web server"
  value       = aws_eip.web.public_ip
}

output "instance_dns" {
  description = "Public DNS of the web server"
  value       = aws_instance.web.public_dns
}
