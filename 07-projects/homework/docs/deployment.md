````markdown
# Deployment Guide

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Deployment Model:** Docker Compose (Primary), Kubernetes (Future), Cloud Ready

---

# Table of Contents

- Introduction
- Deployment Goals
- Supported Deployment Options
- Production Architecture
- Infrastructure Requirements
- Prerequisites
- Environment Variables
- Docker Compose Deployment
- Local Development Deployment
- Production Deployment
- Cloud Deployment
- Reverse Proxy
- SSL Configuration
- Monitoring Stack
- Scaling Strategy
- Backup Strategy
- Disaster Recovery
- Logging
- Security
- CI/CD Pipeline
- Health Checks
- Performance Tuning
- Troubleshooting
- Future Enhancements

---

# Introduction

This document describes how to deploy **Tech Knowledge Navigator** in local, staging, and production environments.

The project has been designed with portability in mind, enabling deployment on:

- Local development machine
- Docker Compose
- Virtual Machines
- Cloud Infrastructure
- Kubernetes (future release)

The primary deployment mechanism for this project is **Docker Compose**, ensuring a fully reproducible environment that satisfies the LLM Zoomcamp evaluation criteria.

---

# Deployment Goals

The deployment architecture is designed to achieve the following objectives:

- One-command deployment
- Fully containerized services
- Independent service scaling
- Environment-based configuration
- Easy reproducibility
- Monitoring and observability
- Secure secret management
- Cloud portability

---

# Supported Deployment Options

| Environment           | Status         |
| --------------------- | -------------- |
| Local Machine         | ✅ Supported   |
| Docker Compose        | ✅ Recommended |
| Ubuntu VM             | ✅ Supported   |
| AWS EC2               | ✅ Supported   |
| Azure VM              | ✅ Supported   |
| Google Compute Engine | ✅ Supported   |
| Kubernetes            | 🚧 Planned     |
| AWS ECS               | 🚧 Planned     |
| Azure Container Apps  | 🚧 Planned     |

---

# Production Architecture

```text
                    Internet
                        │
                        ▼
                Nginx Reverse Proxy
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 Streamlit UI      FastAPI Backend    Grafana
                        │
                        ▼
                Retrieval Service
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  PostgreSQL      OpenSearch       Qdrant
                        │
                        ▼
                  Prefect Worker
                        │
                        ▼
                 Knowledge Sources

Monitoring Stack

Prometheus
     │
     ▼
 Grafana
```

---

# Infrastructure Requirements

## Minimum Configuration

| Component      | Specification |
| -------------- | ------------- |
| CPU            | 4 Cores       |
| RAM            | 8 GB          |
| Storage        | 50 GB SSD     |
| OS             | Ubuntu 22.04+ |
| Docker         | 24+           |
| Docker Compose | v2            |

---

## Recommended Configuration

| Component | Specification |
| --------- | ------------- |
| CPU       | 8 Cores       |
| RAM       | 16 GB         |
| Storage   | 200 GB SSD    |
| Docker    | Latest        |
| GPU       | Optional      |

---

# Prerequisites

Install the following software before deployment.

- Docker Engine
- Docker Compose
- Git
- Python 3.12 (optional for local development)

Verify installation.

```bash
docker --version

docker compose version

git --version
```

---

# Repository Setup

Clone the repository.

```bash
git clone https://github.com/<username>/tech-knowledge-navigator.git

cd tech-knowledge-navigator
```

---

# Environment Variables

Create an environment file.

```bash
cp .env.example .env
```

Example:

```env
APP_ENV=production

API_HOST=0.0.0.0

API_PORT=8000

STREAMLIT_PORT=8501

POSTGRES_USER=rag_user

POSTGRES_PASSWORD=password

POSTGRES_DB=rag_db

POSTGRES_PORT=5432

QDRANT_HOST=qdrant

QDRANT_PORT=6333

OPENSEARCH_HOST=opensearch

OPENSEARCH_PORT=9200

OPENAI_API_KEY=<your-api-key>

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

LLM_PROVIDER=openai

PROMETHEUS_PORT=9090

GRAFANA_PORT=3000
```

