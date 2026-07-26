````markdown
# Dataset Documentation

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Document Version:** 1.0

---

# Table of Contents

- Introduction
- Dataset Objectives
- Dataset Selection
- Data Sources
- Why These Datasets?
- Dataset Characteristics
- Dataset Collection Strategy
- Data Processing Pipeline
- Data Cleaning
- Metadata Extraction
- Document Chunking
- Embedding Generation
- Knowledge Base Schema
- Vector Database Schema
- OpenSearch Schema
- Dataset Versioning
- Dataset Quality
- Evaluation Dataset
- Data Refresh Strategy
- Limitations
- Ethical Considerations
- Future Improvements

---

# Introduction

The quality of a Retrieval-Augmented Generation (RAG) application is directly influenced by the quality of its knowledge base. Unlike traditional Large Language Models that depend only on pre-trained knowledge, Tech Knowledge Navigator retrieves relevant documents from a curated knowledge repository before generating responses.

The objective of the dataset is to build a comprehensive, reliable, and searchable software engineering knowledge base that serves as the foundation for hybrid retrieval and answer generation.

This project intentionally uses **publicly available datasets**, making the repository reproducible and compliant with the LLM Zoomcamp project requirements.

---

# Dataset Objectives

The dataset has been designed to achieve the following goals:

- Build a trusted software engineering knowledge repository
- Support semantic and lexical retrieval
- Enable source citations
- Reduce hallucinations
- Cover multiple software engineering domains
- Support automated ingestion
- Provide metadata for filtering
- Allow continuous updates

---

# Dataset Selection

The project uses multiple publicly available data sources instead of relying on a single dataset.

The knowledge base consists of:

- Wikipedia Articles
- Technical Documentation
- Engineering Blogs
- Conference Talk Transcripts
- YouTube Transcripts
- PDF Documentation
- Technical Books (Public Domain)
- Architecture Articles

This multi-source approach improves retrieval quality and broadens knowledge coverage.

---

# Data Sources

## 1. Wikipedia

Wikipedia provides high-level conceptual information for software engineering topics.

Examples:

- Microservices
- REST
- GraphQL
- Docker
- Kubernetes
- Kafka
- Redis
- CQRS
- Event Sourcing
- SOLID Principles
- Design Patterns

Advantages

- High-quality content
- Well-structured
- Frequently updated
- Rich cross-references

---

## 2. Official Documentation

Official documentation is the primary source for implementation guidance.

Examples

- Spring Framework
- Spring Boot
- Apache Kafka
- Redis
- Docker
- Kubernetes
- OpenSearch
- PostgreSQL
- FastAPI
- Streamlit
- Python

Advantages

- Authoritative
- Accurate
- Version specific
- Best practices

---

## 3. Engineering Blogs

Well-known engineering blogs provide practical implementation knowledge.

Examples

- Martin Fowler
- AWS Architecture Blog
- Microsoft Architecture Center
- Google Cloud Blog
- Netflix Technology Blog
- Uber Engineering
- Shopify Engineering

Advantages

- Real-world examples
- Architecture guidance
- Production lessons
- Case studies

---

## 4. Conference Talks

Conference talks often explain complex topics more clearly than documentation.

Examples

- Spring I/O
- Devoxx
- GOTO Conference
- Google Cloud Next
- KubeCon

Only publicly available transcripts are indexed.

---

## 5. YouTube Transcripts

Public transcripts are collected from educational channels.

Examples

- Spring Developers
- TechWorld with Nana
- Google Developers
- Microsoft Developer
- AWS Events

Advantages

- Practical explanations
- Architecture discussions
- Hands-on demonstrations

---

## 6. PDF Documents

The ingestion pipeline supports PDF documents including:

- Whitepapers
- API Guides
- Reference Manuals
- Architecture Documents
- Design Documents
- Technical Presentations

Text is extracted before indexing.

---

## 7. Images and Slide Decks

The system supports OCR extraction from:

- Technical diagrams
- Conference slides
- Architecture illustrations

OCR-generated text is cleaned before indexing.

---

# Why These Datasets?

The selected datasets satisfy the following requirements:

- Publicly accessible
- High technical quality
- Continuously maintained
- Rich metadata
- Suitable for hybrid search
- Easy to automate
- Appropriate for software engineering

---

# Dataset Characteristics

| Attribute        | Value                           |
| ---------------- | ------------------------------- |
| Domain           | Software Engineering            |
| Language         | English                         |
| Data Type        | Text                            |
| Format           | HTML, PDF, Markdown, Transcript |
| Update Frequency | Configurable                    |
| Searchable       | Yes                             |
| Embeddings       | Yes                             |
| Metadata         | Yes                             |

---

# Dataset Collection Strategy

The ingestion process is fully automated using Prefect.

```text
Wikipedia
        │
Technical Documentation
        │
Engineering Blogs
        │
Conference Transcripts
        │
PDF Documents
        │
───────────────
        │
Collectors
        │
Cleaning
        │
Chunking
        │
Embedding
        │
Indexing
        │
Knowledge Base
```

Every collector follows the same workflow, ensuring consistency across all data sources.

---

# Data Processing Pipeline

The processing pipeline consists of the following stages:

1. Data Collection
2. Content Normalization
3. HTML Cleaning
4. Markdown Cleaning
5. Boilerplate Removal
6. Metadata Extraction
7. Chunk Generation
8. Embedding Generation
9. OpenSearch Indexing
10. Vector Indexing

---

# Data Cleaning

Collected documents are normalized before indexing.

Cleaning operations include:

