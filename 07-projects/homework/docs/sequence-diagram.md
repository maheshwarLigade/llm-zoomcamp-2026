````markdown
# Sequence Diagrams

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Document Version:** 1.0  
**Architecture:** Retrieval-Augmented Generation (RAG)

---

# Table of Contents

- Introduction
- Overall System Sequence
- User Query Processing
- Document Ingestion
- Hybrid Retrieval
- Query Rewriting
- Re-ranking
- Prompt Generation
- LLM Response Generation
- User Feedback Flow
- Monitoring Flow
- Authentication Flow
- Deployment Interaction
- Error Handling
- Summary

---

# Introduction

This document illustrates the runtime interactions between the different components of the Tech Knowledge Navigator platform using UML sequence diagrams.

The diagrams provide a clear understanding of:

- User interactions
- Backend processing
- Retrieval pipeline
- LLM communication
- Monitoring
- Document ingestion
- Evaluation workflow

---

# Overall System Sequence

```text
+------+      +------------+      +----------+      +------------+
| User |      | Streamlit  |      | FastAPI  |      | Monitoring |
+------+      +------------+      +----------+      +------------+
    |                |                  |                  |
    | Open App       |                  |                  |
    |--------------->|                  |                  |
    |                | Health Check     |                  |
    |                |----------------->|                  |
    |                |<-----------------|                  |
    |                |                  |                  |
    | Ask Question   |                  |                  |
    |--------------->|                  |                  |
    |                | REST API         |                  |
    |                |----------------->|                  |
    |                |                  | Log Metrics      |
    |                |                  |----------------->|
    |                |                  |<-----------------|
    |                |<-----------------|                  |
    |<---------------|                  |                  |
```

---

# User Query Processing

```text
User
 │
 │ Ask Question
 ▼
Streamlit
 │
 │ POST /chat
 ▼
FastAPI
 │
 │ Validate Request
 ▼
Query Rewriter
 │
 │ Improved Query
 ▼
Retriever
 │
 │ Relevant Documents
 ▼
Prompt Builder
 │
 │ Prompt
 ▼
LLM
 │
 │ Answer
 ▼
FastAPI
 │
 ▼
Streamlit
 │
 ▼
User
```

---

# Document Ingestion Pipeline

```text
Administrator
      │
      ▼
Prefect Workflow
      │
      ▼
Dataset Loader
      │
      ▼
Document Parser
      │
      ▼
Chunk Generator
      │
      ▼
Embedding Generator
      │
      ├─────────────► OpenSearch
      │
      └─────────────► Qdrant
      │
      ▼
Metadata Store
      │
      ▼
Ingestion Complete
```

---

# Hybrid Retrieval Sequence

```text
User Query
      │
      ▼
Query Rewriter
      │
      ▼
Embedding Generator
      │
      ├────────────► OpenSearch (BM25)
      │
      └────────────► Qdrant (Vector Search)
                       │
                       ▼
              Ranked Results
                       │
                       ▼
          Reciprocal Rank Fusion
                       │
                       ▼
              Metadata Filtering
                       │
                       ▼
               Cross Encoder
                       │
                       ▼
            Top Ranked Documents
```

---

# Query Rewriting Sequence

```text
User Query
     │
     ▼
Query Rewriter
     │
     ├── Normalize Query
     │
     ├── Expand Technical Terms
     │
     ├── Correct Grammar
     │
     ├── Resolve Acronyms
     │
     └── Rewrite Search Query
            │
            ▼
 Improved Query
```

Example

```
Original

Kafka rebalance

↓

Rewritten

Explain Apache Kafka Consumer Group Rebalancing Process
```

---

# Re-ranking Sequence

```text
Hybrid Search
      │
      ▼
Top 20 Documents
      │
      ▼
Cross Encoder
      │
      ├── Query + Document 1
      ├── Query + Document 2
      ├── Query + Document 3
      ├── ...
      └── Query + Document 20
              │
              ▼
      Relevance Scores
              │
              ▼
       Sorted Documents
              │
              ▼
      Top 5 Documents
```

