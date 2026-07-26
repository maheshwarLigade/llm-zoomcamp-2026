````markdown
# API Documentation

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**API Style:** RESTful API  
**Protocol:** HTTP/HTTPS  
**Content-Type:** `application/json`

---

# Table of Contents

- Overview
- API Design Principles
- Base URL
- Authentication
- API Versioning
- Error Handling
- Response Format
- Pagination
- Health APIs
- Chat APIs
- Search APIs
- Documents APIs
- Ingestion APIs
- Evaluation APIs
- Monitoring APIs
- Feedback APIs
- Admin APIs
- OpenAPI Specification
- Rate Limiting
- HTTP Status Codes

---

# Overview

The Tech Knowledge Navigator API exposes a collection of REST endpoints that enable interaction with the Retrieval-Augmented Generation (RAG) platform.

The API supports:

- Conversational AI
- Semantic Search
- Hybrid Retrieval
- Document Management
- Knowledge Base Ingestion
- Monitoring
- Evaluation
- User Feedback

The backend is implemented using **FastAPI**, providing automatic OpenAPI documentation and interactive Swagger UI.

---

# API Design Principles

The API follows REST best practices.

## Stateless

Each request contains all information required for processing.

---

## Versioned

Every endpoint is versioned.

```
/api/v1/
```

Future versions:

```
/api/v2/
/api/v3/
```

---

## JSON Only

Every request and response uses JSON.

Request

```http
Content-Type: application/json
```

Response

```http
Content-Type: application/json
```

---

## Consistent Response Structure

Every endpoint returns a consistent schema.

Success

```json
{
  "success": true,
  "timestamp": "2026-07-26T10:30:00Z",
  "data": {}
}
```

Failure

```json
{
  "success": false,
  "timestamp": "2026-07-26T10:30:00Z",
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Requested document does not exist."
  }
}
```

---

# Base URL

Local

```
http://localhost:8000/api/v1
```

Production

```
https://api.techknowledge.ai/api/v1
```

---

# Authentication

## Current Version

Authentication is optional for local development.

Future versions will support:

- JWT Authentication
- OAuth2
- API Keys
- OpenID Connect

Example

```http
Authorization: Bearer <JWT_TOKEN>
```

---

# API Versioning

The API uses URI versioning.

Example

```
/api/v1/chat

/api/v1/search

/api/v1/documents
```

---

# Response Format

Every successful response returns

```json
{
  "success": true,
  "timestamp": "2026-07-26T12:00:00Z",
  "data": {}
}
```

Every failed response returns

```json
{
  "success": false,
  "timestamp": "2026-07-26T12:00:00Z",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Validation failed."
  }
}
```

---

# Pagination

Endpoints returning multiple records support pagination.

Query Parameters

| Parameter | Description      |
| --------- | ---------------- |
| page      | Page Number      |
| size      | Records Per Page |
| sort      | Sort Field       |
| direction | asc / desc       |

Example

```
GET /documents?page=1&size=20
```

Response

```json
{
  "page": 1,
  "size": 20,
  "totalRecords": 1842,
  "totalPages": 93,
  "items": []
}
```

---

# Health APIs

## Health Check

Returns application health.

### Endpoint

```
GET /health
```

### Response

```json
{
  "status": "UP",
  "application": "Tech Knowledge Navigator",
  "version": "1.0.0",
  "timestamp": "2026-07-26T12:30:00Z"
}
```

---

## Readiness Probe

Used by Kubernetes and Docker.

```
GET /health/ready
```

Response

```json
{
  "status": "READY"
}
```

---

## Liveness Probe

```
GET /health/live
```

Response

```json
{
  "status": "ALIVE"
}
```

---

## Version

```
GET /version
```

Response

```json
{
  "version": "1.0.0"
}
```

---

# Chat APIs

The Chat API powers conversational RAG.

---

## Ask Question

```
POST /chat
```

Request

```json
{
  "query": "Explain Kafka Consumer Groups.",
  "conversationId": "optional"
}
```

Response

```json
{
  "answer": "...",
  "sources": [
    {
      "title": "Kafka",
      "url": "https://...",
      "score": 0.96
    }
  ],
  "conversationId": "12345"
}
```

---

## Streaming Chat

```
POST /chat/stream
```

Returns

```
Server Sent Events (SSE)
```

Example

```
data: Hello

data: Kafka

data: Consumer Groups
```

---

## Conversation History

```
GET /chat/history/{conversationId}
```

Response

```json
{
  "conversationId": "12345",
  "messages": []
}
```

---

## Delete Conversation

```
DELETE /chat/history/{conversationId}
```

---

# Search APIs

The Search API provides document retrieval without LLM generation.

---

## Hybrid Search

```
POST /search
```

Request

```json
{
  "query": "Spring Boot Security"
}
```

Response

```json
{
  "query": "...",
  "rewrittenQuery": "...",
  "documents": []
}
```

---

## Vector Search

```
POST /search/vector
```

---

## BM25 Search

```
POST /search/bm25
```

---

## Hybrid Search Evaluation

```
POST /search/hybrid
```