Never commit the `.env` file to source control.

---

# Docker Compose Deployment

The application is fully containerized.

Directory structure:

```text
docker/

docker-compose.yml

Dockerfile.api

Dockerfile.ui

Dockerfile.ingestion
```

Start the complete platform.

```bash
docker compose up --build
```

Run in detached mode.

```bash
docker compose up -d
```

View running containers.

```bash
docker compose ps
```

Stop services.

```bash
docker compose down
```

Remove all volumes.

```bash
docker compose down -v
```

---

# Docker Services

The deployment consists of the following containers.

| Service        | Port     |
| -------------- | -------- |
| FastAPI        | 8000     |
| Streamlit      | 8501     |
| PostgreSQL     | 5432     |
| OpenSearch     | 9200     |
| Qdrant         | 6333     |
| Prefect Worker | Internal |
| Prometheus     | 9090     |
| Grafana        | 3000     |

---

# Container Startup Order

```text
PostgreSQL

↓

OpenSearch

↓

Qdrant

↓

Prefect

↓

FastAPI

↓

Streamlit

↓

Prometheus

↓

Grafana
```

Service dependencies are managed through Docker Compose health checks.

---

# Local Development Deployment

Install dependencies.

```bash
pip install -r requirements.txt
```

Run FastAPI.

```bash
uvicorn app.main:app --reload
```

Run Streamlit.

```bash
streamlit run ui/Home.py
```

Run Prefect worker.

```bash
prefect worker start
```

---

# Production Deployment

Recommended deployment steps.

## Step 1

Clone repository.

## Step 2

Configure environment variables.

## Step 3

Build containers.

```bash
docker compose build
```

## Step 4

Start services.

```bash
docker compose up -d
```

## Step 5

Run ingestion.

```bash
python scripts/run_ingestion.py
```

## Step 6

Verify health.

```bash
curl http://localhost:8000/health
```

---

# Cloud Deployment

The application can be deployed to any cloud platform supporting Docker.

Supported platforms include:

- AWS EC2
- Azure Virtual Machines
- Google Compute Engine
- DigitalOcean Droplets
- Oracle Cloud Compute

Typical workflow:

```text
Provision VM

↓

Install Docker

↓

Clone Repository

↓

Configure Environment

↓

Docker Compose Up

↓

Run Ingestion

↓

Configure Reverse Proxy

↓

Enable HTTPS
```

---

# Reverse Proxy

Nginx is recommended for production deployments.

Responsibilities:

- SSL termination
- Static content
- Compression
- Security headers
- Request forwarding

Typical routing:

```text
https://example.com

↓

Nginx

↓

FastAPI

↓

Streamlit
```

---

# SSL Configuration

HTTPS should be enabled for all production deployments.

Recommended options:

- Let's Encrypt
- Cloudflare SSL
- AWS ACM
- Azure Managed Certificates

All API traffic should be encrypted in transit.

---

# Monitoring Stack

Prometheus collects metrics from all services.

Grafana visualizes dashboards.

Metrics include:

- API requests
- Response latency
- LLM latency
- Retrieval latency
- Token usage
- CPU usage
- Memory usage
- Error rate
- User feedback

Access dashboards.

```text
Prometheus

http://localhost:9090

Grafana

http://localhost:3000
```

---

# Scaling Strategy

Current deployment supports horizontal scaling.

```text
               Load Balancer

                     │

      ┌──────────────┼──────────────┐

      ▼              ▼              ▼

 FastAPI-1      FastAPI-2      FastAPI-3

      │

      ▼

 Shared OpenSearch

 Shared Qdrant

 Shared PostgreSQL
```

Stateless application containers make horizontal scaling straightforward.

---

# Backup Strategy

Critical data includes:

- PostgreSQL database
- OpenSearch indexes
- Qdrant collections
- Uploaded documents
- Configuration files

Recommended backup frequency:

