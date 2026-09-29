# High-Throughput Transaction Processing Engine (HTTPE)

A production-style, distributed financial transaction processing engine engineered to support a benchmark target of **12,000+ Transactions Per Second (TPS)** with strict ACID compliance, deterministic deadlock prevention, two-tier idempotency barriers, and transactional outbox event streaming.

---

## 🏛️ System Architecture

```
                                  [ CLIENTS / APPS / POS ]
                                             |
                                  (HTTPS / JSON Requests)
                                             |
                                             v
                        +-----------------------------------------+
                        |           API GATEWAY / NGINX           |
                        |   - TLS Termination & Rate Limiting     |
                        |   - Round-Robin / Least-Conn LB         |
                        +-----------------------------------------+
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
                   v                                                   v
     +---------------------------+                       +---------------------------+
     |   HTTPE APP INSTANCE 1    |                       |   HTTPE APP INSTANCE N    |
     |  (Spring Boot / Java 17)  |                       |  (Spring Boot / Java 17)  |
     | - Idempotency Interceptor |                       | - Idempotency Interceptor |
     | - Transfer/Payment Engine |                       | - Transfer/Payment Engine |
     | - Outbox Poller/Publisher |                       | - Outbox Poller/Publisher |
     +---------------------------+                       +---------------------------+
             |            |                                      |            |
             |            +------------------+-------------------+            |
             |                               |                                |
             v                               v                                v
+--------------------------+   +---------------------------+   +--------------------------+
|       REDIS CLUSTER      |   |    POSTGRESQL SHARD 1     |   |    POSTGRESQL SHARD N    |
| - Distributed Lock       |   | [hash(acc_id) % N == 0]   |   | [hash(acc_id) % N == N-1]|
| - Idempotency Cache      |   | - Accounts & Balances     |   | - Accounts & Balances    |
| - Token-Bucket Limiter   |   | - Transactions Ledger     |   | - Transactions Ledger    |
| - Read-Aside Account Meta|   | - Transactional Outbox    |   | - Transactional Outbox   |
+--------------------------+   +---------------------------+   +--------------------------+
                                             |
                                  (Outbox Poller / CDC)
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                    APACHE KAFKA                                         |
| Topics: `txn-events` (16 Partitions) | `txn-events.retry` | `txn-events.dlq`             |
+-----------------------------------------------------------------------------------------+
        |                              |                            |
        v                              v                            v
+------------------+          +------------------+         +------------------+
|  AUDIT CONSUMER  |          |  NOTIF CONSUMER  |         |  FRAUD/RISK SVC  |
+------------------+          +------------------+         +------------------+
```

---

## 🚀 Key Features

- **Deadlock-Free Deterministic Lock Ordering**: Lexicographical account sorting on `SELECT ... FOR UPDATE` eliminates concurrency deadlocks during simultaneous transfers.
- **Two-Tier Idempotency Framework**: Sub-millisecond atomic Redis check (`SETNX`) backed by persistent PostgreSQL SHA-256 request payload verification.
- **Transactional Outbox Pattern**: Guarantees zero event loss between local PostgreSQL transaction commits and Apache Kafka messaging.
- **Atomic Rate Limiting**: Distributed Token-Bucket rate limiter powered by Redis Lua scripts.
- **Precision Accounting**: Strict adherence to arbitrary-precision `NUMERIC(19, 4)` and `BigDecimal` representation for all monetary calculations.

---

## 🛠️ Technology Stack

- **Runtime & Language**: Java 17 LTS / OpenJDK 17
- **Framework**: Spring Boot 3.2.x, Spring Data JPA, Spring Kafka
- **Database**: PostgreSQL 15+ (Sharded / Partitioned)
- **Connection Pool**: HikariCP (Optimized low-latency pooling)
- **In-Memory Cache & Locks**: Redis 7+ / Lettuce Netty
- **Message Broker**: Apache Kafka 3.6+ (16 Partitions, Retry & DLQ Topics)
- **Observability**: Micrometer, Prometheus, Grafana
- **Load Testing**: k6 Async Load Generator

---

## 📊 Performance Capacity Model (12,000 TPS Benchmark Target)

| Metric / Layer | Mathematical Calculation | Sizing & Allocation |
| :--- | :--- | :--- |
| **DB Write IOPS** | 12,000 TPS × 5 operations/txn | **60,000 Write IOPS** (10k IOPS per shard across 6 shards) |
| **Inbound Network** | 12,000 TPS × 400 bytes/req | **38.4 Mbps** (4.8 MB/s) |
| **Outbound Network** | 12,000 TPS × 550 bytes/resp | **52.8 Mbps** (6.6 MB/s) |
| **Kafka Event Ingestion**| 12,000 msgs/sec × 600 B JSON | **7.2 MB/s** across 16 Partitions (450 KB/s per partition) |
| **Redis Memory (24h TTL)**| 414M daily txns × 300 bytes | **~124.2 GB RAM** (~31 GB per node across 4 Redis instances) |

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Docker & Docker Compose
- Java 17+ & Maven 3.8+
- Python 3.10+ (for PDF documentation generator)

### 2. Run Local Stack via Docker Compose
```bash
# Build the Spring Boot application jar
mvn clean package -DskipTests

# Start PostgreSQL, Redis, Kafka, and the HTTPE service
docker compose up -d
```

### 3. Verify Health & OpenAPI Documentation
- **Health Check**: `curl http://localhost:8080/actuator/health`
- **Prometheus Metrics**: `http://localhost:8080/actuator/prometheus`
- **Swagger UI**: `http://localhost:8080/swagger-ui.html`

### 4. Run k6 Load Benchmark
```bash
k6 run load-test/k6_load_test.js
```

### 5. Generate Architecture PDF Manual
```bash
python generate_httpe_pdf.py
```

---

## 📄 API Documentation

### Execute P2P Transfer
`POST /api/v1/transfers`

**Headers:**
```http
Content-Type: application/json
Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d
```

**Request Body:**
```json
{
  "sourceAccountId": "ACC-101",
  "destinationAccountId": "ACC-202",
  "amount": 250.0000,
  "currency": "USD"
}
```

**Response (201 Created):**
```json
{
  "transactionId": "TXN-8d3f7e52-b13c-4e89-9a22-3a215b4c10ef",
  "sourceAccountId": "ACC-101",
  "destinationAccountId": "ACC-202",
  "amount": 250.0000,
  "currency": "USD",
  "status": "SUCCESS",
  "idempotencyKey": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "timestamp": "2026-09-29T10:30:00Z"
}
```

---

## 🛡️ License
Licensed under the [MIT License](LICENSE).