Response

```json
{
  "strategy": "RRF",
  "documents": []
}
```

---

# Documents APIs

---

## List Documents

```
GET /documents
```

Supports pagination.

---

## Get Document

```
GET /documents/{documentId}
```

---

## Search Documents

```
GET /documents/search
```

---

## Delete Document

```
DELETE /documents/{documentId}
```

---

## Reindex Document

```
POST /documents/{documentId}/reindex
```

---

# Ingestion APIs

---

## Trigger Full Ingestion

```
POST /ingestion/run
```

Response

```json
{
  "jobId": "12345",
  "status": "STARTED"
}
```

---

## Trigger Incremental Ingestion

```
POST /ingestion/incremental
```

---

## Pipeline Status

```
GET /ingestion/status/{jobId}
```

---

## List Pipelines

```
GET /ingestion/jobs
```

---

## Cancel Pipeline

```
DELETE /ingestion/jobs/{jobId}
```

---

# Evaluation APIs

---

## Evaluate Retrieval

```
POST /evaluation/retrieval
```

Response

```json
{
  "Recall@5": 0.91,
  "MRR": 0.87,
  "nDCG": 0.92
}
```

---

## Evaluate LLM

```
POST /evaluation/llm
```

Response

```json
{
  "Faithfulness": 0.94,
  "AnswerRelevancy": 0.96,
  "ContextRecall": 0.91
}
```

---

## Generate Benchmark Report

```
POST /evaluation/report
```

---

# Monitoring APIs

---

## Metrics

```
GET /monitoring/metrics
```

---

## Token Usage

```
GET /monitoring/tokens
```

---

## Cost Summary

```
GET /monitoring/cost
```

---

## Retrieval Metrics

```
GET /monitoring/retrieval
```

---

## Dashboard Summary

```
GET /monitoring/dashboard
```

Example

```json
{
  "requests": 12450,
  "averageLatency": 182,
  "feedbackScore": 4.7
}
```

---

# Feedback APIs

---

## Submit Feedback

```
POST /feedback
```

Request

```json
{
  "conversationId": "12345",
  "rating": 5,
  "comment": "Very helpful explanation."
}
```

---

## List Feedback

```
GET /feedback
```

---

## Feedback Statistics

```
GET /feedback/statistics
```

---

# Admin APIs

---

## System Information

```
GET /admin/system
```

---

## Cache Statistics

```
GET /admin/cache
```

---

## Reload Configuration

```
POST /admin/reload
```

---

## Rebuild Vector Index

```
POST /admin/index/rebuild
```

---

## Clear Cache

```
DELETE /admin/cache
```

---

# OpenAPI Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

OpenAPI JSON

```
http://localhost:8000/openapi.json
```

---

# Rate Limiting

Future production deployment supports:

- 100 requests/minute per client
- Burst protection
- API key quotas

Example

```http
429 Too Many Requests
```

---

# HTTP Status Codes

| Code | Description           |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 202  | Accepted              |
| 204  | No Content            |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Resource Not Found    |
| 409  | Conflict              |
| 422  | Validation Error      |
| 429  | Too Many Requests     |
| 500  | Internal Server Error |
| 503  | Service Unavailable   |

---

# Error Codes

| Code                  | Description                 |
| --------------------- | --------------------------- |
| INVALID_REQUEST       | Invalid request payload     |
| VALIDATION_ERROR      | Input validation failed     |
| DOCUMENT_NOT_FOUND    | Document does not exist     |
| VECTOR_SEARCH_FAILED  | Vector database unavailable |
| OPENSEARCH_ERROR      | OpenSearch request failed   |
| LLM_PROVIDER_ERROR    | Failed to invoke LLM        |
| INGESTION_FAILED      | Pipeline execution failed   |
| RATE_LIMIT_EXCEEDED   | Too many requests           |
| INTERNAL_SERVER_ERROR | Unexpected server error     |

---

# API Workflow

```text
                Client
                   │
                   ▼
           FastAPI Controller
                   │
                   ▼
           Request Validation
                   │
                   ▼
            Service Layer
                   │
        ┌──────────┼───────────┐
        ▼          ▼           ▼
  Retrieval     Ingestion     Monitoring
        │
        ▼
 Hybrid Search Engine
        │
        ▼
 Prompt Builder
        │
        ▼
  LLM Provider
        │
        ▼
Response + Citations
```

---

# Future API Enhancements

The following capabilities are planned for future releases:

- WebSocket-based streaming chat
- Batch search endpoints
- Agent workflows
- Tool calling APIs
- Multi-user authentication
- Conversation export
- Knowledge graph query API
- Fine-grained RBAC
- Multi-tenant support
- OpenTelemetry trace endpoints

---

# Related Documentation

- `docs/architecture.md`
- `docs/dataset.md`
- `docs/ingestion.md`
- `docs/retrieval.md`
- `docs/rag-pipeline.md`
- `docs/evaluation.md`
- `docs/monitoring.md`
- `docs/deployment.md`
- `docs/setup.md`

---

**Last Updated:** July 2026  
**API Version:** v1.0.0
````
