# Structured Logging Documentation

## Overview

CloudOps Ninja now includes comprehensive structured logging built on Python's `logging` module. The system provides configurable log levels, both console and file output, and specialized logging functions for different application events.

## Quick Start

### Environment Variables

Configure logging behavior using environment variables:

```bash
# Set log level (DEBUG, INFO, WARNING, ERROR)
export LOG_LEVEL=INFO

# Application will automatically create logs/cloudops.log
```

### Check Logs

View application logs in real-time:

```bash
# View console output (always appears during execution)
# Or read the log file
cat logs/cloudops.log

# Follow log file updates
tail -f logs/cloudops.log
```

## Log Levels

### DEBUG
- Most verbose
- Includes request/response details
- Database queries
- Application flow tracing
- **Use for**: Development, troubleshooting

```bash
export LOG_LEVEL=DEBUG
```

### INFO
- Standard operational messages
- Authentication events
- Deployments
- Health checks
- **Default level**

### WARNING  
- Unusual but non-critical events
- Failed login attempts
- High resource usage warnings
- **Use for**: Production monitoring

### ERROR
- Critical failures
- Failed operations
- Unhandled exceptions
- **Use for**: Production alerts

### CRITICAL
- System-level failures
- Should trigger immediate action

## Configuration

### During Application Startup

The logging system is automatically configured:

```python
# In app.py
configure_logging(app, log_file='logs/cloudops.log')
```

### Custom Configuration

Configure logging programmatically:

```python
from logger import configure_logging, get_logger

# Basic configuration
configure_logging(log_level='DEBUG')

# With file logging
configure_logging(
    app=app,
    log_level='INFO',
    log_file='logs/custom.log'
)

# Get a logger for your module
logger = get_logger(__name__)
logger.info('Application started')
```

## Log Output Format

All logs follow a structured format for easy parsing:

```
[2026-04-11 10:30:45] INFO       | app                        | User logged in: admin
[2026-04-11 10:30:46] INFO       | logger                     | Deployment to aws (version 1.0.0): success
[2026-04-11 10:30:47] WARNING    | logger                     | Authentication failed for user: admin - Error: Invalid credentials
[2026-04-11 10:31:00] ERROR      | app                        | 500 Internal Server Error: Database connection failed
```

### Format Breakdown

- `[Timestamp]` - When the event occurred
- `Level` - Log level (color-coded on console)
- `Logger Name` - Which module generated the log
- `Message` - The log message

## Logged Events

### Authentication

```python
# Successful login
log_authentication('username', True)
# Output: "Authentication successful for user: username"

# Failed login
log_authentication('username', False, 'Invalid password')
# Output: "Authentication failed for user: username - Error: Invalid password"
```

### Deployments

```python
log_deployment('aws', 'v1.0.0', 'success')
# Output: "Deployment to aws (version 1.0.0): success"
```

### Health Checks

```python
log_health_check_result('healthy', {
    'healthy': 4,
    'degraded': 0,
    'unhealthy': 0
})
# Output: "Health check completed: healthy"
```

### Database Operations

```python
log_database_operation('CREATE', 'User', {'user_id': 123})
# Output: "Database CREATE: User"
```

### HTTP Errors

```
# 404 Not Found
[2026-04-11 10:32:00] WARNING    | app | 404 Not Found: /nonexistent

# 500 Server Error
[2026-04-11 10:32:01] ERROR      | app | 500 Internal Server Error: ...
```

## Request Logging

The RequestLogger middleware automatically logs:

- Request start: Method, path, and source IP
- Request completion: Status code
- Errors during request processing

**Example:**

```
[2026-04-11 10:30:45] DEBUG | app | Request started: GET /api/servers
[2026-04-11 10:30:46] DEBUG | app | Request completed: GET /api/servers - Status: 200
```

### Enabling DEBUG Logs for Requests

```bash
export LOG_LEVEL=DEBUG
```

This reveals request details useful for API debugging.

## Log File Management

### Automatic Rotation

Log files are automatically rotated:

- **Max file size**: 10MB
- **Backup count**: 5 files
- **Naming**: `cloudops.log`, `cloudops.log.1`, `cloudops.log.2`, etc.

Old log files are automatically compressed and archived.

### Custom Log File Location

```python
# Via Python
configure_logging(
    app=app,
    log_level='INFO',
    log_file='/var/log/cloudops/app.log'
)

# Create the directory first if needed
os.makedirs('/var/log/cloudops', exist_ok=True)
```

### Log Directory Structure

```
logs/
  cloudops.log      # Current log file (up to 10MB)
  cloudops.log.1    # Previous log file
  cloudops.log.2    # Older log file
  ...
```

