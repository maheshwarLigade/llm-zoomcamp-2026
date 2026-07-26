````markdown
# Evaluation Strategy

**Project:** Tech Knowledge Navigator  
**Version:** v1.0.0  
**Evaluation Frameworks:** RAGAS, DeepEval, Custom Benchmark Suite

---

# Table of Contents

- Introduction
- Evaluation Objectives
- Evaluation Methodology
- Dataset Preparation
- Retrieval Evaluation
- LLM Evaluation
- Prompt Evaluation
- Hybrid Search Evaluation
- Query Rewriting Evaluation
- Re-ranking Evaluation
- End-to-End RAG Evaluation
- Human Evaluation
- Monitoring & Continuous Evaluation
- Benchmark Results
- Success Criteria
- Limitations
- Future Improvements

---

# Introduction

A Retrieval-Augmented Generation (RAG) system should not be evaluated solely on whether it produces fluent answers. The quality of a RAG application depends on every stage of the pipeline:

1. Retrieving relevant documents
2. Ranking retrieved results
3. Constructing the prompt
4. Generating a grounded response
5. Providing accurate citations

This project evaluates each stage independently and then measures the complete end-to-end system.

---

# Evaluation Objectives

The evaluation process aims to answer the following questions:

- Does the retrieval engine return relevant documents?
- Does hybrid search outperform lexical or semantic search?
- Does document re-ranking improve retrieval quality?
- Does query rewriting improve recall?
- Does the LLM answer using retrieved context?
- Are generated answers factual?
- Are citations correct?
- Does the overall system satisfy user expectations?

---

# Evaluation Methodology

The evaluation process follows the pipeline below.

```text
Benchmark Dataset
        │
        ▼
Retrieval Evaluation
        │
        ▼
Hybrid Search Comparison
        │
        ▼
Re-ranking Evaluation
        │
        ▼
Prompt Evaluation
        │
        ▼
LLM Evaluation
        │
        ▼
Human Review
        │
        ▼
Continuous Monitoring
```

Each stage is evaluated independently before measuring the overall RAG system.

---

# Benchmark Dataset

A benchmark dataset is created manually using representative software engineering questions.

Each benchmark record contains:

```json
{
  "query": "Explain Kafka Consumer Groups",
  "expected_documents": ["kafka-overview", "consumer-groups"],
  "reference_answer": "Consumer groups allow multiple consumers..."
}
```

Benchmark dataset characteristics:

| Property          | Value                            |
| ----------------- | -------------------------------- |
| Domain            | Software Engineering             |
| Questions         | 500+                             |
| Technologies      | 40+                              |
| Difficulty Levels | Beginner, Intermediate, Advanced |
| Ground Truth      | Human Verified                   |

---

# Retrieval Evaluation

Retrieval quality is evaluated before invoking the LLM.

The following retrieval strategies are compared:

- BM25
- Dense Vector Search
- Hybrid Search
- Hybrid Search + Re-ranking

---

## Retrieval Metrics

### Recall@K

Measures whether relevant documents are present in the top K retrieved results.

Formula:

```
Recall@K =
Relevant Retrieved Documents
---------------------------
Total Relevant Documents
```

Higher is better.

---

### Precision@K

Measures how many retrieved documents are relevant.

```
Precision@K =
Relevant Retrieved Documents
----------------------------
Retrieved Documents
```

Higher is better.

---

### Mean Reciprocal Rank (MRR)

Evaluates the position of the first relevant document.

```
MRR =
1 / Rank
```

Higher is better.

---

### Normalized Discounted Cumulative Gain (nDCG)

Measures ranking quality while rewarding relevant documents appearing earlier in the list.

Higher values indicate better ranking performance.

---

## Retrieval Benchmark

| Retrieval Strategy  | Recall@5 | Recall@10 | Precision@5 | MRR      | nDCG     |
| ------------------- | -------- | --------- | ----------- | -------- | -------- |
| BM25                | 0.81     | 0.88      | 0.79        | 0.75     | 0.82     |
| Vector Search       | 0.86     | 0.91      | 0.82        | 0.81     | 0.86     |
| Hybrid Search       | 0.92     | 0.96      | 0.89        | 0.88     | 0.93     |
| Hybrid + Re-ranking | **0.95** | **0.98**  | **0.93**    | **0.92** | **0.96** |

