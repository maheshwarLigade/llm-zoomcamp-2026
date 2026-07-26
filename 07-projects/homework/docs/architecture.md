````markdown
# System Architecture

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Architecture Style:** Clean Architecture + Domain Driven Design (DDD) + Retrieval Augmented Generation (RAG) + Event Driven Ingestion

---

# Table of Contents

- Introduction
- Architecture Goals
- High-Level Architecture
- System Components
- End-to-End Request Flow
- Clean Architecture
- Component Architecture
- Data Flow
- Deployment Architecture
- Technology Stack
- Knowledge Base Architecture
- Retrieval Architecture
- RAG Architecture
- Evaluation Architecture
- Monitoring Architecture
- Security Architecture
- Scalability Considerations
- Design Decisions
- Trade-offs
- Future Enhancements

---

# Introduction

Tech Knowledge Navigator is a **production-grade Retrieval-Augmented Generation (RAG)** platform that enables users to search, retrieve, and chat with software engineering knowledge gathered from trusted public sources.

The application combines:

- FastAPI
- Streamlit
- OpenSearch
- Qdrant
- PostgreSQL
- Prefect
- OpenAI/Ollama
- Prometheus
- Grafana

to build an end-to-end AI application following modern software engineering principles.

---

# Architecture Goals

The architecture was designed with the following objectives:

- Modular and maintainable
- Easily testable
- Cloud-native
- Scalable
- Observable
- Extensible
- Provider independent
- Production ready

The system separates concerns into independent modules that can evolve without affecting the rest of the application.

---

# High-Level Architecture

```text
                                   User
                                     │
                           Streamlit Web UI
                                     │
                                     ▼
                           FastAPI REST API
                                     │
          ┌──────────────────────────┼───────────────────────────┐
          ▼                          ▼                           ▼
  Query Rewriter             Search Controller          Chat Controller
          │                          │                           │
          └──────────────┬───────────┴──────────────┬────────────┘
                         ▼
                  Retrieval Service
                         │
          ┌──────────────┼──────────────────┐
          ▼              ▼                  ▼
     BM25 Search    Vector Search      Metadata Filter
   (OpenSearch)      (Qdrant)
          │              │
          └───────┬──────┘
                  ▼
        Hybrid Search (RRF)
                  ▼
          Cross Encoder Re-ranking
                  ▼
          Context Construction
                  ▼
            Prompt Builder
                  ▼
             LLM Provider
        (OpenAI / Ollama / Groq)
                  ▼
          Answer + Citations
                  ▼
          Monitoring & Feedback
```

---

# System Components

The platform consists of the following logical subsystems.

## User Interface

Responsible for:

- Chat Interface
- Search Interface
- Monitoring Dashboard
- Evaluation Dashboard
- Feedback Collection

Technology:

- Streamlit

---

## API Layer

Provides REST APIs.

Responsibilities

- Request validation
- Authentication
- Response serialization
- Error handling
- API versioning

Technology

- FastAPI

---

## Retrieval Layer

Responsible for retrieving relevant knowledge.

Includes:

- Query rewriting
- BM25 retrieval
- Vector retrieval
- Hybrid retrieval
- Re-ranking

---

## LLM Layer

Responsible for answer generation.

Includes

- Prompt templates
- Context builder
- LLM providers
- Streaming responses
- Citation generation

---

## Ingestion Layer

Responsible for building the knowledge base.

Includes

- Data collection
- Cleaning
- Chunking
- Embedding generation
- Metadata extraction
- Indexing

---

## Monitoring Layer

Responsible for

- Metrics
- Logging
- Tracing
- Dashboards
- User feedback

---

# End-to-End Request Flow

```text
User

│

▼

Submit Question

│

▼

FastAPI Controller

│

▼

Query Validation

│

▼

Query Rewriter

│

▼

Hybrid Retrieval

│

▼

OpenSearch + Qdrant

│

▼

Reciprocal Rank Fusion

│

▼

Cross Encoder Re-ranking

│

▼

Context Builder

│

▼

Prompt Generator

│

▼

LLM

│

▼

Answer Generation

│

▼

Citation Builder

│

▼

API Response

│

▼

User Feedback
```

