# Cloud Architecture Fundamentals

## What is Cloud Architecture? 🏗️

Cloud architecture is the **design and structure** of cloud-based systems that provides the foundation for:
- Scalability
- Reliability
- Performance
- Cost-efficiency
- Security

## Architecture Levels

### 1. Single Instance (Week 1)
```
┌─────────────────┐
│  Single VM      │
│  - App running  │
│  - Database     │
│  - Storage      │
└─────────────────┘

Pros: Simple
Cons: Single point of failure
```

### 2. Multi-Instance with Load Balancer (Week 2)
```
┌──────────────────────┐
│   Load Balancer      │
└──────────┬─────────────┘
    ┌──────┴──────┐
    ↓             ↓
┌───────┐     ┌───────┐
│ App 1 │     │ App 2 │
└───┬───┘     └───┬───┘
    └─────────────┘
         ↓
    ┌─────────┐
    │Database │
    └─────────┘

Pros: Redundancy, scalability
Cons: More complex
```

### 3. Multi-Region (Week 3)
```
Region 1 (AWS)          Region 2 (GCP)
┌──────────────┐       ┌──────────────┐
│ Load Bal     │       │ Load Bal     │
│ - App 1      │       │ - App 1      │
│ - App 2      │       │ - App 2      │
│ - Database   │       │ - Database   │
└──────┬───────┘       └───────┬──────┘
       │                       │
       │    Global Router      │
       └───────────┬───────────┘
                   ↓
              Users worldwide

Pros: Global distribution, high availability
Cons: Complex, expensive
```

## Key Architecture Patterns

### Pattern 1: Web Application (Your Setup)
```
Internet
   ↓
Domain/DNS
   ↓
Load Balancer
   ↓
App Servers (2-4 instances)
   ↓
Database
   ↓
Storage (S3/GCS)
```

### Pattern 2: Microservices
```
API Gateway
├── Auth Service
├── User Service
├── Order Service
├── Payment Service
└── Notification Service
```

### Pattern 3: Serverless
```
User Request
   ↓
API Gateway (HTTP endpoint)
   ↓
Cloud Function (Lambda/Cloud Run)
   ↓
Database/Storage
```

### Pattern 4: Event-Driven
```
Event Publisher
   ↓
Event Queue (Kafka/Pub-Sub)
   ↓
Event Consumers (multiple services)
   ↓
Databases/Storage
```

## Architecture Decisions

### When to Scale Vertically (bigger machine)
- Cost < $500/month
- Single function has high load
- Data must stay on one machine

### When to Scale Horizontally (more machines)
- Need > 99.9% uptime
- Cost > $500/month
- Need to handle traffic spikes
- Need disaster recovery

### When to Use Serverless
- Unpredictable traffic
- Short-lived tasks
- Don't want to manage infrastructure
- Cost-conscious

### When to Use Containers (Docker/Kubernetes)
- Multiple environments (dev, staging, prod)
- Need reproducibility
- Team > 5 people
- Frequent deployments

## High Availability (HA) Setup

### For 99.9% Uptime
```
Primary Region          Secondary Region
┌──────────────┐       ┌──────────────┐
│ Active-Active│       │      Or      │
│ Load Bal     │       │  Standby     │
│ ├─ App 1     │       │              │
│ ├─ App 2     │       │              │
│ └─ DB        │       │  Replication │
└──────┬───────┘       └────────┬─────┘
       │                        │
       └────────── Keep in Sync ┘

Metrics:
- 99% = 3.7 days downtime/year ❌
- 99.9% = 8.8 hours downtime/year ✅
- 99.99% = 52 minutes downtime/year ✅✅
```

### For 99.99% Uptime
```
Master Region (Active)
├── AZ-1 (Data Center 1)
│   ├── App instances (3 copies)
│   ├── Database (primary)
│   └── Load Balancer
│
├── AZ-2 (Data Center 2)
│   ├── App instances (3 copies)
│   └── Database (replica)
│
Backup Region (Standby)
├── App instances (warm standby)
├── Database (continuous sync)
└── Can take over in < 5 minutes

Replication:
- Synchronous (must confirm before commit)
- Asynchronous (fire and forget)
```

## Cost Optimization

### 1. Right-Sizing
```bash
# Over-provisioned ❌
- 10 t2.xlarge instances when 2-3 suffice

# Right-sized ✅
- 3 t2.medium instances
- 2-4 autoscaling based on metrics
```

### 2. Reserved Instances (35% discount!)
```bash
# Pay upfront for 1 year commitment
# Better than on-demand
# Use for base load, on-demand for spikes
```

