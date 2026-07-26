"""
Evaluation Prompt Templates

LLM-as-a-Judge prompts for evaluating
RAG pipeline quality.

Supports:
- Answer correctness
- Faithfulness
- Context relevance
- Retrieval quality
- Hallucination detection
- Response grading

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass
from enum import Enum



###############################################################################
# Evaluation Categories
###############################################################################


class EvaluationMetric(str, Enum):
    """
    Evaluation dimensions.
    """

    FAITHFULNESS = "faithfulness"

    ANSWER_RELEVANCE = "answer_relevance"

    CONTEXT_RELEVANCE = "context_relevance"

    COMPLETENESS = "completeness"

    HALLUCINATION = "hallucination"

    RETRIEVAL_QUALITY = "retrieval_quality"



###############################################################################
# Evaluation Input
###############################################################################


@dataclass
class EvaluationInput:
    """
    Generic evaluation input.
    """

    question: str

    answer: str

    context: list[str]

    reference_answer: str | None = None



###############################################################################
# Common Evaluation Rules
###############################################################################


EVALUATION_SYSTEM_PROMPT = """
You are an expert evaluator for Retrieval Augmented Generation systems.

Your task is to objectively evaluate AI-generated answers.

Evaluation rules:

1. Use only the provided information.
2. Do not judge based on external knowledge.
3. Provide numerical scores.
4. Explain your reasoning.
5. Identify unsupported claims.
6. Return structured JSON output.

Always be objective.
"""



###############################################################################
# Faithfulness Evaluation
###############################################################################


FAITHFULNESS_PROMPT = """
Evaluate whether the answer is supported by the provided context.

Question:

{question}


Context:

{context}


Answer:

{answer}


Evaluate:

- Are all claims supported by context?
- Are there invented facts?
- Are there unsupported assumptions?


Return JSON:

{
    "score": 0-1,
    "faithful": true|false,
    "unsupported_claims": [],
    "reason": ""
}
"""



def build_faithfulness_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build faithfulness evaluation prompt.
    """

    return FAITHFULNESS_PROMPT.format(

        question=data.question,

        context="\n\n".join(
            data.context
        ),

        answer=data.answer,

    )



###############################################################################
# Answer Relevance Evaluation
###############################################################################


ANSWER_RELEVANCE_PROMPT = """
Evaluate whether the answer properly addresses
the user question.

Question:

{question}


Answer:

{answer}


Score:

0 = Completely irrelevant

1 = Perfectly answers the question


Return JSON:

{
    "score": 0-1,
    "relevant": true|false,
    "reason": ""
}
"""



def build_answer_relevance_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build answer relevance prompt.
    """

    return ANSWER_RELEVANCE_PROMPT.format(

        question=data.question,

        answer=data.answer,

    )



###############################################################################
# Context Relevance Evaluation
###############################################################################


CONTEXT_RELEVANCE_PROMPT = """
Evaluate whether retrieved documents
are useful for answering the question.

Question:

{question}


Retrieved Context:

{context}


Return JSON:

{
    "score":0-1,
    "useful_documents":[],
    "irrelevant_documents":[],
    "reason":""
}
"""



def build_context_relevance_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build retrieval evaluation prompt.
    """

    return CONTEXT_RELEVANCE_PROMPT.format(

        question=data.question,

        context="\n\n".join(
            data.context
        ),

    )



###############################################################################
# Hallucination Detection
###############################################################################


HALLUCINATION_PROMPT = """
Detect hallucinations in the generated answer.

Question:

{question}


Context:

{context}


Answer:

{answer}


Find:

1. Claims not supported by context.
2. Made-up information.
3. Incorrect references.


Return JSON:

{
    "hallucination_detected":true|false,

    "severity":
        "low|medium|high",

    "issues":[]

}
"""



def build_hallucination_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build hallucination detection prompt.
    """

    return HALLUCINATION_PROMPT.format(

        question=data.question,

        context="\n\n".join(
            data.context
        ),

        answer=data.answer,

    )



###############################################################################
# Completeness Evaluation
###############################################################################


COMPLETENESS_PROMPT = """
Evaluate whether the answer contains
all important information required.

Question:

{question}


Expected Answer:

{reference_answer}


Generated Answer:

{answer}


Return JSON:

{
    "score":0-1,

    "missing_information":[],

    "reason":""
}
"""



def build_completeness_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build completeness evaluation prompt.
    """

    return COMPLETENESS_PROMPT.format(

        question=data.question,

        reference_answer=(
            data.reference_answer
            or "Not provided"
        ),

        answer=data.answer,

    )



###############################################################################
# Retrieval Ranking Evaluation
###############################################################################


RETRIEVAL_EVALUATION_PROMPT = """
Evaluate retrieved documents.

Question:

{question}


Documents:

{documents}


Determine:

- Which documents are relevant?
- Ranking quality.
- Missing information.


Return JSON:

{
    "precision":0-1,

    "recall":0-1,

    "ranking_score":0-1,

    "recommended_order":[]

}
"""



def build_retrieval_evaluation_prompt(
    question: str,
    documents: list[str],
) -> str:
    """
    Build retrieval evaluation prompt.
    """

    return RETRIEVAL_EVALUATION_PROMPT.format(

        question=question,

        documents="\n\n".join(
            documents
        ),

    )



###############################################################################
# Full RAG Evaluation Prompt
###############################################################################


RAG_EVALUATION_PROMPT = """
Perform complete RAG evaluation.

Question:

{question}


Context:

{context}


Answer:

{answer}


Evaluate:

1. Faithfulness
2. Relevance
3. Completeness
4. Hallucination
5. Overall quality


Return JSON:

{
 "faithfulness":0-1,

 "relevance":0-1,

 "completeness":0-1,

 "hallucination":true|false,

 "overall_score":0-1,

 "comments":""
}
"""



def build_rag_evaluation_prompt(
    data: EvaluationInput,
) -> str:
    """
    Build complete RAG evaluation prompt.
    """

    return RAG_EVALUATION_PROMPT.format(

        question=data.question,

        context="\n\n".join(
            data.context
        ),

        answer=data.answer,

    )



###############################################################################
# Prompt Metadata
###############################################################################


def get_evaluation_prompt_metadata():
    """
    Prompt version information.
    """

    return {

        "name": "rag_evaluation_prompt",

        "version": "1.0",

        "type": "llm_as_judge",

    }