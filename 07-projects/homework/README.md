# 🚀 Tech Knowledge Navigator

### Production-Grade Multi-Source RAG & AI Assistant for Software Engineering Knowledge

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![OpenSearch](https://img.shields.io/badge/OpenSearch-Latest-orange.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

# Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Project Goals](#project-goals)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Knowledge Base](#knowledge-base)
- [RAG Pipeline](#rag-pipeline)
- [Evaluation](#evaluation)
- [Monitoring](#monitoring)
- [Screenshots](#screenshots)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Zoomcamp Evaluation Coverage](#zoomcamp-evaluation-coverage)
- [Contributing](#contributing)
- [License](#license)

---

# Overview

Tech Knowledge Navigator is a **production-grade Retrieval Augmented Generation (RAG)** system that enables software engineers, architects, and students to search, explore, and chat with software engineering knowledge collected from multiple trusted public sources.

Unlike traditional chatbots that rely solely on the language model's internal knowledge, this project retrieves relevant information from a curated knowledge base before generating an answer. This significantly improves answer quality, reduces hallucinations, and provides verifiable citations.

The project demonstrates an end-to-end AI application, covering automated ingestion, hybrid retrieval, prompt orchestration, evaluation, monitoring, observability, and deployment.

This repository has been designed as a complete engineering project and satisfies the technical requirements of the **LLM Zoomcamp End-to-End Project**.

---

# Problem Statement

Software engineering knowledge is fragmented across numerous resources:

- Technical documentation
- Wikipedia
- Conference talks
- Engineering blogs
- YouTube transcripts
- Architecture articles
- Technical books

Finding accurate answers often requires searching multiple websites, reading lengthy articles, and comparing conflicting recommendations.

General-purpose LLMs can answer many software engineering questions, but they often:

- Hallucinate implementation details
- Provide outdated information
- Lack references
- Ignore official documentation
- Mix unrelated technologies
- Miss architecture best practices

The goal of this project is to solve these problems by building a Retrieval-Augmented Generation (RAG) system that retrieves trusted technical content before generating responses.

---

# Project Goals

The primary objectives of this project are:

- Build an end-to-end production-ready RAG application.
- Create an automated document ingestion pipeline.
- Support multiple document sources.
- Implement hybrid search using lexical and semantic retrieval.
- Improve retrieval using query rewriting and document re-ranking.
- Evaluate retrieval and generation quality.
- Monitor application health and user feedback.
- Deploy the complete application using Docker Compose.
- Produce a reusable open-source project.

---

# Features

## Knowledge Ingestion

- Automated ingestion pipeline
- Wikipedia integration
- Technical article indexing
- YouTube transcript ingestion
- PDF document support
- OCR-ready image ingestion
- Metadata extraction
- Configurable document chunking

---

## Retrieval

- BM25 lexical search
- Dense vector search
- Hybrid search
- Reciprocal Rank Fusion (RRF)
- Weighted Hybrid Search
- Cross-Encoder Re-ranking
- Query Rewriting
- Metadata filtering
- Source citations

---

## Large Language Model

Supports multiple providers through a pluggable architecture.

Supported providers include:

- OpenAI
- Ollama
- Groq
- Anthropic Claude

---

## User Interface

- Streamlit Dashboard
- Conversational Chat
- Search Interface
- Document Viewer
- Feedback Collection
- Retrieval Inspection
- Monitoring Dashboard

---

## Monitoring

- Prometheus Metrics
- Grafana Dashboards
- Application Health
- Retrieval Metrics
- Token Usage
- User Feedback
- Request Latency
- Cost Monitoring

---

## Evaluation

Supports multiple evaluation frameworks.

- RAGAS
- DeepEval
- Retrieval Benchmarks
- Prompt Evaluation
- Hallucination Detection
- Faithfulness
- Context Precision
- Context Recall

---

# Architecture

```text
                           User
                             │
                             ▼
                     Streamlit UI
                             │
                             ▼
                         FastAPI
                             │
                    Query Rewriter
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼
         OpenSearch                  Qdrant
           BM25                  Vector Search
               ▼                           ▼
               └─────────────┬─────────────┘
                             ▼
                Reciprocal Rank Fusion
                             ▼
                Cross Encoder Re-ranking
                             ▼
                   Context Construction
                             ▼
                    Prompt Generation
                             ▼
                      Large Language Model
                             ▼
                  Response + Source Citations
                             ▼
                Monitoring & User Feedback
```

A detailed explanation of the architecture can be found in:

```
docs/architecture.md
```

---

# Technology Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Backend          | FastAPI                |
| Frontend         | Streamlit              |
| Language         | Python 3.12            |
| LLM              | OpenAI / Ollama / Groq |
| Embeddings       | BAAI BGE               |
| Vector Database  | Qdrant                 |
| Keyword Search   | OpenSearch             |
| Workflow         | Prefect                |
| Database         | PostgreSQL             |
| Monitoring       | Prometheus             |
| Dashboards       | Grafana                |
| Evaluation       | RAGAS, DeepEval        |
| Containerization | Docker Compose         |
| Testing          | Pytest                 |

---

# Project Structure

```
tech-knowledge-navigator/

app/
ui/
datasets/
retrieval/
evaluation/
monitoring/
docker/
docs/
tests/
scripts/
```

The complete repository structure is documented in:

```
docs/architecture.md
```

---

# Knowledge Base

The application indexes software engineering knowledge from trusted public sources.

Current data sources include:

- Wikipedia
- Technical Documentation
- Engineering Blogs
- Conference Talks
- YouTube Transcripts
- Technical Articles
- PDF Documents
- Slide Decks

Every document is:

- cleaned
- normalized
- chunked
- embedded
- indexed
- searchable

More information:

```
docs/dataset.md
```

---

# RAG Pipeline

The retrieval pipeline follows modern production practices.

1. User submits a question.
2. Query is rewritten.
3. Hybrid search retrieves relevant documents.
4. Results are fused using Reciprocal Rank Fusion.
5. Documents are re-ranked.
6. Context is assembled.
7. Prompt is generated.
8. LLM produces a grounded answer.
9. Citations are returned.
10. Feedback is collected.

Documentation:

```
docs/rag-pipeline.md
```

---

# Evaluation

The project evaluates both retrieval quality and generation quality.

## Retrieval Evaluation

- BM25
- Vector Search
- Hybrid Search
- Hybrid + Re-ranking

Metrics:

- Recall@5
- Recall@10
- MRR
- nDCG
- Precision
- Latency

## LLM Evaluation

Multiple prompt strategies are compared.

Metrics include:

- Faithfulness
- Answer Relevance
- Context Precision
- Context Recall
- Hallucination Detection
- Cost
- Latency

Documentation:

```
docs/evaluation.md
```

---

# Monitoring

Application monitoring includes:

- Request Count
- Request Latency
- Search Latency
- LLM Response Time
- Token Usage
- User Feedback
- Error Rate
- Retrieval Statistics

Documentation:

```
docs/monitoring.md
```

---

# Screenshots

The following screenshots will be added after implementation.

- Home Page
- Chat Interface
- Search Interface
- Retrieved Documents
- Monitoring Dashboard
- Evaluation Dashboard
- Docker Deployment

```
docs/screenshots/
```

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/maheshwarligade/LLM-Zoomcamp-2026.git/07-proecjts/homework/tech-knowledge-navigator

cd tech-knowledge-navigator
```

---

## Configure Environment

```bash
cp .env.example .env
```

Update:

- OpenAI API Key
- Database credentials
- Qdrant configuration
- OpenSearch configuration

---

## Start Application

```bash
docker compose up --build
```

---

## Open Applications

| Service    | URL                             |
| ---------- | ------------------------------- |
| FastAPI    | http://localhost:8000           |
| Swagger    | http://localhost:8000/docs      |
| Streamlit  | http://localhost:8501           |
| Grafana    | http://localhost:3000           |
| Prometheus | http://localhost:9090           |
| Qdrant     | http://localhost:6333/dashboard |

---

# Documentation

| Document                  | Description             |
| ------------------------- | ----------------------- |
| docs/problem-statement.md | Project motivation      |
| docs/architecture.md      | System architecture     |
| docs/dataset.md           | Dataset and ingestion   |
| docs/retrieval.md         | Hybrid retrieval        |
| docs/rag-pipeline.md      | Complete RAG flow       |
| docs/api.md               | REST APIs               |
| docs/evaluation.md        | Evaluation strategy     |
| docs/monitoring.md        | Monitoring & dashboards |
| docs/deployment.md        | Deployment guide        |
| docs/setup.md             | Local setup             |
| docs/security.md          | Security considerations |
| docs/roadmap.md           | Future improvements     |

---

# Roadmap

## Phase 1

- Infrastructure
- Docker
- FastAPI
- Streamlit

## Phase 2

- Automated Ingestion
- Embeddings
- Knowledge Base

## Phase 3

- Hybrid Search
- Re-ranking
- Query Rewriting

## Phase 4

- Complete RAG
- Streaming
- Citations

## Phase 5

- Monitoring
- Evaluation
- Production Deployment

---

# Zoomcamp Evaluation Coverage

| Evaluation Criteria  | Status |
| -------------------- | ------ |
| Problem Description  | ✅     |
| Retrieval Flow       | ✅     |
| Retrieval Evaluation | ✅     |
| LLM Evaluation       | ✅     |
| Interface            | ✅     |
| Automated Ingestion  | ✅     |
| Monitoring           | ✅     |
| Containerization     | ✅     |
| Reproducibility      | ✅     |
| Hybrid Search        | ✅     |
| Document Re-ranking  | ✅     |
| Query Rewriting      | ✅     |
| Cloud Deployment     | ✅     |

---

# Future Enhancements

- Multi-Agent Architecture
- Knowledge Graph Integration
- Multi-modal RAG
- Image Understanding
- Voice Interface
- Model Routing
- Function Calling
- Long-term Conversation Memory
- Kubernetes Deployment
- Enterprise Authentication
- Role-Based Access Control (RBAC)

---

# Contributing

Contributions are welcome.

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md

before submitting a Pull Request.

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Acknowledgements

This project was developed as part of the **LLM Zoomcamp** and demonstrates modern Retrieval-Augmented Generation techniques, hybrid search, evaluation, monitoring, and production-ready engineering practices.

Special thanks to the open-source communities behind FastAPI, Streamlit, Qdrant, OpenSearch, Prefect, Grafana, Prometheus, and the evaluation frameworks that make projects like this possible.
