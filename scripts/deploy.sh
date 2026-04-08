#!/bin/bash
################################################################################
# CloudOps Ninja - Deploy Script
# 🥷 Deploys the application to AWS or GCP
#
# Usage: ./deploy.sh <aws|gcp> <version> [environment]
# Example: ./deploy.sh aws 1.0.0 production
################################################################################

set -e
set -u

# Configuration
CLOUD=${1:-aws}
VERSION=${2:-1.0.0}
ENVIRONMENT=${3:-development}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

validate_cloud() {
    case $CLOUD in
        aws|gcp)
            return 0
            ;;
        *)
            log_error "Invalid cloud: $CLOUD. Use 'aws' or 'gcp'"
            exit 1
            ;;
    esac
}

deploy_aws() {
    log_info "Deploying to AWS..."
    
    # Check if terraform files exist
    if [ ! -f "infrastructure/aws/main.tf" ]; then
        log_error "AWS Terraform files not found"
        return 1
    fi
    
    # Navigate to infrastructure directory
    cd infrastructure/aws
    
    log_info "Initializing Terraform..."
    terraform init
    
    log_info "Planning deployment..."
    terraform plan -out=tfplan
    
    log_info "Applying configuration..."
    terraform apply tfplan
    
    log_info "AWS deployment complete!"
    
    cd - > /dev/null
}

deploy_gcp() {
    log_info "Deploying to GCP..."
    
    # Check if terraform files exist
    if [ ! -f "infrastructure/gcp/main.tf" ]; then
        log_error "GCP Terraform files not found"
        return 1
    fi
    
    # Navigate to infrastructure directory
    cd infrastructure/gcp
    
    log_info "Initializing Terraform..."
    terraform init
    
    log_info "Planning deployment..."
    terraform plan -out=tfplan
    
    log_info "Applying configuration..."
    terraform apply tfplan
    
    log_info "GCP deployment complete!"
    
    cd - > /dev/null
}

deploy_docker() {
    log_info "Building Docker image..."
    
    docker build -t cloudops-ninja:${VERSION} backend/
    
    log_info "Running container..."
    docker run -d \
        -p 5000:5000 \
        -e VERSION=${VERSION} \
        -e ENVIRONMENT=${ENVIRONMENT} \
        --name cloudops-ninja-${TIMESTAMP} \
        cloudops-ninja:${VERSION}
    
    log_info "Container running at http://localhost:5000"
}

# Main
main() {
    log_info "CloudOps Ninja Deploy Script"
    echo "Cloud: $CLOUD"
    echo "Version: $VERSION"
    echo "Environment: $ENVIRONMENT"
    echo ""
    
    validate_cloud
    
    case $CLOUD in
        aws)
            deploy_aws
            ;;
        gcp)
            deploy_gcp
            ;;
    esac
    
    log_info "✅ Deployment complete!"
}

# Run
main