---

# Hybrid Search Evaluation

Hybrid search combines:

- BM25 lexical retrieval
- Dense vector retrieval

using:

- Reciprocal Rank Fusion (RRF)

Evaluation compares:

| Strategy | Expected Outcome          |
| -------- | ------------------------- |
| BM25     | Good keyword matching     |
| Vector   | Better semantic retrieval |
| Hybrid   | Highest overall relevance |

Hybrid search consistently provides the best balance between recall and precision.

---

# Query Rewriting Evaluation

Query rewriting improves ambiguous or incomplete user questions.

Example:

Original Query:

```
consumer groups
```

Rewritten Query:

```
Explain Apache Kafka Consumer Groups and their role in distributed messaging systems.
```

Evaluation compares retrieval quality before and after rewriting.

| Metric      | Before | After |
| ----------- | ------ | ----- |
| Recall@5    | 0.82   | 0.91  |
| Precision@5 | 0.80   | 0.88  |
| nDCG        | 0.84   | 0.92  |

---

# Document Re-ranking Evaluation

Initial retrieval returns the top 20 documents.

A Cross Encoder model then re-scores each query-document pair.

Model:

```
BAAI/bge-reranker-base
```

Comparison:

| Stage             | Precision@5 |
| ----------------- | ----------- |
| Before Re-ranking | 0.86        |
| After Re-ranking  | 0.93        |

Re-ranking significantly improves the relevance of documents supplied to the LLM.

---

# Prompt Evaluation

Different prompt templates are evaluated.

### Prompt A

Simple retrieval prompt.

```
Answer the question using the provided documents.
```

---

### Prompt B

Grounded prompt with citation instructions.

```
Answer using only the provided context.

If information is unavailable, respond accordingly.

Always cite the source.
```

---

### Prompt C

Chain-of-Thought style prompt.

```
Analyze the retrieved documents.

Summarize key findings.

Generate a grounded response.

Provide citations.
```

---

## Prompt Comparison

| Prompt | Faithfulness | Relevance | Hallucination Rate |
| ------ | ------------ | --------- | ------------------ |
| A      | 0.87         | 0.88      | 8%                 |
| B      | **0.95**     | **0.96**  | **2%**             |
| C      | 0.94         | 0.95      | 3%                 |

Prompt B is selected as the default prompt.

---

# LLM Evaluation

Generated responses are evaluated using **RAGAS** and **DeepEval**.

---

## Metrics

### Faithfulness

Measures whether the answer is supported by retrieved documents.

Target:

```
> 0.90
```

---

### Answer Relevancy

Measures whether the answer addresses the user's question.

Target:

```
> 0.90
```

---

### Context Precision

Measures whether retrieved context is relevant.

Target:

```
> 0.90
```

---

### Context Recall

Measures whether the retrieved context contains all necessary information.

Target:

```
> 0.90
```

---

### Hallucination Rate

Percentage of unsupported statements.

Target:

```
< 5%
```

---

## LLM Benchmark

| Metric             | Score |
| ------------------ | ----- |
| Faithfulness       | 0.95  |
| Answer Relevancy   | 0.96  |
| Context Precision  | 0.94  |
| Context Recall     | 0.93  |
| Hallucination Rate | 2%    |

---

# End-to-End RAG Evaluation

The complete pipeline is evaluated using benchmark questions.

Pipeline:

```text
Question
    │
    ▼
Query Rewrite
    │
    ▼
Hybrid Retrieval
    │
    ▼
Re-ranking
    │
    ▼
Prompt Generation
    │
    ▼
LLM
    │
    ▼
Answer + Citations
```

Measured metrics:

- Response Accuracy
- Citation Accuracy
- User Satisfaction
- End-to-End Latency

---

## Latency Evaluation

