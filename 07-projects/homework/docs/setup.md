````markdown
# Setup Guide

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Document Version:** 1.0

---

# Table of Contents

- Introduction
- System Requirements
- Technology Stack
- Repository Structure
- Prerequisites
- Clone Repository
- Environment Variables
- Docker Installation
- Local Development Setup
- Database Setup
- OpenSearch Setup
- Qdrant Setup
- Backend Setup
- Frontend Setup
- Prefect Setup
- Monitoring Setup
- Running the Complete Stack
- Verifying Installation
- Sample Test
- Troubleshooting
- Useful Commands

---

# Introduction

This document explains how to set up **Tech Knowledge Navigator** for local development and production deployment.

After completing this guide, you will have a fully working Retrieval-Augmented Generation (RAG) system consisting of:

- FastAPI Backend
- Streamlit Frontend
- PostgreSQL
- OpenSearch
- Qdrant
- Prefect
- Prometheus
- Grafana

Everything can be started with a single Docker Compose command.

---

# System Requirements

Minimum Requirements

| Component      | Requirement             |
| -------------- | ----------------------- |
| CPU            | 4 Cores                 |
| RAM            | 8 GB                    |
| Storage        | 20 GB                   |
| OS             | Linux / macOS / Windows |
| Docker         | Latest                  |
| Docker Compose | Latest                  |

Recommended

| Component | Recommendation |
| --------- | -------------- |
| CPU       | 8 Cores        |
| RAM       | 16 GB          |
| SSD       | 50 GB          |

---

# Technology Stack

| Layer         | Technology  |
| ------------- | ----------- |
| Language      | Python 3.12 |
| Backend       | FastAPI     |
| Frontend      | Streamlit   |
| Vector DB     | Qdrant      |
| Search Engine | OpenSearch  |
| Database      | PostgreSQL  |
| Workflow      | Prefect     |
| Monitoring    | Prometheus  |
| Dashboard     | Grafana     |
| Container     | Docker      |

---

# Repository Structure

```text
tech-knowledge-navigator/

├── backend/
├── frontend/
├── ingestion/
├── evaluation/
├── monitoring/
├── docker/
├── docs/
├── tests/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Prerequisites

Install the following software.

## Python

```
Python 3.12+
```

Verify

```bash
python --version
```

---

## Git

```bash
git --version
```

---

## Docker

```bash
docker --version
```

---

## Docker Compose

```bash
docker compose version
```

---

# Clone Repository

```bash
git clone https://github.com/your-username/tech-knowledge-navigator.git

cd tech-knowledge-navigator
```

---

# Environment Variables

Copy

```bash
cp .env.example .env
```

Example

```env
############################################

# Application

############################################

APP_NAME=Tech Knowledge Navigator

APP_ENV=development

DEBUG=true

############################################

# OpenAI

############################################

OPENAI_API_KEY=your_openai_key

############################################

# PostgreSQL

############################################

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_DB=ragdb

POSTGRES_HOST=postgres

POSTGRES_PORT=5432

############################################

# OpenSearch

############################################

OPENSEARCH_HOST=opensearch

OPENSEARCH_PORT=9200

############################################

# Qdrant

############################################

QDRANT_HOST=qdrant

QDRANT_PORT=6333

############################################

# Grafana

############################################

GRAFANA_ADMIN_PASSWORD=admin

############################################

# Prometheus

############################################

PROMETHEUS_PORT=9090
```

---

# Install Python Dependencies

Backend

```bash
cd backend

pip install -r requirements.txt
```

Frontend

```bash
cd ../frontend

pip install -r requirements.txt
```

---

# Docker Installation

Verify Docker

```bash
docker ps
```

Expected

```
CONTAINER ID

IMAGE

STATUS
```

---

# Database Setup

Start PostgreSQL

```bash
docker compose up postgres -d
```

Verify

```bash
docker ps
```

Database

```
ragdb
```

---

# OpenSearch Setup

Start

```bash
docker compose up opensearch -d
```

Verify

```bash
curl http://localhost:9200
```

Expected

```json
{
  "cluster_name": "docker-cluster"
}
```

---

# Qdrant Setup

Start

```bash
docker compose up qdrant -d
```

Verify

```bash
curl http://localhost:6333
```

Expected

```json
{
  "title": "qdrant"
}
```

---

# Backend Setup

Navigate

```bash
cd backend
```

Install

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

Open

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate

```bash
cd frontend
```

Run

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# Prefect Setup

Start Prefect Server

```bash
prefect server start
```

Open

```
http://localhost:4200
```

Deploy ingestion flow

```bash
python ingestion/deploy.py
```

Run

```bash
python ingestion/run.py
```

---

# Monitoring Setup

Start monitoring stack

```bash
docker compose up prometheus grafana -d
```

Prometheus

```
http://localhost:9090
```

Grafana

```
http://localhost:3000
```

Default Login

```
Username

