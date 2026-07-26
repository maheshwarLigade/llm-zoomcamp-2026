"""
Search Prompt Templates

Prompt engineering layer for retrieval optimization.

Responsibilities:
- Query expansion
- Search intent detection
- Keyword extraction
- Multi-query generation
- Hybrid search optimization
- Query decomposition

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass

from enum import Enum



###############################################################################
# Search Intent
###############################################################################


class SearchIntent(str, Enum):
    """
    Search intent classification.
    """

    INFORMATIONAL = "informational"

    NAVIGATIONAL = "navigational"

    TRANSACTIONAL = "transactional"

    COMPARISON = "comparison"

    TROUBLESHOOTING = "troubleshooting"



###############################################################################
# Search Input
###############################################################################


@dataclass
class SearchPromptInput:
    """
    Search prompt input model.
    """

    query: str

    conversation_history: list[dict[str, str]] | None = None

    domain_context: str | None = None



###############################################################################
# Query Understanding Prompt
###############################################################################


QUERY_ANALYSIS_PROMPT = """
You are an expert search query analyzer.

Analyze the user query for retrieval optimization.

User Query:

{query}


Return JSON:

{
    "intent":
        "informational|navigational|transactional|comparison|troubleshooting",

    "main_topic":"",

    "entities":[],

    "important_terms":[],

    "filters":[],

    "ambiguities":[]
}
"""



def build_query_analysis_prompt(
    data: SearchPromptInput,
) -> str:
    """
    Build query analysis prompt.
    """

    return QUERY_ANALYSIS_PROMPT.format(
        query=data.query
    )



###############################################################################
# Query Expansion
###############################################################################


QUERY_EXPANSION_PROMPT = """
You are a search optimization expert.

Generate multiple search queries from the original query.

Goal:

Improve document retrieval by creating
different semantic variations.

Original Query:

{query}


Generate:

1. Semantic variations
2. Keyword focused queries
3. Technical terminology variations


Return JSON:

{
    "original_query":"",
    "expanded_queries":[]
}
"""



def build_query_expansion_prompt(
    query: str,
) -> str:
    """
    Create query expansion prompt.
    """

    return QUERY_EXPANSION_PROMPT.format(
        query=query
    )



###############################################################################
# Multi Query Retrieval
###############################################################################


MULTI_QUERY_PROMPT = """
You are improving a RAG retrieval system.

Generate multiple independent queries
that can retrieve relevant information.

Question:

{query}


Rules:

- Preserve original meaning.
- Use different wording.
- Cover different perspectives.
- Avoid duplicate queries.


Return:

[
    "query 1",
    "query 2",
    "query 3"
]
"""



def build_multi_query_prompt(
    query: str,
) -> str:
    """
    Generate multi retrieval queries.
    """

    return MULTI_QUERY_PROMPT.format(
        query=query
    )



###############################################################################
# Keyword Extraction
###############################################################################


KEYWORD_EXTRACTION_PROMPT = """
Extract important search keywords.

Query:

{query}


Identify:

- Technical terms
- Product names
- Technologies
- Entities
- Domain specific words


Return JSON:

{
    "keywords":[],
    "entities":[],
    "technical_terms":[]
}
"""



def build_keyword_prompt(
    query: str,
) -> str:
    """
    Build keyword extraction prompt.
    """

    return KEYWORD_EXTRACTION_PROMPT.format(
        query=query
    )



###############################################################################
# Hybrid Search Query Builder
###############################################################################


HYBRID_SEARCH_PROMPT = """
You are optimizing a hybrid search engine.

Hybrid search combines:

1. Semantic vector search
2. Keyword based search


User Query:

{query}


Generate:

Semantic Query:

- Meaning focused query for embeddings


Keyword Query:

- Exact terms for BM25 search


Return JSON:

{
    "semantic_query":"",
    "keyword_query":"",
    "boost_terms":[]
}
"""



def build_hybrid_search_prompt(
    query: str,
) -> str:
    """
    Build hybrid retrieval prompt.
    """

    return HYBRID_SEARCH_PROMPT.format(
        query=query
    )



###############################################################################
# Query Decomposition
###############################################################################


QUERY_DECOMPOSITION_PROMPT = """
Break complex questions into smaller searchable questions.

Question:

{query}


Rules:

- Identify independent information needs.
- Create simple retrieval queries.
- Maintain relationship between queries.


Return JSON:

{
    "complex_question": "",
    "sub_queries":[]
}
"""



def build_query_decomposition_prompt(
    query: str,
) -> str:
    """
    Build decomposition prompt.
    """

    return QUERY_DECOMPOSITION_PROMPT.format(
        query=query
    )



###############################################################################
# Search Result Refinement
###############################################################################


SEARCH_REFINEMENT_PROMPT = """
You are improving retrieval results.

Question:

{query}


Retrieved Documents:

{documents}


Determine:

- Missing information
- Irrelevant documents
- Better search direction


Return:

{
    "missing_topics":[],
    "irrelevant_documents":[],
    "recommended_query":""
}
"""



def build_search_refinement_prompt(
    query: str,
    documents: list[str],
) -> str:
    """
    Build retrieval refinement prompt.
    """

    return SEARCH_REFINEMENT_PROMPT.format(

        query=query,

        documents="\n\n".join(
            documents
        ),

    )



###############################################################################
# Contextual Search
###############################################################################


CONTEXTUAL_SEARCH_PROMPT = """
Rewrite the user question into a standalone search query.

Conversation:

{history}


Current Question:

{query}


Rules:

- Resolve pronouns.
- Include missing context.
- Preserve intent.


Return:

Standalone Search Query:
"""



def build_contextual_search_prompt(
    query: str,
    history: list[dict[str, str]],
) -> str:
    """
    Build contextual search query.
    """

    conversation = "\n".join(

        [
            f"{x['role']}: {x['content']}"
            for x in history
        ]

    )


    return CONTEXTUAL_SEARCH_PROMPT.format(

        history=conversation,

        query=query,

    )



###############################################################################
# Metadata
###############################################################################


def get_search_prompt_metadata():
    """
    Search prompt metadata.
    """

    return {

        "name": "search_prompt",

        "version": "1.0",

        "type": "retrieval_optimization",

    }