---

# Clean Architecture

The application follows Clean Architecture.

```text
                     Presentation Layer

             FastAPI + Streamlit + REST APIs

──────────────────────────────────────────────────

                   Application Layer

       Chat Service

       Search Service

       Retrieval Service

       Evaluation Service

──────────────────────────────────────────────────

                     Domain Layer

Entities

Repositories

Domain Services

Interfaces

──────────────────────────────────────────────────

                 Infrastructure Layer

Qdrant

OpenSearch

PostgreSQL

OpenAI

Prefect

Prometheus

Grafana
```

Benefits:

- Low coupling
- High cohesion
- Easy testing
- Infrastructure independence

---

# Component Architecture

```text
app/

api/

core/

domain/

retrieval/

ingestion/

llm/

evaluation/

monitoring/

infrastructure/
```

Each module owns a single responsibility.

---

# Data Flow

## Ingestion Flow

```text
Wikipedia

Technical Articles

YouTube

PDF

Images

↓

Collectors

↓

Cleaning

↓

Chunking

↓

Metadata Extraction

↓

Embedding Generation

↓

Qdrant

↓

OpenSearch

↓

Knowledge Base
```

---

## Retrieval Flow

```text
User Query

↓

Rewrite Query

↓

Generate Embedding

↓

OpenSearch

+

Qdrant

↓

Hybrid Search

↓

Re-ranking

↓

Top Documents
```

---

## Generation Flow

```text
Documents

↓

Context Builder

↓

Prompt Builder

↓

LLM

↓

Grounded Answer

↓

Source Citations
```

---

# Deployment Architecture

```text
                    Docker Compose

        ┌─────────────────────────────────────┐

                Streamlit

        └─────────────────────────────────────┘

                     │

        ┌─────────────────────────────────────┐

                  FastAPI

        └─────────────────────────────────────┘

         │          │          │

         ▼          ▼          ▼

 PostgreSQL    OpenSearch    Qdrant

         │

         ▼

     Prefect Worker

         │

         ▼

 Prometheus

         │

         ▼

 Grafana
```

Each service runs independently and communicates through Docker networking.

---

# Technology Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | Streamlit              |
| Backend          | FastAPI                |
| LLM              | OpenAI / Ollama / Groq |
| Embeddings       | BAAI BGE               |
| Vector DB        | Qdrant                 |
| Search Engine    | OpenSearch             |
| Workflow         | Prefect                |
| Database         | PostgreSQL             |
| Monitoring       | Prometheus             |
| Dashboards       | Grafana                |
| Evaluation       | RAGAS + DeepEval       |
| Containerization | Docker Compose         |

---

# Knowledge Base Architecture

The knowledge base stores processed documents.

Sources include:

- Wikipedia
- Technical blogs
- Engineering documentation
- Conference talks
- YouTube transcripts
- PDF documents

Each document contains

- metadata
- chunks
- embeddings
- searchable text

---

# Retrieval Architecture

The retrieval engine consists of multiple independent retrieval strategies.

## BM25 Search

Lexical retrieval.

Advantages

- Fast
- Keyword based
- Exact matches

---

## Vector Search

Semantic retrieval.

Advantages

- Meaning based
- Handles synonyms
- Better recall

---

## Hybrid Search

Combines BM25 and Vector Search using

- Reciprocal Rank Fusion (RRF)
- Weighted Hybrid Search

This improves both precision and recall.

---

## Re-ranking

The initial search returns approximately 20–30 documents.

A Cross Encoder model scores each query-document pair and returns the highest-quality results.

Default model:

```
BAAI/bge-reranker-base
```

---

# RAG Architecture

```text
Question

↓

Rewrite

↓

Retrieve

↓

Re-rank

↓

Context

↓

Prompt

↓

LLM

↓

Answer

↓

Sources
```

The LLM never answers directly from its internal knowledge. Every response is grounded using retrieved context.

