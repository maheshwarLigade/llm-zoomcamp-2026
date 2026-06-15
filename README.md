# LLM zoomcamp 2026

## Course on Building LLM Applications with RAG, Agents & Vector Search

![Course image](image.png)

🎓 Prerequisites
Python: You can write code confidently
Command Line: Comfortable with terminal
Docker: Basic familiarity
ML / LLMs: Not required
Hardware: Any laptop or PC. No GPU needed
Expenses: ~$1-5 in API credits

Note

If you can write a Python function and have heard of ChatGPT, you have enough to get started.

Module 1: Agentic RAG (Retrieval-Augmented Generation)
The Goal: Give the AI a "brain" (the LLM) and a "library" (your data) so it can answer questions based on your specific knowledge base

Keyword Search: This is traditional searching, like using Ctrl+F to find exact word matches in a document

Function Calling (Agentic Behavior): Instead of just talking, the AI is taught to "use tools." It can decide to call a specific piece of code (a function) to fetch real-time data or perform a task

Example: You ask, "What is the refund policy?" The AI "decides" to run a search_policy_database() function to find the exact text before answering you.

Concept Diagram:

```mermaid
graph LR
    A[User Query] --> B[AI "Agent"]
    B --> C[Decides to call tool]
    C --> D[Search Database]
    D --> E[AI combines data + query]
    E --> F[Final Answer]

Module 2: Vector Search
The Goal: Search for information based on meaning, not just matching words

Embeddings: This process turns text into a list of numbers (vectors). Words with similar meanings end up with similar numbers

Vector Databases: Specialized tools like PGVector, minsearch, and sqlitesearch are used to store these numbers and find matches quickly

Example: If you search for "puppy care," a vector search will find documents about "young dogs" even if the word "puppy" isn't used, because the meaning is similar.
Module 3: Orchestration
The Goal: Connect all the different parts of your AI system so they work together automatically

Kestra: A workflow tool used to schedule and manage your data pipelines
It ensures that if you add new documents to your library, they are automatically processed and added to your search engine.
Example: Think of this as the "manager" of a factory who ensures that the raw data (documents) gets sent to the right machine (embedding) and then to the warehouse (database).
Workshop: Data Ingestion
The Goal: Learn how to move data from the real world into your AI system

dlt (Data Load Tool): A tool used to pull "traces" (logs of what happened) from monitoring services so you can analyze how your AI is performing

Module 4: Evaluation
The Goal: Use data to prove that your AI is actually giving good answers

Retrieval Evaluation: Did the search find the right documents?
Answer Evaluation: Is the final answer correct, or is the AI making things up (hallucinating)?
Methods: You can use "Offline" (fixed tests) or "Online" (measuring real user interactions) evaluation

Example: You give the AI 100 questions where you already know the answer. If it gets 95 right, your system is 95% accurate.

Module 5: Monitoring
The Goal: Keep the system healthy and listen to your users after the app is live

Live Dashboards: Visual charts that show how many people are using the app and if there are any errors

User Feedback: Tracking "thumbs up" or "thumbs down" to see where the AI needs to improve

Module 6: Best Practices
The Goal: Move from a "hobby" project to a professional, high-quality application

LangChain: A popular framework that provides pre-built "lego blocks" for building LLM applications

Hybrid Search: Combining Keyword Search (for exact names/codes) and Vector Search (for general meaning) to get the best of both worlds

Reranking: After finding the top 10 documents, you use a second, smarter model to sort them again and make sure the absolute best one is at the top

Module 7 & Capstone: Building Your Own App
The Goal: Build a complete project from scratch to show off in your portfolio

The Components: You must build a searchable knowledge base, a retrieval pipeline, an evaluation process, a simple user interface (like Streamlit or FastAPI), and a monitoring loop

Example Ideas:
A Fitness Assistant that knows your workout history

A Codebase Bot that helps you find bugs in your own code

A Study Companion that answers questions about your specific textbooks
```
