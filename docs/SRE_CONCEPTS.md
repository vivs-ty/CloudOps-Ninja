# 📚 SRE Concepts & Monitoring

## What is SRE (Site Reliability Engineering)?

SRE is an engineering discipline focused on **reliability** and **operations** of systems.

### Key Principles

1. **Reliability First** - Systems should be predictable and consistent
2. **Automation Over Toil** - Automate repetitive tasks
3. **Monitoring & Observability** - Know what's happening in production
4. **Incident Response** - Quickly detect, respond, and learn from failures
5. **Continuous Improvement** - Constantly improve systems

## The SRE Stack

```
┌─────────────────────────────────────────┐
│    Alerting & Incident Response         │
│  (PagerDuty, Slack, Webhooks)           │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    Log Aggregation & Analysis           │
│  (ELK, Stackdriver, CloudWatch)         │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    Metrics & Monitoring                 │
│  (Prometheus, Grafana, Datadog)         │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    Instrumentation                      │
│  (Application metrics, health checks)   │
└─────────────────────────────────────────┘
                    ↑
┌─────────────────────────────────────────┐
│    Applications & Infrastructure        │
└─────────────────────────────────────────┘
```

## Key Metrics

### The Four Golden Signals

1. **Latency** - How fast are responses?
   ```
   Good: < 100ms
   Acceptable: 100-500ms
   Bad: > 1s
   ```

2. **Traffic** - How many requests are coming in?
   ```
   Monitor spikes and trends
   Plan capacity accordingly
   ```

3. **Errors** - What percentage of requests fail?
   ```
   Target: < 0.1%
   Alert if > 1%
   ```

4. **Saturation** - How full is the system?
   ```
   CPU: < 70% (reserve for spikes)
   Memory: < 80%
   Disk: < 85%
   Database connections: < 80%
   ```

### Other Important Metrics

- **Availability** (Uptime %)
  - 99.0% = 3.65 days downtime/year
  - 99.9% = 8.77 hours downtime/year
  - 99.99% = 52 minutes downtime/year

- **Mean Time To Recover (MTTR)** - How fast do we fix it?
- **Mean Time Between Failures (MTBF)** - How stable is the system?

## Monitoring with Prometheus

### What Prometheus Does

```
Applications expose metrics
         ↓
  Prometheus scrapes them
         ↓
  Stores time-series data
         ↓
  Alerts based on rules
```

### Basic Prometheus Setup

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
```

### Prometheus Query Language (PromQL)

```promql
# Current value
cloudops_requests_total

# Rate (requests per second)
rate(cloudops_requests_total[5m])

# Percent of 5xx errors
rate(cloudops_errors_total[5m]) / rate(cloudops_requests_total[5m]) * 100

# CPU usage last hour
100 - (avg by (instance) (rate(node_cpu_seconds_total[1h])))

