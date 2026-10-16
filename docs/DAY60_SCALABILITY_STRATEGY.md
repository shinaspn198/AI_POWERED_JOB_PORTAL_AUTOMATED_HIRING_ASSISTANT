# Day 60 – Scalability Strategy & Horizontal Scaling Document

**Project:** Zecpath Autonomous AI Hiring System  
**Stage:** Day 60  
**Focus:** Horizontal Scaling, Microservice Architecture & Load Balancing Strategy

---

## 1. Architectural Scaling Blueprint

```
                     [ AWS Route 53 / Cloudflare DNS ]
                                     |
                                     v
                       [ Application Load Balancer ]
                        (NGINX / AWS ALB Round-Robin)
                                     |
         +---------------------------+---------------------------+
         |                                                       |
         v                                                       v
  [ AI Worker Pod 1 ]                                     [ AI Worker Pod N ]
  (FastAPI Stateless)                                     (FastAPI Stateless)
         |                                                       |
         +---------------------------+---------------------------+
                                     |
                +--------------------+--------------------+
                |                                         |
                v                                         v
       [ Redis Cache & Queue ]               [ PostgreSQL DB Cluster ]
       - Celery Task Queue                    - Primary (Write)
       - Session States & In-Memory TTL       - Read Replicas (Read-Only Pool)
```

---

## 2. Horizontal Scaling Principles

### A. Stateless Microservice Design
- The FastAPI application container stores zero local session state on the local filesystem.
- All session data is stored in Redis or PostgreSQL, allowing pod instances to be horizontally spun up or terminated with zero downtime.

### B. Auto-Scaling Policies (Kubernetes HPA)
- **CPU / Memory Utilization Trigger:** Scale up when average pod CPU exceeds 70% or memory exceeds 80%.
- **Custom Queue Depth Metric:** Scale up worker pods when Celery / Redis queue backlog exceeds 200 pending resume parsing tasks.

### C. Load Balancing Configuration
- **Algorithm:** Least Outstanding Requests (or Weighted Round-Robin) for long-lived WebSocket connections; Standard Round-Robin with Keep-Alive for HTTP REST endpoints.
- **Health Checks:** Dedicated `/api/health` probes checking database connectivity and worker availability every 5 seconds.

### D. Database Connection Pooling & Read Replicas
- SQLAlchemy `QueuePool` with pool size of 20 connections and max overflow of 10.
- Read-heavy queries (Candidate scorecard views, recruiter lists) routed to PostgreSQL Read Replicas.
