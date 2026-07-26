````markdown
# Monitoring & Observability

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Monitoring Stack:** Prometheus + Grafana + Loki + Alertmanager + OpenTelemetry (Future)

---

# Table of Contents

- Introduction
- Monitoring Objectives
- Monitoring Architecture
- Monitoring Stack
- Application Metrics
- Retrieval Metrics
- LLM Metrics
- User Feedback Metrics
- Infrastructure Metrics
- Grafana Dashboards
- Prometheus Configuration
- Logging
- Alerting
- Health Checks
- Business Metrics
- Error Tracking
- Distributed Tracing
- Performance Monitoring
- Security Monitoring
- Monitoring Workflow
- Zoomcamp Evaluation Mapping
- Future Improvements

---

# Introduction

Monitoring is a critical component of any production-grade AI application. Unlike traditional web applications, Retrieval-Augmented Generation (RAG) systems require visibility into every stage of the request lifecycle, including retrieval quality, LLM performance, token usage, latency, infrastructure health, and user satisfaction.

Tech Knowledge Navigator implements a comprehensive monitoring solution to ensure the application remains reliable, observable, and continuously improving.

---

# Monitoring Objectives

The monitoring solution has the following objectives:

- Monitor application availability
- Measure API performance
- Monitor retrieval quality
- Track LLM latency
- Measure token consumption
- Detect failures
- Collect user feedback
- Monitor infrastructure health
- Support capacity planning
- Enable troubleshooting

---

# Monitoring Architecture

```text
                        User
                          │
                          ▼
                    Streamlit UI
                          │
                          ▼
                     FastAPI API
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Retrieval Metrics    LLM Metrics      Application Metrics
      │                   │                   │
      └───────────────────┼───────────────────┘
                          ▼
                 Prometheus Exporter
                          │
                          ▼
                    Prometheus Server
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
     Grafana         Alertmanager        Loki
         │
         ▼
     Dashboards
```

---

# Monitoring Stack

The monitoring platform consists of the following components.

| Component     | Purpose                      |
| ------------- | ---------------------------- |
| Prometheus    | Metrics Collection           |
| Grafana       | Dashboards                   |
| Loki          | Centralized Logging          |
| Alertmanager  | Notifications                |
| OpenTelemetry | Distributed Tracing (Future) |

---

# Metrics Categories

Metrics are grouped into six categories:

- Application Metrics
- Retrieval Metrics
- LLM Metrics
- Infrastructure Metrics
- User Metrics
- Business Metrics

---

# Application Metrics

Application-level metrics measure the health and performance of the FastAPI service.

## Request Count

Metric

```
http_requests_total
```

Measures:

- Total requests
- Requests per endpoint
- Requests by method

Example

```
GET /chat

POST /search

GET /health
```

---

## Request Latency

Metric

```
http_request_duration_seconds
```

Measures:

- Average latency
- Maximum latency
- P95 latency
- P99 latency

Target

```
< 300 ms
```

---

## Error Rate

Metric

```
http_errors_total
```

Monitors

- 4xx responses
- 5xx responses
- Validation failures
- Unexpected exceptions

---

## Active Users

Metric

```
active_sessions
```

Tracks

- Active chat sessions
- Connected users
- Daily active users

---

# Retrieval Metrics

Hybrid retrieval performance is monitored continuously.

---

## Search Latency

Metric

```
retrieval_duration_seconds
```

Measures

- BM25 latency
- Vector search latency
- RRF latency
- Re-ranking latency

---

## Documents Retrieved

Metric

```
retrieved_documents_total
```

Tracks

- Number of retrieved chunks
- Number of filtered chunks
- Final context size

---

## Search Strategy Usage

Metric

```
retrieval_strategy_total
```

Example labels

```
bm25

vector

hybrid

hybrid_rerank
```

---

## Query Rewrite Success

Metric

```
query_rewrite_total
```

Measures

- Queries rewritten
- Rewrite failures
- Average rewrite latency

