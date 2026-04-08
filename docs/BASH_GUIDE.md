# 📚 Bash Scripting Guide - Learn by Example

## Part 1: Bash Fundamentals

### Hello World
```bash
#!/bin/bash
echo "Hello, World!"
```

Save as `hello.sh` and run:
```bash
chmod +x hello.sh
./hello.sh
```

### Variables
```bash
#!/bin/bash

# String variables
NAME="CloudOps"
echo "Hello, $NAME"

# Without quotes
GREETING=Hello
echo $GREETING

# Using variables in commands
DATE=$(date)
echo "Today is $DATE"

# Command substitution alternatives
DATE=`date`  # Old style (backticks)

# Numeric operations
COUNT=5
COUNT=$((COUNT + 1))
echo "Count: $COUNT"
```

### Input from User
```bash
#!/bin/bash

echo "What is your name?"
read NAME
echo "Hello, $NAME!"

# Read multiple values
read FIRST LAST
echo "Full name: $FIRST $LAST"

# Read into array
read -a ARRAY
echo "First element: ${ARRAY[0]}"
```

### Conditionals (if/else)
```bash
#!/bin/bash

# Basic if
if [ 5 -gt 3 ]; then
    echo "5 is greater than 3"
fi

# if/else
AGE=25
if [ $AGE -lt 18 ]; then
    echo "Minor"
else
    echo "Adult"
fi

# if/elif/else
if [ $AGE -lt 13 ]; then
    echo "Child"
elif [ $AGE -lt 18 ]; then
    echo "Teen"
else
    echo "Adult"
fi

# Test operators
[ -f file.txt ]     # File exists
[ -d directory ]    # Directory exists
[ -z "$VAR" ]       # String is empty
[ -n "$VAR" ]       # String is not empty
[ "$A" = "$B" ]     # Strings equal
[ "$A" != "$B" ]    # Strings not equal
[ $X -eq $Y ]       # Numbers equal
[ $X -ne $Y ]       # Numbers not equal
[ $X -lt $Y ]       # Less than
[ $X -gt $Y ]       # Greater than
[ $X -le $Y ]       # Less or equal
[ $X -ge $Y ]       # Greater or equal
```

### Loops

#### For Loop
```bash
#!/bin/bash

# Traditional
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# Range
for i in {1..5}; do
    echo "Number: $i"
done

# C-style
for ((i=1; i<=5; i++)); do
    echo "Number: $i"
done

# Loop through files
for file in *.txt; do
    echo "File: $file"
done

# Loop through array
SERVERS=("web1" "web2" "web3")
for server in "${SERVERS[@]}"; do
    echo "Server: $server"
done
```

#### While Loop
```bash
#!/bin/bash

# Basic while
COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done

# While true (infinite loop)
while true; do
    echo "Running..."
    sleep 1
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt
```

### Functions
```bash
#!/bin/bash

# Simple function
greet() {
    echo "Hello!"
}

# Call function
greet

# Function with parameters
deploy() {
    SERVER=$1
    VERSION=$2
    echo "Deploying $VERSION to $SERVER"
}

deploy "web-01" "1.0.0"

# Function with return value
is_running() {
    if pgrep "$1" > /dev/null; then
        return 0  # Success
    else
        return 1  # Failure
    fi
}

if is_running "nginx"; then
    echo "Nginx is running"
else
    echo "Nginx is stopped"
fi

# Function returning output
get_server_status() {
    echo "healthy"
}

STATUS=$(get_server_status)
echo "Status: $STATUS"
```

## Part 2: Advanced Patterns

### Error Handling
```bash
#!/bin/bash

# Exit on any error
set -e

# Exit on undefined variable
set -u

# Exit on pipe error
set -o pipefail

# Combine all
set -euo pipefail

# Trap errors
trap 'echo "Error on line $LINENO"; exit 1' ERR

# Check exit status
command_that_might_fail
if [ $? -ne 0 ]; then
    echo "Command failed"
    exit 1
fi
```

### Arrays
```bash
#!/bin/bash

# Create array
SERVERS=("web1" "web2" "web3")

# Access element
echo ${SERVERS[0]}

# All elements
echo ${SERVERS[@]}

# Length
echo ${#SERVERS[@]}

# Loop
for server in "${SERVERS[@]}"; do
    echo "$server"
done

# Add element
SERVERS+=("web4")

# Associative array (like dictionary)
declare -A CONFIG
CONFIG[host]="localhost"
CONFIG[port]="5000"
echo ${CONFIG[host]}
```

### String Manipulation
```bash
#!/bin/bash

TEXT="hello world"

# Length
echo ${#TEXT}

# Substring
echo ${TEXT:0:5}  # First 5 chars = "hello"

# Remove prefix
echo ${TEXT#hello }  # "world"

# Remove suffix
echo ${TEXT% world}  # "hello"

# Replace
echo ${TEXT/hello/goodbye}  # "goodbye world"

# Uppercase/Lowercase
echo ${TEXT^^}  # HELLO WORLD
echo ${TEXT,,}  # hello world
```

