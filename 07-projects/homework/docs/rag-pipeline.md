````markdown
# Retrieval-Augmented Generation (RAG) Pipeline

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Pipeline Version:** 1.0  
**Architecture:** Hybrid RAG (Query Rewriting + Hybrid Search + Re-ranking + LLM)

---

# Table of Contents

- Introduction
- What is RAG?
- Why RAG?
- RAG Architecture
- End-to-End Pipeline
- Pipeline Components
- Step 1 - User Query
- Step 2 - Query Rewriting
- Step 3 - Query Embedding
- Step 4 - Hybrid Retrieval
- Step 5 - Reciprocal Rank Fusion
- Step 6 - Metadata Filtering
- Step 7 - Cross-Encoder Re-ranking
- Step 8 - Context Builder
- Step 9 - Prompt Builder
- Step 10 - LLM Generation
- Step 11 - Citation Generation
- Step 12 - Response Delivery
- Pipeline Sequence Diagram
- Prompt Template
- Context Window Management
- Error Handling
- Performance Optimizations
- Pipeline Evaluation
- Technology Stack
- Future Enhancements

---

# Introduction

Large Language Models possess remarkable reasoning capabilities but suffer from an important limitation:

**They only know what they were trained on.**

Even state-of-the-art models may:

- Produce hallucinated answers
- Return outdated information
- Lack organization-specific knowledge
- Fail to provide trustworthy citations

Retrieval-Augmented Generation (RAG) solves this limitation by retrieving relevant knowledge from external sources before generating an answer.

Instead of asking the LLM to answer from memory alone, the model receives carefully selected documents as context.

---

# What is RAG?

Retrieval-Augmented Generation combines two independent systems:

1. Information Retrieval
2. Large Language Model

The retrieval engine searches a knowledge base for relevant information.

The retrieved documents are injected into the LLM prompt.

The LLM generates an answer grounded in those documents.

---

# Why RAG?

Without RAG:

```text
User Question

↓

LLM

↓

Answer (May Hallucinate)
```

Problems

- No citations
- Outdated knowledge
- Hallucinations
- Limited explainability

---

With RAG:

```text
User Question

↓

Knowledge Retrieval

↓

Relevant Documents

↓

LLM

↓

Grounded Answer
```

Benefits

- Current information
- Source citations
- Lower hallucination rate
- Better explainability
- Higher accuracy

---

# RAG Architecture

```text
                  User

                    │

                    ▼

             Streamlit UI

                    │

                    ▼

              FastAPI API

                    │

                    ▼

             Query Rewriting

                    │

                    ▼

           Embedding Generation

                    │

     ┌──────────────┴───────────────┐

     ▼                              ▼

OpenSearch (BM25)            Qdrant Vector Search

     ▼                              ▼

     └──────────────┬───────────────┘

                    ▼

        Reciprocal Rank Fusion (RRF)

                    ▼

         Metadata Filtering

                    ▼

      Cross Encoder Re-ranking

                    ▼

          Top Relevant Chunks

                    ▼

            Context Builder

                    ▼

            Prompt Builder

                    ▼

            Large Language Model

                    ▼

         Grounded Response

                    ▼

            User Feedback
```

---

# End-to-End Pipeline

```text
User Question

↓

Query Rewriting

↓

Embedding Generation

↓

BM25 Retrieval

↓

Vector Retrieval

↓

Hybrid Search

↓

Re-ranking

↓

Context Builder

↓

Prompt Generation

↓

LLM

↓

Answer

↓

Feedback

↓

Monitoring
```

---

# Pipeline Components

| Component         | Responsibility            |
| ----------------- | ------------------------- |
| Streamlit         | User Interface            |
| FastAPI           | Backend API               |
| Query Rewriter    | Improve search queries    |
| Embedding Service | Generate semantic vectors |
| OpenSearch        | Lexical search            |
| Qdrant            | Semantic retrieval        |
| Hybrid Search     | Combine results           |
| Re-ranker         | Improve ranking           |
| Prompt Builder    | Construct LLM prompt      |
| LLM               | Generate answer           |
| Monitoring        | Metrics collection        |

---

# Step 1 — User Query

The pipeline begins with a natural language question.

Example

```
Explain Kafka Consumer Groups.
```

The query is sent to the backend.

---

# Step 2 — Query Rewriting

The original query is optimized.

Original

```
consumer groups
```

Rewritten

```
Explain Apache Kafka Consumer Groups, message distribution, partition assignment, and rebalancing.
```

Benefits

- Better recall
- Better precision
- Better embeddings

---

# Step 3 — Query Embedding

The rewritten query is converted into a dense vector.

Embedding model

```
BAAI/bge-small-en-v1.5
```

Output

```
768-dimensional vector
```

The vector is used for semantic retrieval.

---

# Step 4 — Hybrid Retrieval

Two searches execute in parallel.

### BM25 Search

OpenSearch retrieves documents based on keywords.

Example

```
Consumer Groups
```

---

### Vector Search

Qdrant retrieves semantically similar documents.

Example

```
Partition assignment
```

Even if the exact keywords differ.

---

# Step 5 — Reciprocal Rank Fusion (RRF)

Results from both retrieval systems are merged.

Formula

```
Score = Σ 1 / (k + rank)
```

Benefits

- Stable ranking
- Better recall
- Better precision

---

# Step 6 — Metadata Filtering

Results are filtered using metadata.

Supported filters

- Technology
- Category
- Source
- Language
- Tags
- Published Date

Example

```json
{
  "technology": "Kafka",
  "category": "Messaging"
}
```

---

# Step 7 — Cross-Encoder Re-ranking

Top candidate documents are re-ranked.

Model

```
BAAI/bge-reranker-base
```

Input

```
Query

+

Retrieved Document
```

