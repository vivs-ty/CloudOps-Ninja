#!/bin/bash
################################################################################
# CloudOps Ninja - Linux & Environment Setup Script
# 🥷 Sets up your machine for the learning journey
# 
# Prerequisites: WSL2 / Linux / macOS
# Run with: chmod +x setup-linux.sh && ./setup-linux.sh
################################################################################

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$NAME
            return 0
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        return 0
    fi
    OS="Unknown"
    return 1
}

# Main setup
main() {
    clear
    print_header "🥷 CloudOps Ninja - Setup Script"
    echo ""
    echo "This script will set up your development environment for learning:"
    echo "  • Python 3"
    echo "  • Docker & Docker Compose"
    echo "  • Git"
    echo "  • AWS CLI"
    echo "  • Terraform"
    echo ""
    
    detect_os
    echo "Detected OS: $OS"
    echo ""
    
    # check for WSL
    if grep -qi microsoft /proc/version 2>/dev/null || grep -qi microsoft /sys/hypervisor/properties/uuid 2>/dev/null; then
        print_warning "WSL detected - you may need to install some tools manually"
    fi
    
    read -p "Continue with setup? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Setup cancelled"
        exit 1
    fi
    
    echo ""
    print_header "Step 1: Update System"
    
    if command -v apt &> /dev/null; then
        print_success "Using apt (Ubuntu/Debian)"
        sudo apt update || print_warning "apt update failed"
        sudo apt install -y curl wget git build-essential || print_warning "apt install failed"
    elif command -v brew &> /dev/null; then
        print_success "Using brew (macOS)"
        brew update || print_warning "brew update failed"
    else
        print_warning "Could not find apt or brew - skipping system update"
    fi
    
    echo ""
    print_header "Step 2: Install Python 3"
    
    if ! command -v python3 &> /dev/null; then
        if command -v apt &> /dev/null; then
            sudo apt install -y python3 python3-pip python3-venv
        elif command -v brew &> /dev/null; then
            brew install python3
        fi
    fi
    
    python3 --version && print_success "Python 3 installed"
    
    echo ""
    print_header "Step 3: Install Docker & Docker Compose"
    
    if ! command -v docker &> /dev/null; then
        if command -v apt &> /dev/null; then
            curl -fsSL https://get.docker.com -o get-docker.sh 2>/dev/null && bash get-docker.sh
            rm -f get-docker.sh
            sudo usermod -aG docker $USER
            print_success "Docker installed - you may need to restart your terminal"
        elif command -v brew &> /dev/null; then
            brew install docker docker-compose
        fi
    fi
    
    docker --version && print_success "Docker installed"
    
    if ! command -v docker-compose &> /dev/null; then
        pip3 install --user docker-compose
    fi
    
    docker-compose --version && print_success "Docker Compose installed"
    
    echo ""
    print_header "Step 4: Install AWS CLI"
    
    if ! command -v aws &> /dev/null; then
        pip3 install --user awscli
    fi
    
    aws --version && print_success "AWS CLI installed"
    
    echo ""
    print_header "Step 5: Install Terraform"
    
    if ! command -v terraform &> /dev/null; then
        if command -v apt &> /dev/null; then
            curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
            sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
            sudo apt-get update && sudo apt-get install terraform || print_warning "Terraform install failed - install manually from terraform.io"
        elif command -v brew &> /dev/null; then
            brew tap hashicorp/tap
            brew install hashicorp/tap/terraform
        fi
    fi
    
    terraform --version && print_success "Terraform installed"
    
    echo ""
    print_header "Step 6: Create Project Directories"
    
    mkdir -p ~/cloudops/{projects,tmp,backups}
    print_success "Project directories created at ~/cloudops"
    
    echo ""
    print_header "Step 7: Install Python Dependencies"
    
    if [ -f "backend/requirements.txt" ]; then
        pip3 install --user -r backend/requirements.txt
        print_success "Python dependencies installed"
    fi
    
    echo ""
    print_header "✅ Setup Complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Read docs/LEARNING_PATH.md"
    echo "  2. Read docs/LINUX_BASICS.md"
    echo "  3. Start with: cd backend && python3 app.py"
    echo "  4. Visit: http://localhost:5000"
    echo ""
    echo "Happy learning! 🚀"
}

# Run main
main
