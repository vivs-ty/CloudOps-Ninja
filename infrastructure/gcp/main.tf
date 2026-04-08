# Basic Terraform for GCP
# Similar to AWS but for Google Cloud Platform

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Network
resource "google_compute_network" "vpc" {
  name                    = "cloudops-network"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "cloudops-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

# Firewall rule
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# Compute instance (VM)
resource "google_compute_instance" "web" {
  name         = "cloudops-web"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-lts"
    }
  }

  network_interface {
    network    = google_compute_network.vpc.name
    subnetwork = google_compute_subnetwork.subnet.name

    access_config {
      # Ephemeral public IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install flask
    echo "CloudOps Ninja on GCP" > index.html
  EOF

  tags = ["cloudops", "web"]
}

# Output
output "instance_internal_ip" {
  value = google_compute_instance.web.network_interface[0].network_ip
}

output "instance_external_ip" {
  value = google_compute_instance.web.network_interface[0].access_config[0].nat_ip
}

output "instance_connection_string" {
  value = "gcloud compute ssh cloudops-web --zone=${var.zone}"
}