admin

Password

admin
```

---

# Running the Complete Stack

The easiest way to start the entire application is with Docker Compose.

```bash
docker compose up --build
```

Run in background

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

Remove volumes

```bash
docker compose down -v
```

---

# Service URLs

| Service    | URL                        |
| ---------- | -------------------------- |
| Streamlit  | http://localhost:8501      |
| FastAPI    | http://localhost:8000      |
| Swagger    | http://localhost:8000/docs |
| PostgreSQL | localhost:5432             |
| OpenSearch | http://localhost:9200      |
| Qdrant     | http://localhost:6333      |
| Grafana    | http://localhost:3000      |
| Prometheus | http://localhost:9090      |
| Prefect    | http://localhost:4200      |

---

# Initial Data Ingestion

Run the ingestion pipeline.

```bash
python ingestion/run_ingestion.py
```

The pipeline will

- Load dataset
- Clean documents
- Chunk text
- Generate embeddings
- Store metadata
- Index OpenSearch
- Index Qdrant

---

# Verify Installation

Health Check

```bash
curl http://localhost:8000/health
```

Expected

```json
{
  "status": "UP"
}
```

---

Retrieve API

```bash
curl -X POST http://localhost:8000/api/v1/chat \
-H "Content-Type: application/json" \
-d '{
  "query":"Explain Kafka Consumer Groups"
}'
```

Expected

```json
{
  "answer": "...",
  "sources": []
}
```

---

# Sample Workflow

```text
Clone Repository

↓

Configure .env

↓

docker compose up

↓

Run Ingestion

↓

Open Streamlit

↓

Ask Questions

↓

Monitor Grafana
```

---

# Troubleshooting

## Docker not running

Verify

```bash
docker ps
```

Restart Docker Desktop.

---

## OpenSearch unhealthy

Increase Docker memory to at least

```
4 GB
```

---

## Backend cannot connect to PostgreSQL

Check

```bash
docker ps
```

Ensure PostgreSQL container is running.

---

## Embedding generation fails

Verify

```
OPENAI_API_KEY
```

or

Ensure local embedding model is downloaded.

---

## Qdrant connection refused

Verify

```bash
curl http://localhost:6333
```

---

## Grafana cannot connect

Restart

```bash
docker compose restart grafana
```

---

# Useful Commands

Rebuild containers

```bash
docker compose build
```

Restart

```bash
docker compose restart
```

View logs

```bash
docker compose logs -f
```

Backend logs

```bash
docker compose logs backend
```

Frontend logs

```bash
docker compose logs frontend
```

Stop everything

```bash
docker compose down
```

Remove all containers and volumes

```bash
docker compose down -v
```

---

# Development Workflow

```text
Clone Repository

↓

Install Dependencies

↓

Configure Environment

↓

Start Docker Services

↓

Run Ingestion Pipeline

↓

Start Backend

↓

Start Frontend

↓

Evaluate Retrieval

↓

Monitor Metrics

↓

Commit Changes
```

---

# Recommended Development Tools

| Tool                  | Purpose               |
| --------------------- | --------------------- |
| VS Code               | Code Editor           |
| Docker Desktop        | Container Runtime     |
| Postman               | API Testing           |
| pgAdmin               | PostgreSQL Management |
| OpenSearch Dashboards | Search Inspection     |
| Grafana               | Monitoring            |
| Git                   | Version Control       |

---

# Related Documentation

- `README.md`
- `architecture.md`
- `deployment.md`
- `api.md`
- `dataset.md`
- `monitoring.md`
- `retrieval.md`
- `rag-pipeline.md`

---

# Conclusion

After following this guide, you will have a complete local development environment for **Tech Knowledge Navigator**. The application includes a fully configured hybrid RAG pipeline, automated ingestion workflow, monitoring stack, REST API, and user interface. The setup is reproducible using Docker Compose and is suitable for both development and demonstration purposes, satisfying the reproducibility and containerization requirements of the LLM Zoomcamp project.
````
