# DCNET Flow Cloud Infrastructure Plan

> **Document Version:** 1.0
> **Created:** 28/01/2026
> **Status:** Proposed
> **Author:** DCNET Team

---

## Executive Summary

Tài liệu này đề xuất 2 phương án hạ tầng cloud cho dự án DCNET Flow dựa trên:
- Tài liệu chính thức của nền tảng
- Quy mô dự án: 15-20 users đồng thời, 46 modules, 237 features
- Single company: Nhật Minh Sports

---

## Table of Contents

1. [Project Scale Analysis](#project-scale-analysis)
2. [Option 1: Single VM (All-in-One)](#option-1-single-vm-all-in-one)
3. [Option 2: Multi-VM with HA](#option-2-multi-vm-with-ha-high-availability)
4. [Comparison Matrix](#comparison-matrix)
5. [Capacity Estimation](#capacity-estimation)
6. [Recommendation](#recommendation-for-dcnet-flow)
7. [Verification & Monitoring](#verification--monitoring)
8. [Sources](#sources-official-documentation)

---

## Project Scale Analysis

| Metric | Value |
|--------|-------|
| **Concurrent Users** | 15-20 (estimated) |
| **Total Modules** | 46 (23 CRM + 23 ERP) |
| **Total Features** | 237 |
| **Custom Modules** | 6+ (Fitting, Coaching, Trade-in, Loyalty, Shipping, Import) |
| **Integrations** | E-commerce (3), Shipping (3), Payment (3), BRAVO migration |
| **Company/Site** | Single company, multiple branches |
| **Data Source** | BRAVO ERP migration |

**Classification**: Medium-scale deployment (10-50 users category)

---

## Option 1: Single VM (All-in-One)

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SINGLE VM (Production)                    │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │     Nginx       │  │    Gunicorn     │                  │
│  │  (Reverse Proxy)│  │   (9 workers)   │                  │
│  └────────┬────────┘  └────────┬────────┘                  │
│           │                    │                            │
│  ┌────────┴────────────────────┴────────┐                  │
│  │          DCNET Flow App              │                  │
│  └──────────────────────────────────────┘                  │
│                                                             │
│  ┌──────────────┐  ┌────────────────────┐                  │
│  │   MariaDB    │  │       Redis        │                  │
│  │  (Database)  │  │  (3 instances)     │                  │
│  │              │  │  - Cache :13000    │                  │
│  │              │  │  - Queue :11000    │                  │
│  │              │  │  - Socket:12000    │                  │
│  └──────────────┘  └────────────────────┘                  │
│                                                             │
│  ┌──────────────────────────────────────┐                  │
│  │     Background Workers (RQ)          │                  │
│  │  - worker-short (2 workers)          │                  │
│  │  - worker-long  (1 worker)           │                  │
│  └──────────────────────────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Resource Specifications

| Component | Specification | Notes |
|-----------|--------------|-------|
| **vCPU** | 32 cores | Formula: 2×cores+1 = 65 Gunicorn workers |
| **RAM** | 64 GB | innodb_buffer_pool = 40-45 GB (~70%) |
| **Storage** | 200 GB SSD | NVMe preferred, IOPS 3000+ |
| **OS** | Ubuntu 22.04 LTS | 64-bit required |
| **Network** | 1 Gbps | Minimum |

### Component Configuration

#### Gunicorn Workers
```
workers = 2 × 32 + 1 = 65 workers
```

#### MariaDB Configuration
```ini
[mysqld]
innodb_buffer_pool_size = 45G    # ~70% of 64GB RAM
max_connections = 85              # 20 + num_workers
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

#### Redis Memory Allocation
| Instance | Port | Memory |
|----------|------|--------|
| redis_cache | 13000 | 4 GB |
| redis_queue | 11000 | 2 GB |
| redis_socketio | 12000 | 1 GB |

#### Background Workers
```
queue-short: 2 workers (reports, validations)
queue-long:  1 worker (heavy processing, integrations)
```

### Estimated Monthly Cost

**Đơn giá:**
- CPU: 94,140 VND/vCPU/tháng
- RAM: 94,140 VND/GB/tháng
- Disk: 3,180 VND/GB/tháng

| Component | Quantity | Unit Price | Cost (VND) |
|-----------|----------|------------|------------|
| vCPU | 32 cores | 94,140 | 3,012,480 |
| RAM | 64 GB | 94,140 | 6,024,960 |
| Disk (SSD) | 200 GB | 3,180 | 636,000 |
| **Subtotal** | | | **9,673,440** |
| Backup Storage | 200 GB | 3,180 | 636,000 |
| **Total** | | | **10,309,440 VND/tháng** |

> ~**10.3 triệu VND/tháng** (~$410 USD)

### Pros & Cons

**Pros:**
- Simple setup và maintenance
- Lower cost
- Easy backup/restore
- Phù hợp cho 15-20 users
- Quick deployment

**Cons:**
- Single point of failure
- Downtime during maintenance
- Limited horizontal scaling
- All components compete for resources

### Suitable For
- Development/Staging environment
- Small to medium production (< 50 users)
- Budget-conscious deployment
- Initial go-live phase

---

## Option 2: Multi-VM with HA (High Availability)

### Architecture Diagram

```
                          ┌─────────────────┐
                          │   DNS/CDN       │
                          └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │  Load Balancer  │
                          │  (Active-Standby)│
                          └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
     ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
     │   App Server 1  │  │   App Server 2  │  │  App Server 3  │
     │   (Primary)     │  │   (Secondary)   │  │  (Optional)    │
     │                 │  │                 │  │                │
     │ - Nginx         │  │ - Nginx         │  │ - Nginx        │
     │ - Gunicorn (5)  │  │ - Gunicorn (5)  │  │ - Gunicorn (5) │
     │ - DCNET Flow    │  │ - DCNET Flow    │  │ - DCNET Flow   │
     └────────┬────────┘  └────────┬────────┘  └────────┬───────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
     ┌─────────────────────────────┼─────────────────────────────┐
     │                             │                             │
     │    ┌────────────────────────┼────────────────────────┐    │
     │    │                        │                        │    │
┌────▼────▼────┐          ┌────────▼────────┐      ┌────────▼────▼────┐
│   Database   │          │     Redis       │      │   Worker Pool    │
│   Cluster    │          │    Cluster      │      │                  │
│              │          │                 │      │ ┌──────────────┐ │
│ ┌──────────┐ │          │ ┌─────────────┐ │      │ │ Worker Node 1│ │
│ │ Primary  │ │          │ │  Primary    │ │      │ │ - short (2)  │ │
│ │ MariaDB  │ │          │ │  Redis      │ │      │ │ - long (1)   │ │
│ └────┬─────┘ │          │ └──────┬──────┘ │      │ └──────────────┘ │
│      │       │          │        │        │      │                  │
│ ┌────▼─────┐ │          │ ┌──────▼──────┐ │      │ ┌──────────────┐ │
│ │ Replica  │ │          │ │  Replica    │ │      │ │ Worker Node 2│ │
│ │ MariaDB  │ │          │ │  Redis      │ │      │ │ - short (2)  │ │
│ └──────────┘ │          │ └─────────────┘ │      │ │ - long (1)   │ │
│              │          │                 │      │ └──────────────┘ │
└──────────────┘          └─────────────────┘      └──────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        Shared Storage (NFS/Object)                  │
│                    - Site files, backups, assets                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Node Specifications

#### Load Balancer (Active-Standby)
| Component | Specification |
|-----------|--------------|
| **vCPU** | 1 core per node |
| **RAM** | 2 GB per node |
| **Storage** | 20 GB SSD per node |
| **Quantity** | **2 VMs** (HA pair) |
| **Software** | HAProxy/Nginx/Cloud LB |

#### Application Servers (Stateless)
| Component | Specification |
|-----------|--------------|
| **vCPU** | 4 cores per node |
| **RAM** | 8 GB per node |
| **Storage** | 50 GB SSD per node |
| **Quantity** | **2 VMs** (có thể scale thêm) |
| **Gunicorn** | 9 workers per node |

#### Database Cluster (Primary-Replica)
| Component | Specification |
|-----------|--------------|
| **vCPU** | 4 cores per node |
| **RAM** | 16 GB per node |
| **Storage** | 200 GB NVMe SSD per node |
| **Quantity** | **2 VMs** (Primary + Replica) |
| **innodb_buffer_pool** | 10 GB |

#### Redis Cluster
| Component | Specification |
|-----------|--------------|
| **vCPU** | 1 core per node |
| **RAM** | 2 GB per node |
| **Storage** | 20 GB SSD per node |
| **Quantity** | **2 VMs** (Primary + Replica) |

#### Background Worker Nodes
| Component | Specification |
|-----------|--------------|
| **vCPU** | 1 core per node |
| **RAM** | 2 GB per node |
| **Storage** | 30 GB SSD per node |
| **Quantity** | **2 VMs** (có thể scale thêm) |
| **Workers** | 3 per node (2 short + 1 long) |

#### Shared Storage
| Component | Specification |
|-----------|--------------|
| **Type** | NFS/Object Storage |
| **Size** | 200 GB |
| **Purpose** | Site files, backups, assets |

### Resource Summary Table

| Node Type | Số VM | vCPU/VM | RAM/VM | Disk/VM | Total vCPU | Total RAM | Total Disk |
|-----------|-------|---------|--------|---------|------------|-----------|------------|
| Load Balancer | 2 | 1 | 2 GB | 20 GB | 2 | 4 GB | 40 GB |
| App Server | 2 | 4 | 8 GB | 50 GB | 8 | 16 GB | 100 GB |
| Database | 2 | 4 | 16 GB | 200 GB | 8 | 32 GB | 400 GB |
| Redis | 2 | 1 | 2 GB | 20 GB | 2 | 4 GB | 40 GB |
| Worker | 2 | 1 | 2 GB | 30 GB | 2 | 4 GB | 60 GB |
| Shared Storage | 1 | - | - | 200 GB | - | - | 200 GB |
| **TOTAL** | **11** | - | - | - | **22** | **60 GB** | **840 GB** |

> **Lưu ý:** Có thể scale bằng cách thêm App Server hoặc Worker nodes khi cần

### Estimated Monthly Cost

**Đơn giá:**
- CPU: 94,140 VND/vCPU/tháng
- RAM: 94,140 VND/GB/tháng
- Disk: 3,180 VND/GB/tháng

| Node Type | Số VM | vCPU | RAM | Disk | CPU Cost | RAM Cost | Disk Cost | Total |
|-----------|-------|------|-----|------|----------|----------|-----------|-------|
| Load Balancer | 2 | 2 | 4 GB | 40 GB | 188,280 | 376,560 | 127,200 | 692,040 |
| App Server | 2 | 8 | 16 GB | 100 GB | 753,120 | 1,506,240 | 318,000 | 2,577,360 |
| Database | 2 | 8 | 32 GB | 400 GB | 753,120 | 3,012,480 | 1,272,000 | 5,037,600 |
| Redis | 2 | 2 | 4 GB | 40 GB | 188,280 | 376,560 | 127,200 | 692,040 |
| Worker | 2 | 2 | 4 GB | 60 GB | 188,280 | 376,560 | 190,800 | 755,640 |
| Shared Storage | 1 | - | - | 200 GB | - | - | 636,000 | 636,000 |
| **TOTAL** | **11** | **22** | **60 GB** | **840 GB** | **2,071,080** | **5,648,400** | **2,671,200** | **10,390,680** |

| Summary | Cost (VND) |
|---------|------------|
| Infrastructure (11 VMs) | 10,390,680 |
| Backup Storage (200 GB) | 636,000 |
| **Total** | **11,026,680 VND/tháng** |

> ~**11 triệu VND/tháng** (~$440 USD)
>
> **Có thể scale thêm:** +1 App Server = +1,288,680 VND | +1 Worker = +377,820 VND

### High Availability Features

| Feature | Implementation |
|---------|----------------|
| **App Server HA** | Load balancer distributes traffic, auto-failover |
| **Database HA** | Primary-Replica replication, automatic failover |
| **Redis HA** | Master-Slave with Sentinel |
| **Worker HA** | Multiple worker nodes, queue distribution |
| **Storage HA** | Redundant shared storage |
| **Network HA** | Dual load balancers, health checks |

### Scaling Strategy

```
Horizontal Scaling Path:
├── App Servers: Add more nodes behind LB (up to 5-10)
├── Workers: Add more worker nodes for heavy jobs
├── Database: Add read replicas for reporting
└── Redis: Scale memory allocation

Vertical Scaling Path:
├── Database: Increase to 8vCPU/32GB for heavy workloads
└── App Servers: Increase to 4vCPU/8GB per node
```

### Pros & Cons

**Pros:**
- No single point of failure
- Zero-downtime maintenance possible
- Horizontal scalability
- Better performance under load
- Database read replicas for reporting
- Suitable for enterprise requirements

**Cons:**
- Higher complexity
- Higher cost (4-5× Option 1)
- Requires DevOps expertise
- More monitoring overhead
- Complex backup/restore procedures

### Suitable For
- Production với SLA 99.9%+
- Future growth planning (50+ users)
- Enterprise requirements
- Critical business operations
- 24/7 availability needs

---

## Comparison Matrix

| Criteria | Option 1 (Single VM) | Option 2 (Multi-VM HA) |
|----------|---------------------|------------------------|
| **Monthly Cost** | ~10.3 triệu VND | ~11 triệu VND |
| **Number of VMs** | 1 VM | 11 VMs |
| **Total Resources** | 32 vCPU / 64 GB RAM | 22 vCPU / 60 GB RAM |
| **Storage** | 200 GB | 840 GB |
| **Setup Complexity** | Low | High |
| **Maintenance** | Simple | Complex |
| **Availability** | ~99% | 99.9%+ |
| **Downtime for Updates** | Required | Zero-downtime possible |
| **Scalability** | Vertical only | Horizontal (thêm VM) |
| **Recovery Time** | Hours | Minutes |
| **Team Skill Required** | Basic sysadmin | DevOps expertise |
| **Suitable Users** | 10-50 | 50-500+ |

---

## Capacity Estimation

> **Lưu ý:** Đây là hệ thống nội bộ (internal), lượng truy cập đồng thời phụ thuộc vào số nhân viên thao tác, không phải public traffic.

### Tiêu chí đánh giá

| Tiêu chí | Option 1 (Single VM) | Option 2 (Multi-VM HA) |
|----------|---------------------|------------------------|
| **Concurrent Users** | 50-100 users | 30-50 users (base), scale to 200+ |
| **Active Sessions** | ~100 sessions | ~60 sessions (base), scalable |
| **Gunicorn Workers** | 65 workers | 18 workers (2 App VMs × 9) |
| **Requests/second** | 500-1,000 req/s | 150-300 req/s (base) |

### Khả năng xử lý giao dịch

| Metric | Option 1 | Option 2 |
|--------|----------|----------|
| **Transactions/ngày** | 5,000-10,000 | 2,000-5,000 (base) |
| **Sales Orders/ngày** | 500-1,000 | 200-500 |
| **Purchase Orders/ngày** | 200-500 | 100-200 |
| **Invoices/ngày** | 500-1,000 | 200-500 |
| **Stock Entries/ngày** | 1,000-2,000 | 500-1,000 |

### Database Capacity

| Metric | Option 1 | Option 2 |
|--------|----------|----------|
| **innodb_buffer_pool** | 45 GB | 10 GB/node |
| **Max DB Size** | 100-150 GB | 300+ GB (2×200GB) |
| **Records (estimated)** | 50-100 triệu records | 100+ triệu records |
| **Query Performance** | Single DB, fast | Primary-Replica, HA |

### Background Jobs & Integrations

| Metric | Option 1 | Option 2 |
|--------|----------|----------|
| **Worker Processes** | 3 (shared) | 6 (2 Worker VMs × 3) |
| **Jobs/hour** | 200-500 | 500-1,000 |
| **Email/ngày** | 1,000-2,000 | 2,000-5,000 |
| **E-commerce Sync** | ✓ Adequate | ✓ Better (dedicated workers) |
| **Shipping API calls** | ✓ Adequate | ✓ Better |
| **Heavy Reports** | ⚠️ May slow down app | ✓ Dedicated workers |

### File Storage

| Metric | Option 1 | Option 2 |
|--------|----------|----------|
| **Disk Space** | 200 GB | 840 GB total |
| **Attachments** | ~50 GB available | ~200 GB shared storage |
| **Backup Storage** | 200 GB | 200 GB |
| **Growth/year** | ~30-50 GB | ~50-100 GB |

### Ước lượng cho DCNET Flow (Nhật Minh Sports)

**Quy mô thực tế dự kiến:**

| Metric | Giá trị ước lượng |
|--------|-------------------|
| **Nhân viên sử dụng** | 15-20 người |
| **Truy cập đồng thời (peak)** | 10-15 sessions |
| **Transactions/ngày** | 100-300 |
| **Sales Orders/ngày** | 20-50 |
| **Database size (year 1)** | 5-10 GB |
| **Attachments (year 1)** | 10-20 GB |

**Kết luận:**
- **Option 1**: Dư sức cho quy mô hiện tại, headroom lớn cho tương lai (5-10 năm)
- **Option 2**: Quá dư cho quy mô hiện tại, phù hợp khi cần HA hoặc scale lên 50+ users

### So sánh trực quan

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CAPACITY vs ACTUAL NEED                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Actual Need (DCNET Flow):                                          │
│  ├── Users: 15-20                                                   │
│  ├── Concurrent: 10-15                                              │
│  └── Transactions: 100-300/ngày                                     │
│                                                                     │
│  Option 1 Capacity:        Option 2 Capacity:                       │
│  ├── Users: 50-100         ├── Users: 30-50 (base)                  │
│  ├── Concurrent: ~100      ├── Concurrent: ~60 (base)               │
│  └── Trans: 5,000-10,000   └── Trans: 2,000-5,000                   │
│                                                                     │
│  Headroom:                                                          │
│  ┌─────────────────────┐   ┌─────────────────────┐                  │
│  │ Option 1: ~5-10×    │   │ Option 2: ~3-5×     │                  │
│  │ current need        │   │ + can scale more    │                  │
│  └─────────────────────┘   └─────────────────────┘                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Recommendation for DCNET Flow

### Phase 1: Go-live (04/08/2026)

**Recommended: Option 1 (Single VM) - High Performance**

| Component | Specification |
|-----------|--------------|
| **vCPU** | 32 cores |
| **RAM** | 64 GB |
| **Storage** | 200 GB NVMe SSD |
| **Backup** | 200 GB (Daily automated) |
| **Cost** | ~10.3 triệu VND/tháng |
| **Capacity** | 50-100 users, 5,000-10,000 trans/ngày |
| **Headroom** | ~5-10× nhu cầu thực tế |

**Rationale:**
- Dư sức cho 15-20 users với headroom 5-10× cho tương lai
- Simple deployment & maintenance
- Không cần DevOps expertise
- Phù hợp cho team 3-4 devs
- Chi phí tương đương Option 2 nhưng performance cao hơn

### Phase 2: Growth (6-12 months after go-live)

**Option 2 (Multi-VM HA) - ~11 triệu VND/tháng**

| Metric | Value |
|--------|-------|
| **Base Capacity** | 30-50 users, 2,000-5,000 trans/ngày |
| **With Scale** | 200+ users |
| **HA/Uptime** | 99.9%+ |

**Chuyển sang Option 2 khi:**
- User count > 50 và cần HA
- Yêu cầu SLA 99.9%+
- Cần zero-downtime maintenance
- Có nhiều background jobs (reports, integrations)
- Scale linh hoạt bằng cách thêm VM

**Scale path:**
- +1 App Server (4vCPU/8GB): +1,288,680 VND/tháng → +50 users
- +1 Worker Node (1vCPU/2GB): +377,820 VND/tháng → +200 jobs/hour

### Migration Path

```
Phase 1 (Go-live)              Phase 2 (Growth)
┌──────────────────────┐       ┌──────────────────────┐
│ Option 1: Single VM  │   →   │ Option 2: Multi-VM   │
│ 32 vCPU / 64 GB RAM  │       │ 11 VMs (22vCPU/60GB) │
│ ~10.3 triệu VND      │       │ ~11 triệu VND        │
└──────────────────────┘       └──────────────────────┘
                                        │
                                        ▼ Scale khi cần
                               ┌──────────────────────┐
                               │ + App Servers        │
                               │ + Worker Nodes       │
                               │ + Database Replicas  │
                               └──────────────────────┘
```

---

## Verification & Monitoring

### Key Metrics to Monitor

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| CPU Load | < 4 (num_cores) | Add workers or scale up |
| Memory Usage | < 80% | Increase RAM |
| Disk I/O | < 80% | Upgrade to faster disk |
| Response Time | < 2s | Optimize queries, add workers |
| Queue Length | < 100 | Add more workers |
| DB Connections | < 80% max | Increase max_connections |

### Benchmark Commands

```bash
# Check Gunicorn workers
bench --site [site] doctor

# Monitor MariaDB
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';

# Redis memory
redis-cli -p 13000 INFO memory

# System resources
htop
iostat -x 1
```

---

## Sources (Official Documentation)

1. [Production Setup Guide](https://docs.frappe.io/framework/user/en/production-setup)
2. [Hardware Specifications](https://github.com/frappe/bench/wiki/OS-and-Hardware-Specifications)
3. [Performance Tuning Guide](https://github.com/frappe/erpnext/wiki/ERPNext-Performance-Tuning)
4. [High Availability Architecture](https://frappe.io/blog/technology/erpnext-ha)
5. [MariaDB Configuration Guide](https://github.com/frappe/bench/wiki/MariaDB-conf-for-Frappe)
6. [Docker Deployment](https://github.com/frappe/frappe_docker)

---

## Appendix A: Pricing Reference

### Đơn giá tham chiếu

| Resource | Unit Price | Note |
|----------|------------|------|
| **vCPU** | 94,140 VND/vCPU/tháng | |
| **RAM** | 94,140 VND/GB/tháng | |
| **Disk (SSD)** | 3,180 VND/GB/tháng | |

### Cost Summary

| Option | Số VM | Resources | Monthly Cost |
|--------|-------|-----------|--------------|
| **Option 1** (Single VM) | 1 | 32 vCPU / 64 GB / 200 GB | **~10.3 triệu VND** |
| **Option 2** (Multi-VM HA) | 11 | 22 vCPU / 60 GB / 840 GB | **~11 triệu VND** |

### So sánh nhanh

```
┌─────────────────────────────────────────────────────────────────────┐
│                        COMPARISON SUMMARY                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Option 1: SINGLE VM (High Performance)                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1 VM  │  32 vCPU  │  64 GB RAM  │  ~10.3 triệu VND/tháng  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  Capacity: 50-100 users │ 5,000-10,000 trans/ngày                   │
│  ✓ Simple    ✓ High power    ✗ No HA    ✗ Cannot scale out         │
│                                                                     │
│  Option 2: MULTI-VM HA (Scalable)                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  11 VMs │  22 vCPU  │  60 GB RAM  │  ~11 triệu VND/tháng   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  Capacity: 30-50 users (base) │ 2,000-5,000 trans/ngày              │
│  ✓ HA 99.9%  ✓ Scale out  ✓ Zero-downtime  ✗ Complex setup         │
│                                                                     │
│  DCNET Flow Actual Need: 15-20 users │ 100-300 trans/ngày           │
│  → Both options have 3-10× headroom                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Recommendation

For DCNET Flow project:
- **Go-live (04/08/2026)**: Option 1 - ~10.3 triệu VND/tháng (simple, high performance)
- **Growth phase (50+ users, SLA 99.9%)**: Option 2 - ~11 triệu VND/tháng + scale thêm VM

---

## Appendix B: Backup Strategy

### Option 1 Backup Plan

```
Daily Backup Schedule:
├── 00:00 - Full site backup (bench --site [site] backup)
├── 06:00 - Database only backup
├── 12:00 - Database only backup
└── 18:00 - Database only backup

Retention:
├── Daily: 7 days
├── Weekly: 4 weeks
└── Monthly: 12 months

Storage:
├── Primary: Same VM (/home/dcnet/backups)
└── Offsite: Object Storage (S3/GCS/VNG)
```

### Backup Commands

```bash
# Manual full backup
bench --site [site] backup --with-files

# Automated backup cron
0 0 * * * cd /home/dcnet/dcnet-bench && bench --site [site] backup --with-files

# Restore
bench --site [site] restore [backup-file]
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 28/01/2026 | DCNET Team | Initial document |