---

# Evaluation Architecture

The project evaluates both retrieval quality and LLM output.

## Retrieval

Metrics

- Recall@5
- Recall@10
- Precision
- MRR
- nDCG

---

## Generation

Metrics

- Faithfulness
- Answer Relevancy
- Context Recall
- Context Precision
- Hallucination Detection

Frameworks

- RAGAS
- DeepEval

---

# Monitoring Architecture

Monitoring is built around Prometheus and Grafana.

Metrics collected include:

- Request count
- Search latency
- LLM latency
- Retrieval latency
- Token usage
- API errors
- User feedback
- Cost estimation

Logs are structured in JSON format for easy aggregation and analysis.

---

# Security Architecture

Current implementation includes:

- Input validation
- CORS protection
- Environment-based secrets
- Request IDs
- Rate limiting hooks
- Secure configuration loading

Future enhancements:

- JWT authentication
- RBAC
- Multi-tenant support
- API key management
- OpenID Connect
- Audit logging

---

# Scalability Considerations

The architecture is designed for horizontal scaling.

Examples:

- Multiple FastAPI replicas
- Independent Streamlit deployment
- Dedicated OpenSearch cluster
- Qdrant cluster mode
- Managed PostgreSQL
- Distributed Prefect workers

Caching can be introduced using Redis to reduce repeated retrieval and embedding generation.

---

# Design Decisions

| Decision                 | Reason                                                            |
| ------------------------ | ----------------------------------------------------------------- |
| FastAPI                  | High-performance async framework with OpenAPI support             |
| Streamlit                | Rapid development of an interactive AI interface                  |
| Qdrant                   | Optimized vector database with filtering support                  |
| OpenSearch               | Mature BM25 search engine enabling hybrid retrieval               |
| Prefect                  | Flexible orchestration for ingestion workflows                    |
| Docker Compose           | Simplifies local development and reproducibility                  |
| Clean Architecture       | Improves maintainability and testability                          |
| Hybrid Retrieval         | Increases retrieval quality over lexical or semantic search alone |
| Cross-Encoder Re-ranking | Improves ranking precision before generation                      |

---

# Trade-offs

| Choice           | Benefit               | Trade-off                                             |
| ---------------- | --------------------- | ----------------------------------------------------- |
| Hybrid Search    | Higher relevance      | Additional retrieval latency                          |
| Re-ranking       | Better answer quality | Higher inference cost                                 |
| Local Embeddings | Lower operating cost  | Slower indexing compared to managed APIs              |
| Streamlit UI     | Rapid prototyping     | Less customizable than a dedicated frontend framework |
| Docker Compose   | Easy local setup      | Not intended for large-scale production orchestration |

---

# Future Enhancements

The architecture has been designed to accommodate future capabilities without major refactoring.

Planned enhancements include:

- Multi-agent workflows
- Knowledge graph integration
- Function calling
- Tool execution
- Multimodal RAG (text + image + PDF)
- Long-term conversation memory
- Redis caching
- Kubernetes deployment
- Helm charts
- Terraform infrastructure
- OpenTelemetry distributed tracing
- Multi-tenant SaaS architecture
- Fine-grained Role-Based Access Control (RBAC)

---

# Related Documentation

- `docs/problem-statement.md`
- `docs/dataset.md`
- `docs/ingestion.md`
- `docs/retrieval.md`
- `docs/rag-pipeline.md`
- `docs/api.md`
- `docs/evaluation.md`
- `docs/monitoring.md`
- `docs/deployment.md`
- `docs/setup.md`

---

## Architecture Summary

The Tech Knowledge Navigator architecture combines modern AI engineering practices with proven software architecture principles. By separating ingestion, retrieval, generation, evaluation, and monitoring into independent layers, the platform remains modular, extensible, and production-ready. Hybrid retrieval, document re-ranking, query rewriting, and comprehensive observability ensure that generated responses are accurate, traceable, and measurable, making the system suitable for both the LLM Zoomcamp project requirements and real-world deployment.
````
