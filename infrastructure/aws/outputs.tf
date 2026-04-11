# Terraform outputs - Results after terraform apply

# VPC Outputs
output "vpc_id" {
  description = "ID of VPC"
  value       = module.vpc.vpc_id
}

output "subnet_ids" {
  description = "IDs of subnets"
  value       = module.vpc.subnet_ids
}

output "internet_gateway_id" {
  description = "ID of internet gateway"
  value       = module.vpc.internet_gateway_id
}

# Security Group Outputs
output "security_group_id" {
  description = "ID of security group"
  value       = module.security_group.security_group_id
}

output "security_group_name" {
  description = "Name of security group"
  value       = module.security_group.security_group_name
}

# EC2 Outputs
output "instance_id" {
  description = "ID of EC2 instance"
  value       = module.web_server.instance_id
}

output "instance_public_ip" {
  description = "Public IP of the web server"
  value       = module.web_eip.elastic_ip_address
}

output "instance_public_dns" {
  description = "Public DNS of the web server"
  value       = module.web_server.instance_public_dns
}

output "instance_private_ip" {
  description = "Private IP of the web server"
  value       = module.web_server.instance_private_ip
}

# Elastic IP Outputs
output "elastic_ip_id" {
  description = "ID of Elastic IP"
  value       = module.web_eip.elastic_ip_id
}

# Connection Information
output "connect_command" {
  description = "SSH command to connect to instance"
  value       = "ssh -i <your-key.pem> ubuntu@${module.web_eip.elastic_ip_address}"
}

output "web_url" {
  description = "URL to access the web server"
  value       = "http://${module.web_eip.elastic_ip_address}"
}

# Load Balancer Outputs (if enabled)
output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = var.enable_load_balancer ? module.load_balancer[0].alb_dns_name : null
}

output "load_balancer_url" {
  description = "URL to access via load balancer"
  value       = var.enable_load_balancer ? "http://${module.load_balancer[0].alb_dns_name}" : null
}