| Component      | Frequency |
| -------------- | --------- |
| PostgreSQL     | Daily     |
| Qdrant         | Daily     |
| OpenSearch     | Daily     |
| Uploaded Files | Daily     |
| Configuration  | On Change |

---

# Disaster Recovery

Recovery steps:

1. Restore database.
2. Restore vector database.
3. Restore OpenSearch indexes.
4. Restore uploaded documents.
5. Redeploy containers.
6. Verify ingestion metadata.
7. Execute health checks.

---

# Logging

Application logs are written in structured JSON.

Log levels:

- INFO
- WARNING
- ERROR
- DEBUG

Logs include:

- Request ID
- Response Time
- API Endpoint
- User Feedback
- Retrieval Time
- LLM Latency
- Error Details

---

# Security

Recommended production practices.

- HTTPS only
- Environment variables for secrets
- Disable debug mode
- Strong PostgreSQL credentials
- Firewall configuration
- Reverse proxy
- Rate limiting
- Input validation
- Regular dependency updates

Future enhancements:

- JWT Authentication
- OAuth2
- Role-Based Access Control
- API Keys
- Secrets Manager Integration

---

# CI/CD Pipeline

Recommended deployment pipeline.

```text
Git Push

↓

GitHub Actions

↓

Run Tests

↓

Build Docker Images

↓

Security Scan

↓

Push Images

↓

Deploy

↓

Smoke Tests

↓

Production
```

Suggested quality gates:

- Unit tests
- Integration tests
- Linting
- Dependency vulnerability scan
- Container image scan

---

# Health Checks

Verify application health.

FastAPI

```bash
curl http://localhost:8000/health
```

Swagger

```text
http://localhost:8000/docs
```

Streamlit

```text
http://localhost:8501
```

Prometheus

```text
http://localhost:9090
```

Grafana

```text
http://localhost:3000
```

---

# Performance Tuning

Production recommendations.

- Increase OpenSearch heap size
- Enable PostgreSQL connection pooling
- Use SSD storage
- Cache embeddings
- Configure request timeouts
- Enable gzip compression
- Tune worker count based on CPU cores
- Optimize chunk size for retrieval performance

---

# Troubleshooting

## Containers Not Starting

```bash
docker compose logs
```

---

## Restart Services

```bash
docker compose restart
```

---

## Rebuild Images

```bash
docker compose build --no-cache
```

---

## Remove All Containers

```bash
docker compose down -v
```

---

## Verify Docker Resources

```bash
docker system df
```

---

# Future Enhancements

Planned deployment improvements include:

- Kubernetes manifests
- Helm charts
- Terraform infrastructure
- GitOps with ArgoCD
- Blue/Green deployments
- Canary releases
- OpenTelemetry tracing
- Service mesh integration
- Multi-region deployment
- High Availability PostgreSQL
- Managed OpenSearch cluster
- Managed Qdrant cluster

---

# Related Documentation

- `docs/setup.md`
- `docs/architecture.md`
- `docs/api.md`
- `docs/monitoring.md`
- `docs/evaluation.md`
- `docs/security.md`

---

# Deployment Checklist

| Task                             | Status |
| -------------------------------- | ------ |
| Docker Installed                 | ✅     |
| Docker Compose Installed         | ✅     |
| Repository Cloned                | ✅     |
| Environment Variables Configured | ✅     |
| Containers Built                 | ✅     |
| Services Running                 | ✅     |
| Health Checks Passed             | ✅     |
| Initial Ingestion Completed      | ✅     |
| Monitoring Enabled               | ✅     |
| Dashboards Accessible            | ✅     |
| Backup Strategy Configured       | ✅     |

---

## Deployment Summary

Tech Knowledge Navigator is designed as a fully containerized, cloud-ready RAG platform. The Docker Compose deployment provides a reproducible environment for local development, demonstrations, and production-like testing, while the architecture supports future migration to Kubernetes and managed cloud services. Built-in monitoring, health checks, backup strategies, and deployment best practices ensure that the platform is reliable, maintainable, and aligned with modern DevOps practices as well as the LLM Zoomcamp evaluation criteria.
````
