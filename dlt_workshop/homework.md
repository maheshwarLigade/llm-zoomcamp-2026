````markdown
# Homework: dlt — Solution Guide

**Course:** LLM Zoomcamp 2026 — dlt Workshop

**Focus:** Instrumenting the Module 1 FAQ agent with Pydantic Logfire and ingesting trace data into DuckDB using dlt.

**Course Material:** https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026/workshops/dlt

---

## Environment Setup

For this assignment, the original Module 1 FAQ agent was reimplemented using **Pydantic AI** instead of the custom agent loop. While the underlying functionality remains unchanged—using the same system prompt, FAQ index, and search tool—Pydantic AI provides native integration with **Pydantic Logfire**, making observability significantly easier.

Enabling tracing requires only two lines of code:

```python
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()
```

Once instrumentation is enabled, every agent execution automatically generates a trace in Logfire. The trace captures each significant step of the execution, including:

- The overall agent invocation
- Individual LLM requests
- Tool invocations

This provides complete visibility into how the agent reaches its final response.

---

## Q1. Instrumenting the Agent with Logfire

### Question

For the prompt:

> **"How do I run Ollama locally?"**

How many spans are generated during a single agent execution?

### Answer

**5**

### Explanation

Each trace consists of multiple spans representing different stages of execution.

These spans include:

- The agent execution itself
- Every LLM interaction
- Every tool invocation

For this particular query, the model performed two searches before producing its final answer. Consequently, the execution consisted of:

- **3 LLM calls**
- **2 tool calls**

Although querying the complete trace returned six recorded span entries, the closest answer among the provided homework options is **5**.

### Example

```python
result = faq_agent.run_sync(
    "How do I run Ollama locally?",
    deps=deps
)
```

The resulting trace follows this execution flow:

```text
invoke_agent faq_agent
│
├── chat (gpt-5.4-mini)
├── execute_tool (search)
├── chat (gpt-5.4-mini)
├── execute_tool (search)
└── chat (gpt-5.4-mini)
```

The model initially searches for relevant documentation, evaluates the returned information, performs another search if necessary, and finally generates the response.

---

## Q2. Loading Logfire Traces into DuckDB with dlt

### Question

After importing the Logfire trace data into DuckDB using **dlt**, how many tables are created within the `agent_traces` schema?

### Answer

**24**

### Explanation

Each Logfire span is stored as a single record containing a deeply nested `attributes` JSON document.

During ingestion, **dlt** automatically normalizes nested structures by:

- Mapping JSON objects to table columns.
- Creating separate child tables for nested arrays.
- Preserving parent-child relationships using internal identifiers.

Although only **six span records** were imported, the nested structure generated:

- 1 primary table (`records`)
- 20 normalized child tables
- 3 internal dlt metadata tables

This resulted in a total of **24 tables**.

### Implementation

```python
import dlt
import requests

@dlt.resource(name="records", write_disposition="replace")
def logfire_records(read_token: str = dlt.secrets.value):

    response = requests.get(
        "https://logfire-us.pydantic.dev/v1/query",
        params={
            "sql": "SELECT * FROM records"
        },
        headers={
            "Authorization": f"Bearer {read_token}"
        },
    )

    response.raise_for_status()

    columns = response.json()["columns"]

    row_count = len(columns[0]["values"]) if columns else 0

    for i in range(row_count):
        yield {
            column["name"]: column["values"][i]
            for column in columns
        }


pipeline = dlt.pipeline(
    pipeline_name="logfire",
    destination="duckdb",
    dataset_name="agent_traces",
)

pipeline.run(logfire_records())
```

Verify the generated tables:

```sql
SELECT COUNT(*)
FROM information_schema.tables
WHERE table_schema = 'agent_traces';
```

Result:

```text
24
```

> **Note:** The Logfire Query API returns data in a **column-oriented format** rather than as a list of row objects. Before passing the data to dlt, the pipeline reconstructs individual records by transforming column arrays into row-oriented dictionaries.

---

## Q3. Querying Trace Data for Token Usage

### Question

For the same trace generated in **Question 1**, calculate the total value of:

`gen_ai.usage.input_tokens`

across all LLM spans.

Which answer range does the result belong to?

### Answer

**1500–5000**

**Exact Total:** **4,067 input tokens**

### Explanation

Each LLM span records its own token usage inside the `attributes` JSON document.

Tool execution spans do not include token statistics because no language model is invoked during those operations.

Summing the token counts across all three LLM calls gives the total input token consumption for the complete execution.

### SQL Query

```sql
SELECT
    SUM(
        (attributes->>'gen_ai.usage.input_tokens')::BIGINT
    ) AS total_input_tokens
FROM records
WHERE trace_id = '<trace_id>';
```

Result:

```text
4067
```

Token usage per LLM request:

| LLM Call       | Input Tokens |
| -------------- | -----------: |
| First Request  |        1,419 |
| Second Request |          204 |
| Third Request  |        2,444 |
| **Total**      |    **4,067** |

The distribution reflects the execution flow:

- The **first request** contains the complete system prompt and user query.
- The **second request** evaluates whether another search is required.
- The **third request** includes the accumulated search results before producing the final response.

---
````
