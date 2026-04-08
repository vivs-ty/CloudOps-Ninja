# 🐍 Python Learning Guide

## Part 1: Python Fundamentals for This Project

### Installation
```bash
# Check if installed
python3 --version

# Install (Ubuntu/Debian)
sudo apt install python3 python3-pip

# Install (macOS)
brew install python3

# Virtual environment (best practice)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Part 2: Essential Python for DevOps/SRE

### Data Types & Variables
```python
# Strings
name = "CloudOps"
message = f"Hello, {name}!"  # f-string (Python 3.6+)

# Lists (arrays)
servers = ["web1", "web2", "web3"]
servers.append("web4")
print(servers[0])  # web1

# Dictionaries (objects/maps)
config = {
    "host": "localhost",
    "port": 5000,
    "debug": True
}
print(config["host"])  # localhost

# Tuples (immutable lists)
coordinates = (10, 20)
x, y = coordinates

# Sets (unique values)
unique_ips = {"192.168.1.1", "192.168.1.2", "192.168.1.1"}

# Type checking
isinstance(5, int)       # True
type(servers)            # <class 'list'>
```

### Conditionals & Loops
```python
# if/else
cpu_usage = 85
if cpu_usage > 80:
    print("HIGH CPU!")
elif cpu_usage > 60:
    print("Medium CPU")
else:
    print("Normal")

# for loop
servers = ["web1", "web2", "web3"]
for server in servers:
    print(f"Checking {server}")

# for with range
for i in range(1, 6):
    print(i)  # 1 to 5

# while loop
count = 0
while count < 5:
    print(count)
    count += 1

# List comprehension
squares = [x**2 for x in range(10)]  # [0, 1, 4, 9, ...]
```

### Functions
```python
# Simple function
def greet(name):
    return f"Hello, {name}"

result = greet("CloudOps")

# Function with default arguments
def deploy(app, environment="production"):
    print(f"Deploying {app} to {environment}")

deploy("myapp")              # Uses "production"
deploy("myapp", "staging")   # Uses "staging"

# Function returning multiple values
def get_status():
    return ("healthy", 99.9, 1234)

status, uptime, timestamp = get_status()

# *args (variable arguments)
def log_servers(*servers):
    for server in servers:
        print(server)

log_servers("web1", "web2", "web3")

# **kwargs (keyword arguments)
def create_config(**options):
    for key, value in options.items():
        print(f"{key}: {value}")

create_config(host="localhost", port=5000, debug=True)
```

### Working with Files
```python
# Read file
with open("config.txt") as f:
    content = f.read()
    
# Read lines
with open("config.txt") as f:
    for line in f:
        print(line.strip())

# Write file
with open("output.txt", "w") as f:
    f.write("Hello, World!")

# Check file exists
import os
if os.path.exists("file.txt"):
    print("File exists")

# Get file size
size = os.path.getsize("file.txt")

# List files in directory
for filename in os.listdir("/home/user"):
    print(filename)
```

### Error Handling
```python
# Try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")

# Multiple exceptions
try:
    data = json.load(file)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Failed to load: {e}")

# Finally block
try:
    f = open("file.txt")
    content = f.read()
finally:
    f.close()

# Better: with statement
with open("file.txt") as f:
    content = f.read()
    # File automatically closed
```

## Part 3: DevOps/SRE Specific Python

### Working with APIs
```python
import requests

# GET request
response = requests.get("http://api.example.com/servers")
data = response.json()
print(data)

# POST request
payload = {"name": "new-server", "type": "t2.micro"}
response = requests.post("http://api.example.com/servers", json=payload)

# Check status
if response.status_code == 200:
    print("Success!")
else:
    print(f"Error: {response.status_code}")

# Error handling
try:
    response = requests.get("http://unreachable.local", timeout=5)
except requests.ConnectionError:
    print("Cannot reach server")
except requests.Timeout:
    print("Request timed out")
```

### JSON Processing
```python
import json