---

# LLM Metrics

The application tracks model performance.

---

## LLM Requests

Metric

```
llm_requests_total
```

Measures

- Requests per provider
- Model usage
- Provider distribution

---

## LLM Latency

Metric

```
llm_response_duration_seconds
```

Target

```
< 1000 ms
```

---

## Token Usage

Metric

```
llm_tokens_total
```

Tracks

- Prompt Tokens
- Completion Tokens
- Total Tokens

---

## Cost Estimation

Metric

```
llm_cost_total
```

Measures

- Daily cost
- Monthly cost
- Cost per request

---

## Hallucination Reports

Metric

```
hallucination_reports_total
```

Collected through:

- User feedback
- Evaluation pipeline
- Manual review

---

# User Feedback Metrics

User feedback is collected after every conversation.

Feedback options

- 👍 Helpful
- 👎 Not Helpful
- Rating (1–5)
- Free-text comments

---

## Feedback Score

Metric

```
user_rating_average
```

Target

```
≥ 4.5
```

---

## Feedback Distribution

Metric

```
feedback_total
```

Example

| Rating | Count |
| ------ | ----- |
| 5      | 1240  |
| 4      | 438   |
| 3      | 102   |
| 2      | 18    |
| 1      | 6     |

---

# Infrastructure Metrics

Infrastructure monitoring ensures platform stability.

---

## CPU Usage

Metric

```
container_cpu_usage
```

Target

```
< 75%
```

---

## Memory Usage

Metric

```
container_memory_usage
```

Target

```
< 80%
```

---

## Disk Usage

Metric

```
disk_usage
```

Target

```
< 85%
```

---

## Container Health

Metrics

```
container_up

container_restart_total
```

---

# Grafana Dashboards

The project includes multiple dashboards.

---

## Dashboard 1

### Application Overview

Charts

- Total Requests
- Active Users
- Response Time
- Error Rate
- Throughput

---

## Dashboard 2

### Retrieval Dashboard

Charts

- BM25 Latency
- Vector Search Latency
- Hybrid Search Latency
- Documents Retrieved
- Re-ranking Latency

---

## Dashboard 3

### LLM Dashboard

Charts

- Requests
- Latency
- Tokens
- Cost
- Model Distribution

---

## Dashboard 4

### Infrastructure Dashboard

Charts

- CPU
- Memory
- Disk
- Containers
- Network

---

## Dashboard 5

### User Feedback Dashboard

Charts

- User Ratings
- Feedback Trend
- Hallucination Reports
- Average Rating
- Satisfaction Score

---

# Dashboard Summary

| Dashboard      | Charts |
| -------------- | ------ |
| Application    | 5      |
| Retrieval      | 5      |
| LLM            | 5      |
| Infrastructure | 5      |
| Feedback       | 5      |

**Total Charts: 25**

This exceeds the LLM Zoomcamp requirement of **at least five charts**.

---

# Prometheus Configuration

Prometheus scrapes metrics from all application services.

Example configuration

```yaml
scrape_configs:
  - job_name: "fastapi"
    metrics_path: "/metrics"
    static_configs:
      - targets:
          - fastapi:8000
```

Scrape interval

```yaml
15s
```

---

# Logging

Structured JSON logging is used throughout the application.

Example

```json
{
  "timestamp": "2026-07-26T10:00:00Z",
  "level": "INFO",
  "requestId": "abc123",
  "endpoint": "/chat",
  "latencyMs": 842,
  "status": 200
}
```

Logs include

- Request ID
- Session ID
- User Query
- Retrieval Time
- LLM Time
- Response Time
- Error Messages

---

# Alerting

Alertmanager sends notifications when thresholds are exceeded.

Example alerts

| Alert           | Threshold           |
| --------------- | ------------------- |
| API Down        | Service unavailable |
| CPU High        | > 85%               |
| Memory High     | > 90%               |
| High Error Rate | > 5%                |
| LLM Latency     | > 3 sec             |
| Search Failure  | > 2%                |
| Disk Full       | > 90%               |