Output

```
Relevance Score
```

Top five documents are selected.

---

# Step 8 — Context Builder

Selected chunks are merged into a single context.

Example

```text
Document 1

-----------

Document 2

-----------

Document 3

-----------

Document 4
```

The builder removes duplicates and preserves source metadata.

---

# Context Window Management

Large contexts may exceed the LLM's token limit.

Strategies

- Maximum token budget
- Duplicate removal
- Chunk prioritization
- Metadata compression
- Citation preservation

Example

```
Maximum Context

6000 Tokens
```

---

# Step 9 — Prompt Builder

The prompt builder combines:

- System prompt
- User question
- Retrieved context
- Instructions
- Citation rules

---

## Prompt Template

```text
You are an expert software engineering assistant.

Answer only using the supplied context.

If the answer is unavailable, clearly state that the information is not present.

Always provide citations.

Context

{retrieved_documents}

Question

{user_query}
```

---

# Step 10 — LLM Generation

Supported providers

- OpenAI
- Ollama
- Groq
- AWS Bedrock

The LLM receives the prompt and generates a grounded response.

Example

```
Kafka Consumer Groups enable horizontal scalability...

Source:
Wikipedia
Apache Kafka Documentation
```

---

# Step 11 — Citation Generation

Each answer includes references to retrieved documents.

Example

```text
Sources

1. Apache Kafka Documentation

2. Wikipedia

3. Confluent Documentation
```

Benefits

- Transparency
- Explainability
- Verification

---

# Step 12 — Response Delivery

The response returned to the user contains:

- Final answer
- Sources
- Confidence indicators (optional)
- Response time
- Feedback controls

Example

```text
Answer

...

Sources

Apache Kafka Documentation

Wikipedia
```

---

# Pipeline Sequence Diagram

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

Query Rewriter

 │

 ▼

Embedding Service

 │

 ├────────► OpenSearch

 │

 ├────────► Qdrant

 │

 ▼

Hybrid Search

 │

 ▼

Re-ranker

 │

 ▼

Prompt Builder

 │

 ▼

LLM

 │

 ▼

FastAPI

 │

 ▼

Streamlit
```

---

# Error Handling

The pipeline handles failures gracefully.

| Failure                     | Recovery        |
| --------------------------- | --------------- |
| Embedding Model Unavailable | Retry           |
| Vector Search Failure       | BM25 fallback   |
| OpenSearch Failure          | Vector fallback |
| LLM Timeout                 | Retry           |
| Empty Retrieval             | Inform user     |
| Missing Metadata            | Skip filtering  |

---

# Performance Optimizations

The pipeline incorporates several optimizations.

### Embedding Cache

Avoid repeated embedding generation.

---

### Query Cache

Frequently searched questions are cached.

---

### Parallel Retrieval

BM25 and Vector Search execute simultaneously.

---

### Metadata Filtering

Reduce unnecessary re-ranking.

---

### Chunk Deduplication

Remove duplicate contexts.

---

### Connection Pooling

Reuse database connections.

---

### Async Processing

FastAPI executes retrieval asynchronously.

---

# Pipeline Evaluation

The RAG pipeline is evaluated end-to-end.

| Metric             | Target     |
| ------------------ | ---------- |
| Recall@5           | ≥ 0.90     |
| Precision@5        | ≥ 0.90     |
| Faithfulness       | ≥ 0.90     |
| Context Precision  | ≥ 0.90     |
| Hallucination Rate | < 5%       |
| Response Time      | < 1 second |

---

# Technology Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| UI               | Streamlit              |
| API              | FastAPI                |
| Retrieval        | OpenSearch             |
| Vector Database  | Qdrant                 |
| Embeddings       | BAAI/bge-small-en-v1.5 |
| Re-ranking       | BAAI/bge-reranker-base |
| Workflow         | Prefect                |
| Database         | PostgreSQL             |
| Monitoring       | Prometheus + Grafana   |
| Containerization | Docker Compose         |

---

# Zoomcamp Evaluation Mapping

| Requirement         | Implementation       |
| ------------------- | -------------------- |
| Knowledge Base      | OpenSearch + Qdrant  |
| Retrieval Flow      | Hybrid Search        |
| Query Rewriting     | Implemented          |
| Document Re-ranking | Cross Encoder        |
| LLM                 | OpenAI/Ollama/Groq   |
| Interface           | Streamlit + FastAPI  |
| Monitoring          | Prometheus + Grafana |
| Automated Ingestion | Prefect              |
| Evaluation          | RAGAS + DeepEval     |

---

# Future Enhancements

Future versions will include:

- Multi-modal RAG
- Knowledge Graph Retrieval
- Agentic Retrieval
- Long Context LLMs
- Adaptive Chunking
- Context Compression
- Multi-hop Retrieval
- Conversation Memory
- Personalized Retrieval
- Streaming Responses
- Local LLM Support
- Automatic Prompt Optimization

---

# Related Documentation

- `docs/architecture.md`
- `docs/hybrid-search.md`
- `docs/query-rewriting.md`
- `docs/dataset.md`
- `docs/evaluation.md`
- `docs/monitoring.md`
- `docs/deployment.md`

---

# Summary

The Retrieval-Augmented Generation (RAG) pipeline is the foundation of Tech Knowledge Navigator. By combining **query rewriting**, **hybrid retrieval (BM25 + vector search)**, **Reciprocal Rank Fusion**, **metadata filtering**, **cross-encoder re-ranking**, **context construction**, and **LLM-based answer generation**, the platform delivers accurate, explainable, and source-grounded responses. This architecture minimizes hallucinations, improves retrieval quality, and provides a production-ready implementation that satisfies all mandatory and advanced evaluation criteria of the LLM Zoomcamp project.
````
