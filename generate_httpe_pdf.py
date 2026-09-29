import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "HIGH-THROUGHPUT TRANSACTION PROCESSING ENGINE (HTTPE) — ARCHITECTURE & CODE MANUAL")
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "TARGET: 12,000+ TPS")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(8.5 * 72 - 54, 34, footer_text)
        self.drawString(54, 34, "CONFIDENTIAL — FINTECH DISTRIBUTED SYSTEMS & PERFORMANCE ENGINEERING PORTFOLIO")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 44, 8.5 * 72 - 54, 44)
        
        self.restoreState()

def create_httpe_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0F2942")   # Dark Navy
    secondary_color = colors.HexColor("#1E4E79") # Deep Blue
    accent_color = colors.HexColor("#2B6CB0")    # Classic Blue
    dark_neutral = colors.HexColor("#2D3748")    # Charcoal
    light_bg = colors.HexColor("#F8FAFC")        # Slate White
    code_bg = colors.HexColor("#EDF2F7")         # Soft Code Grey
    border_color = colors.HexColor("#CBD5E0")
    tag_bg = colors.HexColor("#E2E8F0")

    # Typography Styles
    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )

    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_neutral,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#1A202C")
    )

    qa_q_style = ParagraphStyle(
        'QAQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=primary_color,
        spaceBefore=3,
        spaceAfter=1,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QAA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.8,
        textColor=dark_neutral,
        leftIndent=8,
        spaceAfter=3
    )

    story = []

    # ================= COVER BANNER =================
    story.append(Paragraph("High-Throughput Transaction Processing Engine (HTTPE)", cover_title))
    story.append(Paragraph("A Distributed FinTech Architecture Engineered for 12,000+ TPS | Java 17, Spring Boot 3, Kafka, Redis, PostgreSQL", cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceBefore=0, spaceAfter=10))

    # Meta Info Summary Table
    meta_table_data = [
        [Paragraph("<b>Target Benchmark:</b> 12,000+ TPS (Linear Sharded Scale)", body_style),
         Paragraph("<b>Core Invariant:</b> Strict Financial Consistency (Zero Double Debit)", body_style)],
        [Paragraph("<b>Database Strategy:</b> Hash Sharding + Deterministic Row-Level Locks", body_style),
         Paragraph("<b>Event Architecture:</b> Transactional Outbox + 16-Partition Kafka", body_style)],
        [Paragraph("<b>Deduplication:</b> 2-Tier SHA-256 Idempotency (Redis + DB)", body_style),
         Paragraph("<b>Observability:</b> Prometheus Histograms & Percentiles (p50/p95/p99)", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    def add_code_block(title, content):
        if title:
            story.append(Paragraph(title, h2_style))
        t = Table([[Paragraph(f"<pre>{content}</pre>", code_style)]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), code_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    # ================= 1. PROJECT OVERVIEW =================
    story.append(Paragraph("1. Executive Project Overview & Core Philosophy", h1_style))
    story.append(Paragraph(
        "The <b>High-Throughput Transaction Processing Engine (HTTPE)</b> is an enterprise-grade distributed banking ledger and payment processing "
        "engine designed to handle <b>12,000+ Transactions Per Second (TPS)</b>. The platform coordinates customer account lifecycle, peer-to-peer (P2P) transfers, "
        "and payment provider interactions while guaranteeing strict ACID compliance, idempotency across retries, and high availability.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Design Tenet:</b> In financial infrastructure, <i>correctness and auditability take absolute precedence over blind throughput</i>. "
        "A system that executes 50,000 TPS but allows double-spending or balance divergence is unacceptable. HTTPE guarantees mathematical balance conservation "
        "through deterministic row locking, zero event loss via the Transactional Outbox pattern, and sub-millisecond deduplication using Redis memory barriers.",
        body_style
    ))

    # ================= 2. ARCHITECTURE DIAGRAM =================
    story.append(Paragraph("2. Distributed System Architecture & Flow", h1_style))
    arch_ascii = """                                  [ CLIENTS / APPS / POS ]
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
+------------------+          +------------------+         +------------------+"""
    add_code_block("System Architecture Diagram", arch_ascii)

    # ================= 3. DATABASE SCHEMA & DDL =================
    story.append(Paragraph("3. PostgreSQL DDL Schema & Invariant Constraints", h1_style))
    story.append(Paragraph(
        "The persistence layer is modeled with immutable double-entry ledger transactions, optimistic/pessimistic balance locks, "
        "and an integrated outbox table. Precision is strictly bounded using <b>NUMERIC(19, 4)</b> to eliminate floating-point error.",
        body_style
    ))
    ddl_code = """-- Accounts Table (Partitioned by hash(account_id))
CREATE TABLE accounts (
    account_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    balance NUMERIC(19, 4) NOT NULL CHECK (balance >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    version BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_accounts_customer ON accounts (customer_id);

-- Transactions Ledger (Immutable Record)
CREATE TABLE transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    source_account_id VARCHAR(64) NOT NULL,
    destination_account_id VARCHAR(64) NOT NULL,
    amount NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    failure_reason VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_tx_source_created ON transactions (source_account_id, created_at DESC);
CREATE INDEX idx_tx_dest_created ON transactions (destination_account_id, created_at DESC);

-- Transactional Outbox (Guarantees zero-loss event streaming)
CREATE TABLE outbox_events (
    event_id VARCHAR(64) PRIMARY KEY,
    aggregate_type VARCHAR(64) NOT NULL,
    aggregate_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_outbox_pending ON outbox_events (status, created_at) WHERE status = 'PENDING';

-- Idempotency Records
CREATE TABLE idempotency_records (
    idempotency_key VARCHAR(128) PRIMARY KEY,
    request_hash VARCHAR(64) NOT NULL,
    transaction_id VARCHAR(64),
    status VARCHAR(20) NOT NULL,
    response_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);"""
    add_code_block("PostgreSQL Production DDL", ddl_code)

    # ================= 4. JAVA SOURCE IMPLEMENTATION =================
    story.append(Paragraph("4. Production Java Implementation Source Code", h1_style))
    story.append(Paragraph("Complete implementations of core business logic, services, controllers, and infrastructure beans.", body_style))

    # Entity & DTO Code
    add_code_block("Account.java (Entity)", """package com.example.httpe.entity;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "accounts")
public class Account {
    @Id @Column(name = "account_id", length = 64) private String accountId;
    @Column(name = "customer_id", length = 64, nullable = false) private String customerId;
    @Column(name = "currency", length = 3, nullable = false) private String currency;
    @Column(name = "balance", precision = 19, scale = 4, nullable = false) private BigDecimal balance;
    @Column(name = "status", length = 20, nullable = false) private String status;
    @Version @Column(name = "version") private Long version;
    @Column(name = "created_at", updatable = false) private Instant createdAt;
    @Column(name = "updated_at") private Instant updatedAt;

    public Account() {}
    public Account(String accountId, String customerId, String currency, BigDecimal initialBalance) {
        this.accountId = accountId; this.customerId = customerId; this.currency = currency;
        this.balance = initialBalance; this.status = "ACTIVE"; this.version = 0L;
        this.createdAt = Instant.now(); this.updatedAt = Instant.now();
    }
    public void debit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException("Amount must be positive");
        if (this.balance.compareTo(amount) < 0) throw new IllegalStateException("Insufficient balance");
        this.balance = this.balance.subtract(amount); this.updatedAt = Instant.now();
    }
    public void credit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException("Amount must be positive");
        this.balance = this.balance.add(amount); this.updatedAt = Instant.now();
    }
    public String getAccountId() { return accountId; }
    public BigDecimal getBalance() { return balance; }
    public String getCurrency() { return currency; }
    public String getStatus() { return status; }
}""")

    add_code_block("TransferService.java (Deadlock-Free Deterministic Locking Engine)", """package com.example.httpe.service;
import com.example.httpe.dto.*;
import com.example.httpe.entity.*;
import com.example.httpe.exception.*;
import com.example.httpe.idempotency.IdempotencyService;
import com.example.httpe.repository.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.*;
import java.time.Instant;
import java.util.UUID;

@Service
public class TransferService {
    private final AccountRepository accountRepository;
    private final TransactionRepository transactionRepository;
    private final OutboxEventRepository outboxEventRepository;
    private final IdempotencyService idempotencyService;
    private final ObjectMapper objectMapper;
    private final Counter successCounter;
    private final Counter failureCounter;
    private final Timer transferTimer;

    public TransferService(AccountRepository accountRepo, TransactionRepository txRepo,
                           OutboxEventRepository outboxRepo, IdempotencyService idempSvc,
                           ObjectMapper mapper, MeterRegistry registry) {
        this.accountRepository = accountRepo; this.transactionRepository = txRepo;
        this.outboxEventRepository = outboxRepo; this.idempotencyService = idempSvc;
        this.objectMapper = mapper;
        this.successCounter = registry.counter("httpe.tx.success.total");
        this.failureCounter = registry.counter("httpe.tx.failed.total");
        this.transferTimer = registry.timer("httpe.tx.latency");
    }

    @Transactional(propagation = Propagation.REQUIRED, isolation = Isolation.READ_COMMITTED, timeout = 5)
    public TransferDto.Response executeTransfer(TransferDto.Request request, String idempotencyKey) {
        return transferTimer.record(() -> {
            if (request.sourceAccountId().equals(request.destinationAccountId())) {
                throw new IllegalArgumentException("Source and destination accounts must be distinct");
            }
            // 1. Deterministic Lock Acquisition (Lexicographical ordering prevents cyclic deadlocks)
            String firstLockId = request.sourceAccountId().compareTo(request.destinationAccountId()) < 0
                    ? request.sourceAccountId() : request.destinationAccountId();
            String secondLockId = firstLockId.equals(request.sourceAccountId())
                    ? request.destinationAccountId() : request.sourceAccountId();

            Account first = accountRepository.findByIdForUpdate(firstLockId)
                    .orElseThrow(() -> new AccountNotFoundException("Account not found: " + firstLockId));
            Account second = accountRepository.findByIdForUpdate(secondLockId)
                    .orElseThrow(() -> new AccountNotFoundException("Account not found: " + secondLockId));

            Account source = firstLockId.equals(request.sourceAccountId()) ? first : second;
            Account dest = firstLockId.equals(request.sourceAccountId()) ? second : first;

            if (!"ACTIVE".equals(source.getStatus()) || !"ACTIVE".equals(dest.getStatus())) {
                throw new IllegalStateException("Accounts must be active");
            }
            if (source.getBalance().compareTo(request.amount()) < 0) {
                failureCounter.increment();
                throw new InsufficientBalanceException("Insufficient balance");
            }

            // 2. Ledger balance mutation
            source.debit(request.amount());
            dest.credit(request.amount());
            accountRepository.save(source);
            accountRepository.save(dest);

            // 3. Record immutable transaction
            String transactionId = "TXN-" + UUID.randomUUID();
            Transaction tx = new Transaction(transactionId, source.getAccountId(), dest.getAccountId(),
                    request.amount(), request.currency(), "SUCCESS", idempotencyKey);
            transactionRepository.save(tx);

            // 4. Atomically enqueue Transactional Outbox event
            try {
                TransactionEvent event = new TransactionEvent("EVT-" + UUID.randomUUID(), "TRANSACTION_COMPLETED",
                        transactionId, source.getAccountId(), dest.getAccountId(), request.amount(), request.currency(), Instant.now());
                outboxEventRepository.save(new OutboxEvent(UUID.randomUUID().toString(), "TRANSACTION",
                        transactionId, "TRANSACTION_COMPLETED", objectMapper.writeValueAsString(event)));
            } catch (Exception e) { throw new RuntimeException("Outbox serialization failure", e); }

            TransferDto.Response response = new TransferDto.Response(transactionId, source.getAccountId(),
                    dest.getAccountId(), request.amount(), request.currency(), "SUCCESS", idempotencyKey, Instant.now());
            idempotencyService.completeRecord(idempotencyKey, transactionId, response);
            successCounter.increment();
            return response;
        });
    }
}""")

    add_code_block("IdempotencyService.java (Two-Tier Multi-Level Deduplication)", """package com.example.httpe.idempotency;
import com.example.httpe.entity.IdempotencyRecord;
import com.example.httpe.exception.IdempotencyConflictException;
import com.example.httpe.repository.IdempotencyRecordRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.*;

@Service
public class IdempotencyService {
    private final StringRedisTemplate redisTemplate;
    private final IdempotencyRecordRepository repository;
    private final ObjectMapper objectMapper;

    public IdempotencyService(StringRedisTemplate redisTemplate, IdempotencyRecordRepository repository, ObjectMapper objectMapper) {
        this.redisTemplate = redisTemplate;
        this.repository = repository;
        this.objectMapper = objectMapper;
    }

    public <T> T checkAndLock(String idempotencyKey, Object requestPayload, Class<T> responseType) {
        String requestHash = computeSha256(requestPayload);
        String redisKey = "idempotency:" + idempotencyKey;

        // 1. In-Memory Sub-Millisecond Cache Lookup
        String cached = redisTemplate.opsForValue().get(redisKey);
        if (cached != null) {
            if ("IN_PROGRESS".equals(cached)) throw new IdempotencyConflictException("Concurrent request in progress");
            try { return objectMapper.readValue(cached, responseType); } catch (Exception ignored) {}
        }

        // 2. Database Record Verification
        var recordOpt = repository.findById(idempotencyKey);
        if (recordOpt.isPresent()) {
            IdempotencyRecord record = recordOpt.get();
            if (!record.getRequestHash().equals(requestHash)) throw new IdempotencyConflictException("Payload mismatch for key");
            if ("COMPLETED".equals(record.getStatus())) {
                try { return objectMapper.readValue(record.getResponseData(), responseType); } catch (Exception e) { throw new RuntimeException(e); }
            } else throw new IdempotencyConflictException("Request is currently in progress");
        }

        // 3. Acquire Distributed Lock
        Boolean ok = redisTemplate.opsForValue().setIfAbsent(redisKey, "IN_PROGRESS", Duration.ofSeconds(60));
        if (Boolean.FALSE.equals(ok)) throw new IdempotencyConflictException("Concurrent duplicate request detected");

        repository.save(new IdempotencyRecord(idempotencyKey, requestHash, "IN_PROGRESS", Instant.now().plus(24, java.time.temporal.ChronoUnit.HOURS)));
        return null;
    }

    public void completeRecord(String idempotencyKey, String transactionId, Object response) {
        try {
            String json = objectMapper.writeValueAsString(response);
            redisTemplate.opsForValue().set("idempotency:" + idempotencyKey, json, Duration.ofHours(24));
            repository.findById(idempotencyKey).ifPresent(r -> {
                r.setStatus("COMPLETED"); r.setTransactionId(transactionId); r.setResponseData(json);
                repository.save(r);
            });
        } catch (Exception e) { throw new RuntimeException(e); }
    }

    private String computeSha256(Object obj) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256").digest(objectMapper.writeValueAsString(obj).getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) sb.append(String.format("%02x", b));
            return sb.toString();
        } catch (Exception e) { throw new RuntimeException(e); }
    }
}""")

    add_code_block("OutboxPublisherService.java (Transactional Event Poller & Kafka Dispatcher)", """package com.example.httpe.outbox;
import com.example.httpe.entity.OutboxEvent;
import com.example.httpe.kafka.KafkaTopicConfig;
import com.example.httpe.repository.OutboxEventRepository;
import org.springframework.data.domain.PageRequest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import java.time.Instant;
import java.util.List;

@Component
public class OutboxPublisherService {
    private final OutboxEventRepository outboxRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;

    public OutboxPublisherService(OutboxEventRepository outboxRepo, KafkaTemplate<String, String> kafkaTemplate) {
        this.outboxRepository = outboxRepo; this.kafkaTemplate = kafkaTemplate;
    }

    @Scheduled(fixedDelayString = "${httpe.outbox.polling-interval-ms:500}")
    @Transactional
    public void publishPendingOutboxEvents() {
        List<OutboxEvent> pending = outboxRepository.findByStatusOrderByCreatedAtAsc("PENDING", PageRequest.of(0, 100));
        for (OutboxEvent event : pending) {
            kafkaTemplate.send(KafkaTopicConfig.TOPIC_TXN_EVENTS, event.getAggregateId(), event.getPayload())
                .whenComplete((res, ex) -> {
                    if (ex == null) {
                        event.setStatus("PUBLISHED");
                        event.setPublishedAt(Instant.now());
                    } else {
                        event.setRetryCount(event.getRetryCount() + 1);
                        if (event.getRetryCount() > 5) event.setStatus("FAILED");
                    }
                    outboxRepository.save(event);
                });
        }
    }
}""")

    # ================= 5. DOCKER & KUBERNETES CONFIGURATION =================
    story.append(Paragraph("5. Deployment & Orchestration (Docker & Kubernetes)", h1_style))
    story.append(Paragraph("Production container definitions and Kubernetes manifests configured with Horizontal Pod Autoscalers.", body_style))

    add_code_block("docker-compose.yml (Local Full Stack)", """version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: httpe_db
      POSTGRES_USER: httpe_user
      POSTGRES_PASSWORD: httpe_secret
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "1gb", "--maxmemory-policy", "allkeys-lru"]

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports: ["9092:9092"]
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092'
      KAFKA_PROCESS_ROLES: 'broker,controller'
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:29093'
      KAFKA_LISTENERS: 'PLAINTEXT://0.0.0.0:29092,CONTROLLER://0.0.0.0:29093,PLAINTEXT_HOST://0.0.0.0:9092'
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'

  httpe-app:
    build: { context: ., dockerfile: docker/Dockerfile }
    ports: ["8080:8080"]
    environment:
      DB_HOST: postgres
      REDIS_HOST: redis
      KAFKA_BOOTSTRAP_SERVERS: kafka:29092
    depends_on: [postgres, redis, kafka]
volumes: { pgdata: }""")

    add_code_block("k8s/deployment.yaml & HPA", """apiVersion: apps/v1
kind: Deployment
metadata: { name: httpe-deployment }
spec:
  replicas: 12
  selector: { matchLabels: { app: httpe } }
  template:
    metadata: { labels: { app: httpe } }
    spec:
      containers:
      - name: httpe
        image: httpe:1.0.0
        resources:
          requests: { cpu: "2000m", memory: "4Gi" }
          limits: { cpu: "4000m", memory: "6Gi" }
        ports: [{ containerPort: 8080 }]
        readinessProbe: { httpGet: { path: /actuator/health/readiness, port: 8080 }, periodSeconds: 5 }
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: httpe-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: httpe-deployment }
  minReplicas: 8
  maxReplicas: 32
  metrics:
  - type: Resource
    resource: { name: cpu, target: { type: Utilization, averageUtilization: 65 } }""")

    # ================= 6. LOAD TESTING SCRIPTS =================
    story.append(Paragraph("6. High-Throughput Load Testing (k6)", h1_style))
    add_code_block("load-test/k6_load_test.js (1k -> 15k TPS Ramp)", """import http from 'k6/http';
import { check } from 'k6';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export const options = {
  scenarios: {
    ramp_to_12k_tps: {
      executor: 'ramping-arrival-rate',
      startRate: 1000,
      timeUnit: '1s',
      preAllocatedVUs: 500,
      maxVUs: 2000,
      stages: [
        { duration: '30s', target: 2000 },
        { duration: '1m',  target: 6000 },
        { duration: '2m',  target: 12000 },
        { duration: '30s', target: 15000 },
        { duration: '30s', target: 0 }
      ]
    }
  },
  thresholds: {
    http_req_duration: ['p(95)<150', 'p(99)<300'],
    http_req_failed: ['rate<0.001']
  }
};

export default function () {
  const payload = JSON.stringify({
    sourceAccountId: `ACC-${Math.floor(Math.random() * 1000)}`,
    destinationAccountId: `ACC-${Math.floor(Math.random() * 1000) + 1000}`,
    amount: 10.50,
    currency: 'USD'
  });
  const res = http.post('http://localhost:8080/api/v1/transfers', payload, {
    headers: { 'Content-Type': 'application/json', 'Idempotency-Key': uuidv4() }
  });
  check(res, { 'status is 200 or 201': (r) => r.status === 200 || r.status === 201 });
}""")

    # ================= 7. CAPACITY PLANNING =================
    story.append(Paragraph("7. Capacity Planning & Engineering Sizing Model (12,000 TPS)", h1_style))
    calc_data = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>Calculation & Mathematical Basis</b>", body_style), Paragraph("<b>Sizing Metric</b>", body_style)],
        [Paragraph("<b>DB Write IOPS</b>", body_style), Paragraph("12,000 TPS × 5 operations (2 balance updates, 3 inserts)", body_style), Paragraph("<b>60,000 IOPS</b> (10k IOPS/shard × 6 shards)", body_style)],
        [Paragraph("<b>Network Ingress</b>", body_style), Paragraph("12,000 TPS × 400 bytes/request", body_style), Paragraph("<b>38.4 Mbps</b> (4.8 MB/s)", body_style)],
        [Paragraph("<b>Network Egress</b>", body_style), Paragraph("12,000 TPS × 550 bytes/response", body_style), Paragraph("<b>52.8 Mbps</b> (6.6 MB/s)", body_style)],
        [Paragraph("<b>Kafka Volume</b>", body_style), Paragraph("12,000 msgs/sec × 600 bytes JSON", body_style), Paragraph("<b>7.2 MB/s</b> (450 KB/s per partition × 16)", body_style)],
        [Paragraph("<b>Redis Idempotency RAM</b>", body_style), Paragraph("414M daily txns × 300 bytes (24h TTL)", body_style), Paragraph("<b>~124.2 GB</b> (31 GB per node × 4)", body_style)]
    ]
    calc_table = Table(calc_data, colWidths=[110, 240, 154])
    calc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_bg),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(calc_table)
    story.append(Spacer(1, 10))

    # ================= 8. 40+ INTERVIEW QUESTIONS & ANSWERS =================
    story.append(Paragraph("8. Senior Distributed Systems & FinTech Interview Guide (40 Questions)", h1_style))

    qa_list = [
        ("Q1: Why use BigDecimal over double/float in financial ledger applications?",
         "Binary floating-point (IEEE 754) cannot represent base-10 fractions accurately (0.1 + 0.2 != 0.3). BigDecimal provides exact arbitrary-precision arithmetic and explicit rounding control."),
        ("Q2: How does deterministic lock ordering prevent SQL deadlocks under high concurrency?",
         "Deadlocks require circular wait conditions (T1 holds A, waits for B; T2 holds B, waits for A). Enforcing a global total order (e.g. sorting account IDs lexicographically) guarantees all threads acquire row locks in identical sequence."),
        ("Q3: What is the impact of Java thread context switching at 12,000 TPS?",
         "Creating too many OS threads leads to CPU thrashing in kernel context switching. Sizing worker pools to physical cores and keeping transactions sub-millisecond minimizes switch overhead."),
        ("Q4: How do Java 17 Records enhance thread safety in DTOs?",
         "Records are immutable data carriers with final fields, eliminating race conditions on shared objects across concurrent asynchronous worker threads."),
        ("Q5: What is the role of the ZGC / G1GC Garbage Collector in low-latency systems?",
         "Generational ZGC keeps Stop-The-World (STW) pauses below 1ms by performing object marking and relocation concurrently with application threads, preventing p99 latency spikes."),
        ("Q6: How does CompletableFuture avoid thread blocking compared to Future.get()?",
         "CompletableFuture uses event-driven callbacks (thenApply, thenCompose) executed on fork-join pools without holding calling threads in a blocked state."),
        ("Q7: What happens when @Transactional is invoked from another method within the same bean?",
         "Spring uses dynamic proxies. Internal self-invocation calls the raw instance directly, bypassing the transaction interceptor proxy and executing without an active transaction."),
        ("Q8: Why is Isolation.READ_COMMITTED preferred over SERIALIZABLE for 12,000 TPS?",
         "SERIALIZABLE triggers high rollback rates due to serialization anomalies under concurrent access. READ_COMMITTED paired with explicit row-level locking (SELECT FOR UPDATE) provides strict consistency with zero retry thrashing."),
        ("Q9: Why is spring.jpa.open-in-view set to false in high-throughput production?",
         "Disabling OSIV ensures database connections are released immediately after service transactions complete rather than lingering through HTTP serialization."),
        ("Q10: How does Hibernate Optimistic Locking (@Version) work under the hood?",
         "Hibernate adds 'WHERE version = old_version' to UPDATE queries. If another transaction changed the row, update count is 0 and OptimisticLockException is raised."),
        ("Q11: What is HikariCP Connection Leak Detection?",
         "The leakDetectionThreshold timer warns when a thread leases a connection longer than expected, exposing uncommitted transactions or slow blocking I/O inside transaction blocks."),
        ("Q12: When should Propagation.REQUIRES_NEW be used in fintech workflows?",
         "When an operation must commit independently of the outer transaction's rollback status, such as recording security audit logs or incrementing failed attempt counters."),
        ("Q13: What is the difference between partitioning and sharding?",
         "Partitioning divides tables within a single database instance (e.g. Postgres declarative partitions). Sharding splits data across multiple physical database servers."),
        ("Q14: How do you handle cross-shard transfers without Two-Phase Commit (2PC)?",
         "Using asynchronous Sagas or an intermediary settlement account, avoiding blocking distributed locks that degrade throughput."),
        ("Q15: What is Write Amplification in B-Tree indices?",
         "Every row insertion or balance update requires updating index pages on disk. High-write financial ledgers must keep secondary indices minimal."),
        ("Q16: Why are immutable append-only ledgers standard in banking?",
         "Transactions are never updated or deleted; adjustments are performed via compensating credit/debit entries, maintaining a tamper-evident audit history."),
        ("Q17: How does Postgres MVCC avoid read-write lock contention?",
         "Postgres writes new row versions (tuples). Readers view historical snapshots matching their transaction start time without blocking active writers."),
        ("Q18: What is the operational impact of autovacuum at 12,000 TPS?",
         "High update rates generate dead tuples rapidly. Tuning autovacuum with aggressive scale factors is mandatory to prevent table bloat and performance degradation."),
        ("Q19: Why is partition count critical for Kafka consumer parallelism?",
         "In a consumer group, each partition is processed by at most one consumer thread. 16 partitions allow up to 16 parallel consumers in a group."),
        ("Q20: How do you guarantee per-account chronological ordering in Kafka?",
         "By routing all events with partition key = sourceAccountId. All transactions for that account land on the same partition in sequential offset order."),
        ("Q21: What does enable.idempotence=true do on a Kafka Producer?",
         "Assigns a Producer ID (PID) and sequence numbers to messages, transparently deduplicating messages sent due to network retries."),
        ("Q22: What is Kafka Consumer Lag and how is it monitored?",
         "The difference between the latest offset written by producers and the current offset committed by consumers, monitored via Prometheus metric kafka_consumergroup_lag."),
        ("Q23: How does a Dead Letter Queue (DLQ) protect consumer pipelines?",
         "Poison-pill messages that fail repeatedly are routed to a DLQ topic after N retries, unblocking the partition for subsequent messages."),
        ("Q24: Why does the Transactional Outbox Pattern solve the dual-write problem?",
         "It saves events in a local database table within the same ACID transaction as the business entity, eliminating partial failures where DB commits but message dispatch fails."),
        ("Q25: Why should mutable account balances NEVER be cached in Redis?",
         "Concurrent cache invalidation race conditions cause stale reads and potential double-spending. Balances must always be checked and locked against authoritative database shards."),
        ("Q26: How does Redis SET key val NX EX implement a distributed lock?",
         "NX ensures atomic creation only if the key doesn't exist; EX provides automatic TTL expiration to prevent permanent deadlocks if the holder crashes."),
        ("Q27: What is Cache Stampede and how is it mitigated?",
         "When a hot cached key expires and thousands of requests query the DB simultaneously. Mitigated using mutex locking, probabilistic early expiration, or background pre-warming."),
        ("Q28: What is Redis allkeys-lru memory eviction policy?",
         "When RAM limits are reached, Redis evicts the Least Recently Used keys across the entire dataset to accommodate new writes."),
        ("Q29: How does Lettuce Netty pooling improve throughput over Jedis?",
         "Lettuce uses non-blocking asynchronous Netty channels, allowing multiple threads to share single connections via pipelining without thread blocking."),
        ("Q30: Why are Redis Lua scripts atomic?",
         "Redis executes Lua scripts on its single-threaded event loop without interruption, ensuring multi-step read-modify-write operations are race-free."),
        ("Q31: How does the CAP theorem apply to HTTPE?",
         "During network partitions (P), financial ledger engines choose Consistency (C) over Availability (A), rejecting ambiguous transfers to prevent balance divergence."),
        ("Q32: What is the difference between at-least-once and exactly-once delivery?",
         "At-least-once guarantees no message loss but allows duplicates. Exactly-once requires at-least-once transport combined with idempotent deduplication at the consumer."),
        ("Q33: What is a Circuit Breaker and how does it prevent cascading failures?",
         "It tracks failure rates to downstream dependencies; when errors exceed thresholds, it trips open to fail fast without exhausting application thread pools."),
        ("Q34: Why is exponential backoff with jitter necessary for retries?",
         "Adding random jitter breaks synchronization among retrying clients, preventing the 'thundering herd' overload on recovering services."),
        ("Q35: What is Distributed Tracing (Trace ID / Span ID)?",
         "A unique Trace ID passed in headers across HTTP and Kafka metadata to trace a request's lifecycle across microservices in Grafana/Jaeger."),
        ("Q36: What is Graceful Shutdown in Spring Boot?",
         "The app stops accepting new HTTP connections and allows active requests and Kafka listeners to complete before shutting down DB pools."),
        ("Q37: Why is p99 latency more important than average latency in fintech?",
         "Average latency hides severe outliers. A low average of 15ms can mask that 1 in 100 high-value customers experiences a 3-second timeout."),
        ("Q38: How do you identify connection pool starvation in HikariCP?",
         "By alerting on hikaricp_pending_connection_requests and connection acquisition timeout rates in Prometheus."),
        ("Q39: What is the overhead of synchronous logging under high load?",
         "Synchronous disk I/O blocks worker threads. High-throughput engines use asynchronous log appenders with ring buffers (Logback AsyncAppender)."),
        ("Q40: How do you benchmark 12,000+ TPS without client-side bottlenecks?",
         "By distributing load generators across multiple physical nodes and measuring server-side latency histograms rather than client-perceived response times.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    story.append(Spacer(1, 8))

    # ================= 9. INTERVIEW PITCHES & RESUME =================
    story.append(Paragraph("9. Interview Pitch Deck & Resume Descriptions", h1_style))
    story.append(Paragraph(
        "<b>30-Second Elevator Pitch:</b><br/>"
        "<i>'HTTPE is an ACID-compliant distributed transaction engine engineered for 12,000+ TPS. It resolves the classic trade-off between throughput and financial correctness "
        "by utilizing deterministic row-level locking to eliminate deadlocks, a two-tier idempotency barrier to prevent double-spending, and the Transactional Outbox pattern "
        "to guarantee zero event loss to Kafka.'</i>",
        body_style
    ))
    story.append(Paragraph(
        "<b>Resume Bullet Points:</b><br/>"
        "• <b>Architected High-Throughput Transaction Processing Engine (HTTPE)</b> designed for 12,000+ TPS using Java 17, Spring Boot 3, PostgreSQL, Redis, and Apache Kafka.<br/>"
        "• <b>Implemented ACID-compliant financial balance transfers</b> utilizing deterministic row-level locking (`SELECT ... FOR UPDATE`), eliminating concurrency deadlocks and double debits.<br/>"
        "• <b>Engineered zero-loss event streaming pipeline</b> with the Transactional Outbox Pattern and Kafka retry/DLQ topics across 16 partitions.<br/>"
        "• <b>Built a two-tier idempotency barrier</b> in Redis and PostgreSQL, ensuring exactly-once execution semantics under heavy network retry storms.<br/>"
        "• <b>Constructed Prometheus/Grafana observability suites</b> and automated k6 load-testing scenarios validating p95 latencies under 150ms.",
        body_style
    ))

    # Build the PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Expanded PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\Admin\OneDrive\Desktop\Alpha_Qspider\httpe"
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, "HTTPE_Complete_Architecture_and_Project.pdf")
    create_httpe_pdf(out_pdf)
