#!/bin/bash
################################################################################
# CloudOps Ninja - Health Check Script
# 🥷 Checks the health of your services
#
# This is a practical Bash script that teaches:
#  - Functions
#  - Curl for API calls
#  - JSON parsing
#  - Error handling
#  - Loops and conditionals
#
# Usage: ./health-check.sh
################################################################################

set -u

# Configuration
SERVICES=(
    "http://localhost:5000"
    "http://localhost:9090"  # Prometheus
    "http://localhost:3000"  # Grafana
)

TIMEOUT=5
RETRIES=3

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
check_service() {
    local url=$1
    local name=$(echo $url | cut -d'/' -f3)
    
    echo -e "${BLUE}Checking $name...${NC}"
    
    # Try to connect with retries
    for i in $(seq 1 $RETRIES); do
        if curl -s --max-time $TIMEOUT "$url/health" > /dev/null 2>&1 || \
           curl -s --max-time $TIMEOUT "$url/api/status" > /dev/null 2>&1 || \
           curl -s --max-time $TIMEOUT "$url" > /dev/null 2>&1; then
            
            echo -e "${GREEN}✓ $name is healthy${NC}"
            return 0
        fi
        
        if [ $i -lt $RETRIES ]; then
            echo -e "${YELLOW}  Retry $i/$RETRIES...${NC}"
            sleep 2
        fi
    done
    
    echo -e "${RED}✗ $name is DOWN${NC}"
    return 1
}

check_disk_space() {
    echo ""
    echo -e "${BLUE}Checking disk space...${NC}"
    
    USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$USAGE" -gt 80 ]; then
        echo -e "${RED}✗ Disk usage: ${USAGE}% (> 80%)${NC}"
        echo "   Run: df -h to see details"
        return 1
    else
        echo -e "${GREEN}✓ Disk usage: ${USAGE}%${NC}"
        return 0
    fi
}

check_memory() {
    echo -e "${BLUE}Checking memory...${NC}"
    
    MEM_FREE=$(free | awk 'NR==2 {print ($7/$2)*100}')
    MEM_USAGE=$((100 - ${MEM_FREE%.*}))
    
    if [ "$MEM_USAGE" -gt 80 ]; then
        echo -e "${RED}✗ Memory usage: ${MEM_USAGE}% (> 80%)${NC}"
        echo "   Run: free -h to see details"
        return 1
    else
        echo -e "${GREEN}✓ Memory usage: ${MEM_USAGE}%${NC}"
        return 0
    fi
}

check_docker() {
    echo ""
    echo -e "${BLUE}Checking Docker...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠ Docker not installed${NC}"
        return 0
    fi
    
    if docker ps > /dev/null 2>&1; then
        RUNNING=$(docker ps -q | wc -l)
        echo -e "${GREEN}✓ Docker running ($RUNNING containers)${NC}"
        return 0
    else
        echo -e "${RED}✗ Docker not running${NC}"
        return 1
    fi
}

generate_report() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    Health Check Report - $(date +%Y-%m-%d\ %H:%M:%S)   ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
    
    # Test all services
    FAILED_SERVICES=0
    for service in "${SERVICES[@]}"; do
        if ! check_service "$service"; then
            ((FAILED_SERVICES++))
        fi
    done
    
    # Check system resources
    check_disk_space || true
    check_memory || true
    check_docker || true
    
    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    if [ "$FAILED_SERVICES" -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ $FAILED_SERVICES service(s) failed${NC}"
        return 1
    fi
}

# Main
main() {
    generate_report
    exit $?
}

# Run
main