Notification channels

- Email
- Slack
- Microsoft Teams
- Webhook

---

# Health Checks

FastAPI exposes health endpoints.

```text
GET /health

GET /health/live

GET /health/ready
```

Each service also reports its own health status.

Example

```json
{
  "status": "UP",
  "postgres": "UP",
  "opensearch": "UP",
  "qdrant": "UP",
  "llm": "UP"
}
```

---

# Business Metrics

Business metrics help understand application adoption.

Metrics include

- Daily Active Users
- Weekly Active Users
- Monthly Active Users
- Queries Per Day
- Average Session Length
- Average Conversation Length
- Returning Users
- Most Popular Technologies

---

# Error Tracking

Errors are categorized by type.

| Category       | Examples               |
| -------------- | ---------------------- |
| Validation     | Invalid requests       |
| Retrieval      | Search failures        |
| Database       | PostgreSQL unavailable |
| Vector DB      | Qdrant errors          |
| OpenSearch     | Index unavailable      |
| LLM            | API failures           |
| Infrastructure | Container failures     |

Each error contains

- Request ID
- Stack Trace
- User Session
- Endpoint
- Timestamp

---

# Distributed Tracing

Future versions will integrate OpenTelemetry.

Tracing will include

```text
User Request

↓

FastAPI

↓

Retrieval

↓

OpenSearch

↓

Qdrant

↓

LLM

↓

Response
```

Benefits

- End-to-end visibility
- Latency breakdown
- Root cause analysis

---

# Performance Monitoring

The application continuously measures:

| Metric         | Target    |
| -------------- | --------- |
| API Latency    | < 300 ms  |
| Search Latency | < 200 ms  |
| LLM Response   | < 1000 ms |
| Availability   | 99.9%     |
| Error Rate     | < 1%      |
| User Rating    | > 4.5     |

---

# Security Monitoring

Security metrics include

- Failed authentication attempts
- Rate limit violations
- Suspicious traffic
- Invalid API requests
- Container restarts
- Unauthorized access attempts

Future releases will integrate with SIEM platforms.

---

# Monitoring Workflow

```text
Application

↓

Metrics

↓

Prometheus

↓

Grafana

↓

Dashboards

↓

Alerts

↓

Engineers
```

---

# Zoomcamp Evaluation Mapping

| Zoomcamp Requirement      | Implementation                    |
| ------------------------- | --------------------------------- |
| User Feedback Collection  | Chat feedback, ratings, comments  |
| Monitoring Dashboard      | Grafana                           |
| At Least 5 Charts         | 25 charts across 5 dashboards     |
| Retrieval Monitoring      | Search latency, retrieval metrics |
| LLM Monitoring            | Tokens, latency, costs            |
| Infrastructure Monitoring | CPU, Memory, Disk, Containers     |

---

# Future Improvements

Planned enhancements include:

- OpenTelemetry tracing
- Jaeger integration
- AI-powered anomaly detection
- Predictive capacity planning
- SLO and SLA dashboards
- Kubernetes monitoring
- Cloud-native observability
- Log correlation
- User journey analytics
- Real-time cost optimization

---

# Related Documentation

- `docs/architecture.md`
- `docs/evaluation.md`
- `docs/api.md`
- `docs/deployment.md`
- `docs/rag-pipeline.md`

---

# Monitoring Summary

The monitoring solution for Tech Knowledge Navigator provides comprehensive observability across the entire RAG lifecycle. By combining Prometheus, Grafana, structured logging, and user feedback, the platform continuously measures application health, retrieval quality, LLM performance, infrastructure utilization, and user satisfaction. The monitoring implementation exceeds the LLM Zoomcamp project requirements by collecting user feedback and providing multiple dashboards with more than 25 visualizations, enabling proactive operations and continuous improvement.
````