# Parse JSON
data = json.loads('{"name": "web-server", "cpu": 45}')
print(data["name"])

# Convert to JSON
config = {
    "servers": ["web1", "web2"],
    "port": 5000,
    "debug": False
}
json_str = json.dumps(config, indent=2)
print(json_str)

# Read JSON file
with open("config.json") as f:
    config = json.load(f)

# Write JSON file
with open("output.json", "w") as f:
    json.dump(config, f, indent=2)
```

### System Administration
```python
import subprocess
import os
import sys

# Run shell commands
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)  # 0 = success

# Run command with output
output = subprocess.check_output(["ps", "aux"], text=True)
for line in output.split("\n"):
    print(line)

# Environment variables
os.environ["DEBUG"] = "True"
debug = os.getenv("DEBUG", "False")

# Get current user
current_user = os.getenv("USER")

# Exit with code
sys.exit(0)  # Success
sys.exit(1)  # Error
```

### Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Different log levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Log to file
logging.basicConfig(filename='app.log', level=logging.INFO)
```

### DateTime Operations
```python
from datetime import datetime, timedelta
import time

# Current time
now = datetime.now()
print(now)  # 2024-01-01 12:30:45.123456

# Format datetime
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)  # 2024-01-01 12:30:45

# Parse datetime
dt = datetime.strptime("2024-01-01", "%Y-%m-%d")

# Add/subtract time
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)
next_hour = now + timedelta(hours=1)

# Sleep
time.sleep(5)  # Wait 5 seconds

# Measure execution time
start = time.time()
some_operation()
end = time.time()
print(f"Took {end - start:.2f} seconds")
```

## Part 4: Flask Web Framework

### Basic Flask App
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Route with GET
@app.route('/api/status')
def status():
    return jsonify({
        "status": "healthy",
        "uptime": 99.9
    })

# Route with POST
@app.route('/api/deploy', methods=['POST'])
def deploy():
    data = request.json
    app_name = data.get('app')
    version = data.get('version')
    
    return jsonify({
        "message": f"Deploying {app_name} v{version}",
        "status": "success"
    }), 201

# Route with URL parameters
@app.route('/api/servers/<server_id>')
def get_server(server_id):
    return jsonify({
        "id": server_id,
        "status": "running"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Request Handling
```python
from flask import Flask, request, jsonify

@app.route('/api/deploy', methods=['POST'])
def deploy():
    # Get JSON body
    data = request.json
    
    # Get query parameters
    version = request.args.get('version', '1.0')
    
    # Get form data
    name = request.form.get('name')
    
    # Get headers
    auth = request.headers.get('Authorization')
    
    return jsonify({"success": True})

@app.route('/upload', methods=['POST'])
def upload():
    # Get file
    file = request.files['file']
    file.save('uploads/' + file.filename)
    return {"uploaded": True}
```

### Middleware & Decorators
```python
from flask import Flask, jsonify
from functools import wraps
import time

app = Flask(__name__)

# Custom decorator for timing
def measure_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{f.__name__} took {elapsed:.3f}s")
        return result
    return decorated_function

@app.route('/api/slow')
@measure_time
def slow_endpoint():
    time.sleep(2)
    return jsonify({"done": True})

# Before/after requests
@app.before_request
def log_request():
    print(f"Request: {request.method} {request.path}")

@app.after_request
def add_headers(response):
    response.headers['X-Custom-Header'] = 'CloudOps'
    return response
```

## Part 5: Testing Python

### Unit Tests
```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_status_endpoint(self):
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest tests.py -v
# or with pytest
pip install pytest
pytest tests.py -v
```

---

## Next Steps

1. **Copy** the Flask app code from `backend/app.py`
2. **Run** it locally: `python3 app.py`
3. **Modify** it - add new endpoints
4. **Test** your changes
5. **Deploy** using Docker and Terraform

**Learn more**: [Real Python](https://realpython.com/), [Flask Docs](https://flask.palletsprojects.com/)

---

**Ready to code? Let's go! 🚀**
