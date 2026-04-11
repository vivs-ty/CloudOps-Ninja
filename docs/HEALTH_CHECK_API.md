# Health Check API Documentation

## Overview

The Health Check API provides comprehensive monitoring and diagnostics for the CloudOps Ninja application. It performs multiple checks to ensure system health across different layers:

- **Database Connectivity**: Verifies SQLite database connection
- **System Resources**: Monitors CPU, memory, and disk usage
- **External Services**: Checks connectivity to cloud providers and DNS
- **Application Status**: Validates application-level data integrity

## Endpoint

### `GET /api/health`

Perform comprehensive health checks on the entire system.

**Authentication**: Not required

**Response Format**: JSON

**HTTP Status Codes**:
- `200 OK`: System is healthy
- `503 Service Unavailable`: System is unhealthy

## Response Structure

```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "checks": {
    "database": { ... },
    "system_resources": { ... },
    "external_services": { ... },
    "application": { ... }
  },
  "summary": {
    "total_checks": 4,
    "healthy": 4,
    "degraded": 0,
    "unhealthy": 0
  }
}
```

## Detailed Response Objects

### Database Check

```json
{
  "database": {
    "status": "healthy|unhealthy",
    "type": "sqlite",
    "message": "Database connection successful",
    "error": "Optional error message if unhealthy"
  }
}
```

**Status Indicators**:
- `healthy`: Database connection successful
- `unhealthy`: Database connection failed

### System Resources Check

```json
{
  "system_resources": {
    "status": "healthy|degraded",
    "cpu": {
      "usage_percent": 45.2,
      "cores": 8
    },
    "memory": {
      "usage_percent": 62.3,
      "total_mb": 16384,
      "available_mb": 6000,
      "used_mb": 10384
    },
    "disk": {
      "usage_percent": 75.5,
      "total_gb": 250,
      "free_gb": 61
    },
    "warnings": []
  }
}
```

**Thresholds**:
- CPU > 80% → degraded
- Memory > 80% → degraded
- Disk > 85% → degraded

### External Services Check

```json
{
  "external_services": {
    "status": "healthy|degraded",
    "services": {
      "AWS API": {
        "status": "healthy",
        "response_code": 200
      },
      "GCP API": {
        "status": "degraded",
        "error": "Connection error (may be offline)"
      },
      "DNS Resolution": {
        "status": "healthy",
        "message": "DNS resolution working"
      }
    }
  }
}
```

**Checked Services**:
- AWS API (https://api.aws.amazon.com)
- GCP API (https://www.googleapis.com)
- DNS Resolution (8.8.8.8:53)

### Application Status Check

```json
{
  "application": {
    "status": "healthy|degraded",
    "aws_server": {
      "status": "healthy|missing",
      "instances": 2
    },
    "gcp_server": {
      "status": "healthy|missing",
      "instances": 2
    },
    "total_deployments": 5
  }
}
```

## Status Definitions

### Overall Status

- **Healthy**: All checks passed or all checks are in a good state
- **Degraded**: Some checks show warnings or resource usage is high
- **Unhealthy**: One or more critical checks failed

### Summary

The summary object provides a quick overview of all checks:

```json
{
  "summary": {
    "total_checks": 4,
    "healthy": 4,
    "degraded": 0,
    "unhealthy": 0
  }
}
```

## Usage Examples

### Basic Health Check

```bash
curl http://localhost:5000/api/health
```

### With Pretty JSON Output

```bash
curl http://localhost:5000/api/health | python -m json.tool
```

### Check Specific Component

```bash
# Get the response and parse just the database check
curl http://localhost:5000/api/health | jq '.checks.database'

# Check system resources
curl http://localhost:5000/api/health | jq '.checks.system_resources'

# Get overall status
curl http://localhost:5000/api/health | jq '.status'
```

### Scripting Example

```bash
#!/bin/bash
# Health check with automatic retry

HEALTH_URL="http://localhost:5000/api/health"
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  RESPONSE=$(curl -s $HEALTH_URL)
  STATUS=$(echo $RESPONSE | jq -r '.status')
  
  if [ "$STATUS" = "healthy" ]; then
    echo "✓ System is healthy"
    exit 0
  elif [ "$STATUS" = "degraded" ]; then
    echo "⚠ System is degraded"
    echo $RESPONSE | jq '.checks'
    exit 1
  fi
  
  RETRY_COUNT=$((RETRY_COUNT + 1))
  sleep 5
done

echo "✗ Health check failed after $MAX_RETRIES retries"
exit 2
```

## Monitoring Integration

### Prometheus

Add this to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'cloudops-health'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    metrics_relabel_configs:
      - source_labels: [__name__]
        regex: 'cloudops_.*'
        action: keep
```

### Container Health Check

For Docker/Kubernetes deployments:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1
```

### Kubernetes Probe

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Common Responses

### All Systems Healthy

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "summary": {
    "total_checks": 4,
    "healthy": 4,
    "degraded": 0,
    "unhealthy": 0
  }
}
```

### High CPU Warning

```json
{
  "status": "degraded",
  "checks": {
    "system_resources": {
      "status": "degraded",
      "cpu": {
        "usage_percent": 92.5
      },
      "warnings": ["High CPU usage: 92.5%"]
    }
  }
}
```

### Database Connection Failed

```json
{
  "status": "unhealthy",
  "checks": {
    "database": {
      "status": "unhealthy",
      "error": "Unable to connect to database"
    }
  }
}
```

## Troubleshooting

### High CPU Usage

**Issue**: Health check shows `cpu.usage_percent > 80`

**Solutions**:
1. Stop unnecessary processes: `systemctl stop <service>`
2. Increase instance size
3. Scale horizontally

### Database Connection Failed

**Issue**: Database check fails with connection error

**Solutions**:
1. Verify SQLite database exists: `ls -la ./app.db`
2. Check file permissions: `chmod 644 ./app.db`
3. Restart the application
4. Check logs: `tail -f backend.log`

### External Services Unreachable

**Issue**: External services show degraded status and "Connection error"

**Solutions**:
1. Check network connectivity: `ping 8.8.8.8`
2. Verify firewall rules allow outbound HTTPS
3. Check if proxy is needed
4. System may be offline (this is expected in isolated environments)

## Performance Considerations

- **Response Time**: Typically 100-500ms depending on system resources
- **Resource Impact**: Minimal - checks use <1% CPU
- **Database Impact**: No side effects, read-only query
- **Network Impact**: ~50KB of outbound traffic for external service checks

## Related Endpoints

- `GET /api/status` - Quick system status (lighter weight)
- `GET /metrics` - Prometheus metrics
- `GET /api/servers` - Cloud infrastructure stats
- `GET /api/deployments` - Deployment history

## Version History

### v1.0.0 (Current)
- Initial release
- Database connectivity checks
- System resource monitoring
- External service dependency checks
- Application status verification