- Remove HTML tags
- Remove navigation menus
- Remove advertisements
- Remove duplicate paragraphs
- Remove empty sections
- Normalize whitespace
- Preserve code blocks
- Normalize Unicode
- Remove unsupported characters

The goal is to improve retrieval quality while preserving technical accuracy.

---

# Metadata Extraction

Each document is enriched with structured metadata.

| Field          | Description                |
| -------------- | -------------------------- |
| document_id    | Unique document identifier |
| title          | Document title             |
| source         | Dataset source             |
| source_url     | Original URL               |
| author         | Author if available        |
| category       | Technology category        |
| technology     | Main technology            |
| language       | Document language          |
| tags           | Search tags                |
| published_date | Publication date           |
| indexed_at     | Ingestion timestamp        |

Metadata enables filtering and source attribution during retrieval.

---

# Document Chunking

Large documents are divided into smaller chunks suitable for retrieval.

Supported strategies include:

- Fixed-size chunking
- Recursive chunking
- Semantic chunking

Default configuration:

| Parameter     | Value      |
| ------------- | ---------- |
| Chunk Size    | 500 tokens |
| Chunk Overlap | 100 tokens |

Each chunk retains metadata linking it back to the original document.

---

# Embedding Generation

Every chunk is transformed into a dense vector representation.

Default embedding model:

```
BAAI/bge-small-en-v1.5
```

The embedding service is provider-independent, allowing migration to alternative models in the future.

Each embedding is stored in Qdrant together with its metadata.

---

# Knowledge Base Schema

Each processed document follows a unified structure.

```json
{
  "document_id": "doc-001",
  "title": "Kafka Consumer Groups",
  "source": "Wikipedia",
  "source_url": "https://en.wikipedia.org/wiki/Apache_Kafka",
  "category": "Messaging",
  "technology": "Kafka",
  "tags": ["Kafka", "Consumer", "Messaging"],
  "language": "en",
  "text": "...",
  "indexed_at": "2026-07-26T10:00:00Z"
}
```

---

# Chunk Schema

```json
{
  "chunk_id": "chunk-001",
  "document_id": "doc-001",
  "chunk_number": 3,
  "total_chunks": 8,
  "text": "...",
  "embedding": [],
  "metadata": {}
}
```

---

# Vector Database Schema

Qdrant stores:

- Embedding Vector
- Chunk Text
- Metadata
- Chunk Identifier
- Document Identifier

Collection name:

```
tech_knowledge_chunks
```

---

# OpenSearch Schema

Each searchable document contains:

- title
- content
- source
- technology
- category
- tags
- language

OpenSearch provides lexical retrieval using the BM25 ranking algorithm.

---

# Dataset Versioning

Each ingestion run creates a new dataset version.

Version metadata includes:

- Dataset Version
- Ingestion Timestamp
- Number of Documents
- Number of Chunks
- Embedding Model
- Processing Duration

Example:

```text
Dataset Version: 2026.07.26
Documents: 4,582
Chunks: 42,318
Embedding Model: BAAI/bge-small-en-v1.5
```

Versioning supports reproducibility and rollback if needed.

---

# Dataset Quality

Quality checks performed during ingestion include:

- Duplicate detection
- Empty document removal
- Broken URL detection
- Metadata validation
- Language detection
- Chunk size validation
- Embedding validation

These checks improve retrieval accuracy and maintain data consistency.

---

# Evaluation Dataset

A separate benchmark dataset is created to evaluate retrieval performance.

Each benchmark record includes:

```json
{
  "query": "Explain Kafka Consumer Groups",
  "expected_documents": ["kafka-001", "kafka-005"]
}
```

This dataset is used to compute:

- Recall@5
- Recall@10
- Precision
- Mean Reciprocal Rank (MRR)
- nDCG

---

# Data Refresh Strategy

The knowledge base supports both full and incremental updates.

## Full Refresh

- Re-ingest all sources
- Recompute embeddings
- Rebuild indexes

## Incremental Refresh

- Detect new content
- Process only changed documents
- Update affected embeddings
- Reindex modified chunks

The refresh schedule can be configured using Prefect deployments.

---

# Limitations

Current limitations include:

- English-language documents only
- Public data sources only
- OCR quality depends on image resolution
- PDF extraction quality depends on document formatting
- Dynamic web pages may require custom collectors
- Embedding quality depends on the selected model

---

# Ethical Considerations

The project follows responsible AI and data usage practices.

- Uses publicly accessible information
- Preserves original source attribution
- Provides citations with generated answers
- Avoids storing copyrighted content beyond what is necessary for retrieval
- Supports source traceability and transparency

Users are encouraged to consult original documentation for authoritative guidance.

---

# Future Improvements

Future dataset enhancements include:

- Multi-language support
- Additional engineering domains
- GitHub repository indexing
- Stack Overflow integration
- RFC document ingestion
- Knowledge graph generation
- Automatic duplicate detection using embeddings
- Document freshness scoring
- Source quality ranking
- Incremental embedding updates
- Multimodal datasets (text, images, diagrams, audio)

---

# Related Documentation

- `docs/problem-statement.md`
- `docs/architecture.md`
- `docs/ingestion.md`
- `docs/retrieval.md`
- `docs/rag-pipeline.md`
- `docs/evaluation.md`
- `docs/api.md`

---

## Dataset Summary

The Tech Knowledge Navigator knowledge base combines authoritative documentation, educational resources, and engineering best practices into a unified retrieval corpus. Through automated ingestion, metadata enrichment, semantic chunking, and hybrid indexing, the dataset provides the foundation for accurate, explainable, and reproducible Retrieval-Augmented Generation while satisfying the dataset and reproducibility expectations of the LLM Zoomcamp project.
````