# Alert: High error rate
rate(cloudops_errors_total[5m]) > 0.05
```

## Alerting Rules

```yaml
# alert_rules.yml
groups:
  - name: CloudOps
    rules:
      # Alert if error rate is too high
      - alert: HighErrorRate
        expr: rate(cloudops_errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate: {{ $value }}"
          description: "Error rate above 5%"

      # Alert if service is down
      - alert: ServiceDown
        expr: up{job="myapp"} == 0
        for: 1m
        annotations:
          summary: "Service down!"

      # Alert if high latency
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "P95 latency > 1s"
```

## Dashboards with Grafana

### Creating a Dashboard

1. **Data Source**: Connect to Prometheus
2. **Panels**: Create visualizations
3. **Queries**: Use PromQL to get metrics
4. **Alerts**: Set up alerting rules

### Example Dashboard Panels

```
┌─────────────────────┬─────────────────────┐
│  Requests/sec       │  Error Rate %       │
│  12,543             │  0.02%              │
└─────────────────────┴─────────────────────┘
┌─────────────────────┬─────────────────────┐
│  P95 Latency (ms)   │  P99 Latency (ms)   │
│  245                │  1,843              │
└─────────────────────┴─────────────────────┘
┌─────────────────────────────────────────┐
│  Requests Over Time (line chart)        │
└─────────────────────────────────────────┘
```

## Incident Response Process

### When an Alert Fires

```
1. ALERT TRIGGERED
   └─> Notification sent (email, Slack, SMS)

2. INVESTIGATION
   └─> Check dashboards
   └─> Review recent changes
   └─> Look at logs
   └─> Run diagnostics

3. MITIGATION
   └─> Scale system
   └─> Roll back change
   └─> Fix configuration
   └─> Restart service

4. RESOLUTION
   └─> Service restored
   └─> Incident closed

5. POST-MORTEM
   └─> What happened?
   └─> Why did it happen?
   └─> What will we do differently?
   └─> Update runbooks/automation
```

### Runbook Example

```markdown
# Runbook: High CPU Alert

## Symptoms
- CPU usage > 80%
- Requests are slow
- Users report issues

## Diagnosis
1. SSH to affected server
2. Run: `top` or `htop`
3. Identify process: `ps aux | grep process_name`
4. Check logs: `journalctl -u service_name`

## Immediate Actions
1. If it's a runaway process: `kill -9 PID`
2. If it's legitimate load:
   - Spin up new instance
   - Add to load balancer
   - Route traffic to new instance

## Long-term
1. Increase instance size
2. Optimize hot code paths
3. Update autoscaling rules
```

## Chaos Engineering

### What is it?

Intentionally break things in production to find weaknesses.

### Examples

```python
# Kill a service
def simulate_service_failure():
    subprocess.run(["systemctl", "stop", "myapp"])
    time.sleep(300)  # Service down for 5 mins
    subprocess.run(["systemctl", "start", "myapp"])
    # Did we auto-recover? Did we detect it?

# Increase latency
def simulate_network_latency():
    subprocess.run(["tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", "500ms"])
    # Run tests...
    subprocess.run(["tc", "qdisc", "del", "dev", "eth0", "root"])

# Fill up disk
def simulate_disk_full():
    subprocess.run(["fallocate", "-l", "50G", "/tmp/fillfile"])
    # Does application handle gracefully?
    os.remove("/tmp/fillfile")
```

## Best Practices

### 1. MoM (Measure of Monitoring)

Every system needs:
- [ ] Uptime monitoring
- [ ] Error rate monitoring
- [ ] Latency monitoring
- [ ] Resource usage (CPU, memory, disk)
- [ ] Dependency monitoring

### 2. Alerting Rules

- [ ] Alert on **outcomes**, not **causes**
  - Good: Alert on "error rate > 5%"
  - Bad: Alert on "cpu > 80%" (it might be fine!)

- [ ] Avoid alert fatigue
  - Good: Alert p99 latency > 1s
  - Bad: Alert on p50 latency > 100ms (too sensitive)

- [ ] Always have a runbook
- [ ] Make alerts actionable

### 3. On-Call

- [ ] Clear escalation policy
- [ ] Someone always on-call
- [ ] Blameless post-mortems
- [ ] Share learnings with team

## Tools in This Project

### What We Use

- **Prometheus** - Metrics collection
- **Grafana** - Dashboards & visualization
- **AlertManager** - Alert routing & grouping
- **Custom Python scripts** - Custom checks

### How to Set Up

```bash
# Start monitoring stack
make run

# Access Grafana
open http://localhost:3000
# user: admin
# password: admin

# View Prometheus
open http://localhost:9090

# Check alerts
open http://localhost:9093
```

## Learning Path

Week 1-2: Understand Four Golden Signals
  └─> Do: Monitor your app

Week 3-4: Set up Prometheus & Grafana
  └─> Do: Create dashboards

Week 5-6: Create alert rules
  └─> Do: Trigger alerts, see if you catch them

Week 7: Practice incident response
  └─> Do: Simulate failures, fix them

Week 8: Chaos engineering
  └─> Do: Run chaos experiments

---

**Next**: Deploy monitoring with `make run` and visit Grafana!