### File Operations
```bash
#!/bin/bash

# Check if file exists
if [ -f "file.txt" ]; then
    echo "File exists"
fi

# Check if directory exists
if [ -d "folder" ]; then
    echo "Directory exists"
fi

# Read file
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Write to file
echo "Hello" > file.txt      # Overwrite
echo "World" >> file.txt     # Append

# Check file permissions
if [ -x "script.sh" ]; then
    echo "File is executable"
fi

# Get file size
SIZE=$(stat -f%z file.txt 2>/dev/null || stat -c%s file.txt)
echo "Size: $SIZE bytes"
```

## Part 3: Real-World Examples

### Example 1: Backup Script
```bash
#!/bin/bash

# Backup script with error handling and logging

set -euo pipefail

# Config
SOURCE_DIR="/home/user/projects"
BACKUP_DIR="/mnt/backup"
LOG_FILE="/var/log/backup.log"

# Function to log
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Main backup function
backup_files() {
    log "Starting backup..."
    
    if [ ! -d "$SOURCE_DIR" ]; then
        log "ERROR: Source directory does not exist"
        return 1
    fi
    
    # Create backup with timestamp
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
    
    tar -czf "$BACKUP_FILE" "$SOURCE_DIR"
    log "Backup complete: $BACKUP_FILE"
    
    # Remove backups older than 30 days
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete
    log "Cleaned old backups"
}

# Error handler
trap 'log "ERROR: Backup failed!"; exit 1' ERR

# Run backup
backup_files
log "Done!"
```

### Example 2: Deployment Script
```bash
#!/bin/bash

# Deploy application with health checks

set -euo pipefail

SERVER=${1:-localhost}
VERSION=${2:-latest}
APP_DIR="/opt/app"

echo "Deploying $VERSION to $SERVER..."

# Connect and deploy
ssh "$SERVER" << 'EOF'
    set -e
    cd /opt/app
    
    # Pull latest code
    git fetch origin
    git checkout "$VERSION"
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run migrations if exists
    if [ -f migrate.sh ]; then
        ./migrate.sh
    fi
    
    # Restart service
    systemctl restart myapp
    
    # Health check
    sleep 2
    if curl -f http://localhost:5000/health > /dev/null; then
        echo "✓ Deployment successful"
    else
        echo "✗ Health check failed"
        exit 1
    fi
EOF

echo "Deployment complete!"
```

### Example 3: System Monitor
```bash
#!/bin/bash

# Monitor system and alert if thresholds exceeded

CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
LOG_FILE="/var/log/system_monitor.log"

monitor_system() {
    # CPU usage
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}' | cut -d. -f1)
    
    # Memory usage
    MEMORY=$(free | awk 'NR==2 {printf("%.0f", $3/$2 * 100)}')
    
    # Disk usage
    DISK=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    # Log stats
    echo "$(date) - CPU: ${CPU}% | Memory: ${MEMORY}% | Disk: ${DISK}%" >> "$LOG_FILE"
    
    # Alert if high
    if [ "$CPU" -gt "$CPU_THRESHOLD" ]; then
        echo "HIGH CPU: $CPU%" | mail -s "Alert" admin@example.com
    fi
    
    if [ "$MEMORY" -gt "$MEMORY_THRESHOLD" ]; then
        echo "HIGH MEMORY: $MEMORY%" | mail -s "Alert" admin@example.com
    fi
}

# Run monitoring
monitor_system
```

## Part 4: Best Practices

### 1. Script Header
```bash
#!/bin/bash
# Description of what the script does
# Usage: ./script.sh [options]
# Author: Your name
# Version: 1.0.0

set -euo pipefail  # Error handling
```

### 2. Comments
```bash
# Good: Explains why, not what
USER_ID=$(id -u)  # Get numeric user ID to check if root

# Bad: Obvious from code
X=5  # Set X to 5
```

### 3. Variable Naming
```bash
# Use UPPER_CASE for constants
BACKUP_DIR="/mnt/backup"

# Use lower_case for variables
backup_file="backup_20240101.tar.gz"

# Use descriptive names
MAXIMUM_RETRIES=3  # Good
MAX_RETRIES=3      # Okay
MR=3               # Bad
```

### 4. Error Handling
```bash
#!/bin/bash
set -euo pipefail

# Trap errors with context
trap 'echo "Error on line ${LINENO}"; exit 1' ERR

# Check command exists
if ! command -v docker &> /dev/null; then
    echo "Docker is required"
    exit 1
fi

# Check file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi
```

### 5. Code Organization
```bash
#!/bin/bash

# ==================== CONFIG ====================
CONFIG_FILE="/etc/app/config.conf"
LOG_FILE="/var/log/app.log"

# ==================== FUNCTIONS ====================
log() {
    echo "[$(date)] $1" >> "$LOG_FILE"
}

deploy() {
    # Implementation
    :
}

# ==================== MAIN ====================
main() {
    deploy
    log "Done"
}

main "$@"
```

---

**Practice Challenge**: Write a script that:
1. Takes a directory as input
2. Counts files in the directory
3. Calculates total size
4. Logs results to a file
5. Alerts if total size > 1GB

**Answer**: See `scripts/` directory for examples!

---

**📖 Next**: Learn Python in `PYTHON_GUIDE.md`