---

# Prompt Generation Sequence

```text
User Query
      │
      ▼
Context Builder
      │
      ▼
Retrieved Documents
      │
      ▼
Prompt Builder
      │
      ├── System Prompt
      ├── User Question
      ├── Retrieved Context
      ├── Instructions
      └── Citation Rules
              │
              ▼
         Final Prompt
```

---

# LLM Response Generation

```text
Prompt Builder
      │
      ▼
LLM Provider
      │
      ├── OpenAI
      ├── Ollama
      ├── Groq
      └── AWS Bedrock
              │
              ▼
Generated Response
              │
              ▼
Citation Generator
              │
              ▼
Final Response
```

---

# User Feedback Flow

```text
User
 │
 │ Rate Answer
 ▼
Streamlit
 │
 │ POST /feedback
 ▼
FastAPI
 │
 ▼
PostgreSQL
 │
 ▼
Grafana Dashboard
```

Feedback contains:

- Rating
- Comment
- Query
- Response ID
- Timestamp

---

# Monitoring Flow

```text
Application
      │
      ├── API Metrics
      ├── Retrieval Metrics
      ├── LLM Metrics
      ├── Errors
      └── User Feedback
             │
             ▼
Prometheus
      │
      ▼
Grafana
      │
      ▼
Dashboard
```

---

# Authentication Flow

```text
User
 │
 ▼
Login
 │
 ▼
Authentication Provider
 │
 ▼
JWT Token
 │
 ▼
FastAPI
 │
 ▼
Protected API
```

For public demo deployments, authentication may be disabled.

---

# Deployment Interaction

```text
Docker Compose
       │
       ├────────► FastAPI
       │
       ├────────► Streamlit
       │
       ├────────► PostgreSQL
       │
       ├────────► OpenSearch
       │
       ├────────► Qdrant
       │
       ├────────► Prometheus
       │
       └────────► Grafana
```

---

# Error Handling Sequence

```text
User
 │
 ▼
FastAPI
 │
 ▼
Retriever
 │
 ├── Success
 │
 └── Failure
        │
        ▼
Fallback Retrieval
        │
        ▼
LLM
        │
        ▼
Graceful Response
```

Example

```
Vector Search Failed

↓

Fallback to BM25

↓

Return Response
```

---

# Complete End-to-End Sequence

```text
User
 │
 ▼
Streamlit
 │
 ▼
FastAPI
 │
 ▼
Authentication
 │
 ▼
Query Rewriter
 │
 ▼
Embedding Generator
 │
 ├────────► BM25 Search
 │
 ├────────► Vector Search
 │
 ▼
Hybrid Search
 │
 ▼
RRF
 │
 ▼
Metadata Filter
 │
 ▼
Cross Encoder
 │
 ▼
Prompt Builder
 │
 ▼
LLM
 │
 ▼
Citation Generator
 │
 ▼
FastAPI
 │
 ▼
Streamlit
 │
 ▼
User
 │
 ▼
Feedback
 │
 ▼
Monitoring
```

---

# Summary

The sequence diagrams presented in this document illustrate the major runtime interactions within **Tech Knowledge Navigator**. They cover the complete lifecycle of a user request—from authentication and query rewriting through hybrid retrieval, re-ranking, prompt generation, LLM inference, citation generation, feedback collection, and monitoring. These interactions demonstrate a production-ready Retrieval-Augmented Generation (RAG) workflow that is modular, scalable, and aligned with the architecture and evaluation requirements of the LLM Zoomcamp project.

---

# Related Documentation

- `architecture.md`
- `rag-pipeline.md`
- `retrieval.md`
- `reranking.md`
- `query-rewriting.md`
- `monitoring.md`
- `deployment.md`
- `evaluation.md`

```**

```
````