### 3. Spot Instances (70% discount!)
```bash
# Short-term, interruptible compute
# Great for:
# - Batch processing
# - Background jobs
# - Dev/test environments
```

### 4. Right Storage Tier
```
Hot Data (frequently accessed)   → Standard storage
Warm Data (occasionally used)    → Infrequent access
Cold Data (archival)             → Glacier/Archive

Example costs:
Standard: $0.023/GB/month
Infrequent: $0.0125/GB/month
Archive: $0.004/GB/month
```

### 5. Data Transfer Costs
```
Best practices:
- Keep data in same region
- Use CDN for static content
- Compress before transfer
- Cache aggressively
```

## Security Architecture

### Defense in Depth
```
Layer 1: Internet
   ↓
Layer 2: DDoS Protection (CloudFlare, AWS Shield)
   ↓
Layer 3: Firewall & WAF (Web Application Firewall)
   ↓
Layer 4: VPC/Security Groups (Network segmentation)
   ↓
Layer 5: Authentication (IAM, OAuth, MFA)
   ↓
Layer 6: Encryption in Transit (TLS/SSL)
   ↓
Layer 7: Encryption at Rest (KMS, customer-managed keys)
   ↓
Layer 8: Application Security
   ↓
Layer 9: Data Layer Security (Row-level security, RBAC)
```

### Zero Trust Architecture
```
Before: Trust inside network, verify outside
After: Never trust, always verify

- Verify every request
- Encrypt everything
- Log everything
- Assume breach
- Micro-segmentation
```

## Resilience Patterns

### Circuit Breaker
```
Request → Service
  │
  ├─ Success → Allow call
  ├─ Fail (< threshold) → Allow call
  ├─ Fail (> threshold) → Trip circuit
  │    ↓
  │    Return cached/default response
  │    ↓
  │    (After timeout) Try again
```

### Bulkhead Pattern
```
Service Partition 1   Service Partition 2   Service Partition 3
├─ Threads (10)       ├─ Threads (10)       ├─ Threads (10)
├─ Memory (100MB)     ├─ Memory (100MB)     ├─ Memory (100MB)
└─ Connections (5)    └─ Connections (5)    └─ Connections (5)

If Partition 1 fails, Partitions 2 & 3 unaffected
```

### Graceful Degradation
```
All Features Available → Remove non-critical features
                      → Essential features only
                      → Maintenance mode
                      → Complete outage

Example:
- Can't reach recommendations? → Hide recommendations
- Database slow? → Use cached data
- Auth service down? → Deny new signups
```

## Monitoring Architecture

```
Applications (Emit metrics)
    ↓
Metrics Collector (Prometheus)
    ↓
Metrics Storage (Time-series DB)
    ↓
Query Engine (Prometheus)
    ↓
┌───────────────────────┐
├── Visualization       │
│   (Grafana dashboards)│
├── Alerting            │
│   (AlertManager)      │
└── Analytics           │
    (Custom queries)    │

Logs:
Applications (Emit logs)
    ↓
Log Collector (Fluentd/Logstash)
    ↓
Log Storage (Elasticsearch)
    ↓
Log Viewer (Kibana)
    ↓
Analysis & Alerting
```

## Your Architecture (CloudOps Ninja)

```
Global View:

┌─────────────────────────────────────────────────────┐
│              Users Worldwide                        │
└─────────────────────┬───────────────────────────────┘
                      ↓
        ┌─────────────────────────┐
        │   Global Load Balancer  │
        └──────────┬──────────────┘
        ┌──────────┴──────────┐
        ↓                     ↓
    AWS Region          GCP Region
    us-east-1           us-central1
    
┌─────────────────┐   ┌─────────────────┐
│  AWS Setup      │   │  GCP Setup      │
├─────────────────┤   ├─────────────────┤
│ VPC/VNetwork    │   │ VPC/VNetwork    │
│ ├─ Load Bal     │   │ ├─ Load Bal     │
│ ├─ App 1,2,3    │   │ ├─ App 1,2,3    │
│ ├─ RDS DB       │   │ ├─ Cloud SQL    │
│ └─ S3 Bucket    │   │ └─ GCS Bucket   │
│ Monitoring:     │   │ Monitoring:     │
│ └─ CloudWatch   │   │ └─ Stack Driver │
└─────────────────┘   └─────────────────┘
        ↓                       ↓
        └───┬─────────────────┬─┘
            ↓                 ↓
    ┌───────────────────────────────┐
    │   Central Monitoring Stack    │
    │   Prometheus + Grafana +      │
    │   Alert Manager + Custom Apps │
    └───────────────────────────────┘
```

---

For hands-on practice, see [projects/README.md](../projects/README.md)

**Next**: Start with Project 1! 🚀
