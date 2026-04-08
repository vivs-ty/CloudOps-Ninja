# Terraform outputs

output "vpc_id" {
  description = "ID of VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of subnet"
  value       = aws_subnet.web.id
}

output "security_group_id" {
  description = "ID of security group"
  value       = aws_security_group.web.id
}

output "instance_id" {
  description = "ID of EC2 instance"
  value       = aws_instance.web.id
}

output "instance_public_ip" {
  description = "Public IP of the web server"
  value       = aws_eip.web.public_ip
}

output "instance_public_dns" {
  description = "Public DNS of the web server"
  value       = aws_instance.web.public_dns
}

output "connect_command" {
  description = "SSH command to connect to instance"
  value       = "ssh -i <your-key.pem> ubuntu@${aws_eip.web.public_ip}"
}