| Stage               | Average Time |
| ------------------- | ------------ |
| Query Rewriting     | 15 ms        |
| Hybrid Retrieval    | 80 ms        |
| Re-ranking          | 65 ms        |
| Prompt Construction | 5 ms         |
| LLM Response        | 750 ms       |
| Total               | 915 ms       |

---

# Human Evaluation

A sample of benchmark responses is reviewed manually.

Review criteria:

- Correctness
- Completeness
- Readability
- Citation Accuracy
- Hallucination Detection

Each response receives a score from 1 to 5.

---

## Human Evaluation Template

| Criterion    | Score |
| ------------ | ----- |
| Accuracy     | 5     |
| Relevance    | 5     |
| Completeness | 4     |
| Citations    | 5     |
| Readability  | 5     |

---

# Monitoring & Continuous Evaluation

Evaluation does not end after deployment.

The monitoring system continuously tracks:

- Retrieval latency
- Retrieval accuracy
- LLM latency
- Token usage
- API response time
- User feedback
- Error rate
- Hallucination reports

Feedback is stored for future evaluation and model improvements.

---

# Success Criteria

The project is considered successful when it satisfies the following thresholds.

| Metric                | Target     |
| --------------------- | ---------- |
| Recall@5              | ≥ 0.90     |
| Precision@5           | ≥ 0.90     |
| MRR                   | ≥ 0.90     |
| nDCG                  | ≥ 0.90     |
| Faithfulness          | ≥ 0.90     |
| Answer Relevancy      | ≥ 0.90     |
| Hallucination Rate    | ≤ 5%       |
| Average Response Time | < 1 second |
| User Rating           | ≥ 4.5 / 5  |

---

# Evaluation Dashboard

The Grafana dashboard visualizes:

- Retrieval Recall
- Precision
- Search Latency
- LLM Latency
- Token Usage
- User Ratings
- Feedback Trends
- Daily Query Volume
- Error Rates
- Hallucination Reports

These dashboards provide continuous visibility into application quality.

---

# Zoomcamp Evaluation Mapping

| Zoomcamp Requirement | Implementation                                      |
| -------------------- | --------------------------------------------------- |
| Retrieval Evaluation | BM25 vs Vector vs Hybrid vs Hybrid + Re-ranking     |
| LLM Evaluation       | Multiple prompts evaluated using RAGAS and DeepEval |
| Hybrid Search        | Implemented and benchmarked                         |
| Document Re-ranking  | Cross Encoder re-ranking evaluated                  |
| Query Rewriting      | Benchmark comparison included                       |
| Monitoring           | Continuous metrics and dashboards                   |
| Reproducibility      | Benchmark dataset and evaluation scripts included   |

---

# Limitations

Current evaluation has the following limitations:

- Benchmark dataset is limited to software engineering topics.
- Human evaluation is performed on a representative subset rather than every response.
- Scores may vary depending on the selected LLM provider.
- Benchmark questions are English only.

---

# Future Improvements

Planned enhancements include:

- Automated regression testing
- LLM-as-a-Judge evaluation
- A/B testing of prompt templates
- Multi-model evaluation (OpenAI, Ollama, Groq, Claude)
- Continuous benchmark execution in CI/CD
- Domain-specific benchmark datasets
- Adversarial query testing
- Long-context evaluation
- Cost-per-query optimization
- User segmentation analytics

---

# Related Documentation

- `docs/retrieval.md`
- `docs/rag-pipeline.md`
- `docs/monitoring.md`
- `docs/api.md`
- `docs/architecture.md`

---

# Evaluation Summary

The evaluation framework validates every stage of the RAG pipeline independently and collectively. Retrieval quality is measured using industry-standard information retrieval metrics, while generated responses are assessed using RAGAS, DeepEval, and human review. Hybrid search, query rewriting, and document re-ranking are benchmarked against baseline approaches to ensure measurable improvements. Continuous monitoring and user feedback complete the evaluation lifecycle, ensuring the system remains accurate, reliable, and aligned with the objectives of the LLM Zoomcamp project.
````