## Parsing and Filtering Logs

### View Specific Log Levels

```bash
# Only errors
grep "ERROR" logs/cloudops.log

# Errors and warnings
grep -E "(ERROR|WARNING)" logs/cloudops.log

# All events from a specific module
grep "logger" logs/cloudops.log
```

### Search for Specific Events

```bash
# Authentication events
grep -i "authentication" logs/cloudops.log

# Deployment events
grep "Deployment" logs/cloudops.log

# Health check results
grep "Health check" logs/cloudops.log

# Failed requests
grep "Failed\|ERROR\|500" logs/cloudops.log
```

### Monitor Logs in Real-Time

```bash
# Follow new log entries
tail -f logs/cloudops.log

# With grep filter
tail -f logs/cloudops.log | grep -i "error\|warning"

# Watch for specific user
tail -f logs/cloudops.log | grep "username"
```

## Integration Examples

### Monitoring and Alerting

Integrate logs with your monitoring system:

```bash
#!/bin/bash
# Alert on errors
tail -f logs/cloudops.log | grep ERROR | while read line; do
  # Send alert
  curl -X POST "https://alerts.example.com" -d "error=$line"
done
```

### Docker/Kubernetes

Logs are written to console (stdout) and file, making them compatible with:

- Docker log drivers
- Kubernetes log aggregators
- ELK Stack integration

```dockerfile
# In Dockerfile
RUN mkdir -p /app/logs

# Logs appear in docker logs
ENTRYPOINT ["python", "app.py"]
```

### Log Aggregation

Example with ELK Stack:

```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/cloudops.log
  
output.elasticsearch:
  hosts: ["localhost:9200"]
```

## Troubleshooting

### Logs not being written to file

**Check:**
1. Directory exists: `mkdir -p logs/`
2. Write permissions: `chmod 755 logs/`
3. Log level is set: `export LOG_LEVEL=INFO`

**Solution:**
```bash
mkdir -p logs/
chmod 755 logs/
python app.py
```

### Log file too large

The system automatically rotates files at 10MB. To manually clean:

```bash
# Archive old logs
tar -czf logs/archive-$(date +%Y%m%d).tar.gz logs/*.log.[0-9]*

# Remove archived logs
rm logs/*.log.[0-9]*
```

### Sensitive data in logs

Be careful not to log:
- Passwords
- API keys
- Tokens
- Personal information

The current implementation avoids logging these by default.

## Advanced Configuration

### Custom Format

To customize log format, modify `StructuredFormatter`:

```python
# In logger.py
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        # Customize the format here
        return custom_format
```

### Multiple Loggers

Get separate loggers for different modules:

```python
# In different modules
logger = get_logger(__name__)

# auth.py - logs show "[app.auth]"
# api.py   - logs show "[app.api]"
```

### Handler Configuration

Add custom handlers:

```python
from logger import get_logger
import logging.handlers

logger = get_logger('mymodule')

# Add email handler for critical errors
email_handler = logging.handlers.SMTPHandler(
    'smtp.example.com',
    'app@example.com',
    ['admin@example.com'],
    'Critical Error'
)
email_handler.setLevel(logging.CRITICAL)
logger.addHandler(email_handler)
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# Good
logger.debug('User clicked button X')           # Development
logger.info('User logged in successfully')      # Operations
logger.warning('Database response time high')   # Monitoring
logger.error('Failed to connect to database')   # Alerting
```

### 2. Include Context

```python
# Good
logger.info(f"Deployment {version} to {cloud} initiated by {user}")

# Avoid
logger.info("Deployment started")  # Not enough context
```

### 3. Avoid Logging Secrets

```python
# Good
logger.info(f"Connecting to database: {host}:{port}")

# Bad
logger.info(f"Connecting to database: {host}:{port} with password: {password}")
```

### 4. Use Structured Logging

```python
# Good - can be parsed
logger.info("Deployment complete", extra={
    'cloud': 'aws',
    'version': 'v1.0.0',
    'status': 'success'
})

# Acceptable
logger.info("Deployment to aws v1.0.0: success")
```

## Related Documentation

- [Health Check API](./HEALTH_CHECK_API.md) - Includes health check logging
- [API Documentation](./QUICKSTART.md) - API endpoints and events
- [Deployment Guide](./DEPLOYMENT_STRATEGY.md) - Deployment logging context

## Version History

### v1.0.0 (Current)
- Initial logging implementation
- DEBUG, INFO, WARNING, ERROR levels
- Console and file output
- Structured formatting
- Request/response logging
- Automatic log rotation
- Integration with Flask app
- Specialized logging functions for key events
