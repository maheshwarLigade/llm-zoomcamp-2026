"""
Chat Prompt Templates

Prompt engineering layer for RAG chat generation.

Responsibilities:
- System instructions
- Context grounding
- Conversation formatting
- Answer generation
- Citation handling

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass
from typing import Any



###############################################################################
# Prompt Constants
###############################################################################


CHAT_SYSTEM_PROMPT = """
You are a helpful AI assistant powered by Retrieval Augmented Generation (RAG).

Your responsibility is to answer user questions using only the provided
knowledge context.

Rules:

1. Always prioritize retrieved context over your own knowledge.

2. If the answer is not available in the context, clearly say:
   "I don't have enough information to answer this question."

3. Never invent facts, sources, numbers, or references.

4. Provide concise and accurate answers.

5. When possible, cite the source documents.

6. Explain complex concepts step-by-step.

7. Ask clarification questions when the user query is ambiguous.

8. Maintain conversation context for follow-up questions.
"""



###############################################################################
# Data Models
###############################################################################


@dataclass
class ChatPromptInput:
    """
    Input required to build chat prompt.
    """

    question: str

    context: list[str]

    conversation_history: list[dict[str, str]] | None = None

    user_profile: dict[str, Any] | None = None



###############################################################################
# Conversation Formatting
###############################################################################


def format_conversation_history(
    history: list[dict[str, str]] | None,
) -> str:
    """
    Convert conversation history into prompt format.

    Example:

    User:
    What is RAG?

    Assistant:
    RAG is ...

    """

    if not history:
        return "No previous conversation."


    messages = []


    for item in history:

        role = item.get(
            "role",
            "user",
        )

        content = item.get(
            "content",
            "",
        )


        messages.append(
            f"{role.capitalize()}: {content}"
        )


    return "\n".join(
        messages
    )



###############################################################################
# Context Formatting
###############################################################################


def format_context(
    contexts: list[str],
) -> str:
    """
    Format retrieved documents.

    Adds document boundaries to help LLM
    understand context separation.
    """

    if not contexts:

        return "No relevant context found."


    formatted = []


    for index, context in enumerate(
        contexts,
        start=1,
    ):

        formatted.append(
            f"""
--- Document {index} ---

{context}

--- End Document {index} ---
"""
        )


    return "\n".join(
        formatted
    )



###############################################################################
# Main Chat Prompt Builder
###############################################################################


def build_chat_prompt(
    data: ChatPromptInput,
) -> str:
    """
    Build final RAG chat prompt.

    Used by:
    - ChatService
    - StreamingChatService
    - Evaluation pipeline

    """


    context = format_context(
        data.context
    )


    history = format_conversation_history(
        data.conversation_history
    )



    return f"""
Conversation History:

{history}


Retrieved Knowledge Context:

{context}


User Question:

{data.question}


Instructions:

Answer the user question using the retrieved context.

Requirements:

- Do not use unsupported information.
- Explain clearly.
- Provide references if available.
- If context is insufficient, say so.

Answer:
"""



###############################################################################
# Streaming Chat Prompt
###############################################################################


def build_streaming_prompt(
    question: str,
    context: list[str],
) -> str:
    """
    Lightweight prompt for streaming responses.

    Used when:
    - User expects real-time output
    """

    return f"""
Context:

{format_context(context)}


Question:

{question}


Generate the answer:
"""



###############################################################################
# Follow-up Question Prompt
###############################################################################


FOLLOW_UP_PROMPT = """
You are maintaining a conversation.

Given previous conversation and new question:

Conversation:

{history}


New Question:

{question}


Determine whether the new question depends on previous context.

Return:

{
    "is_follow_up": true|false,
    "standalone_question": "rewritten question"
}
"""



def build_follow_up_prompt(
    history: list[dict[str, str]],
    question: str,
) -> str:
    """
    Build follow-up detection prompt.
    """

    return FOLLOW_UP_PROMPT.format(

        history=format_conversation_history(
            history
        ),

        question=question,

    )



###############################################################################
# Citation Prompt
###############################################################################


CITATION_INSTRUCTION = """
When answering:

- Mention relevant document names.
- Add citations in this format:

[Source: document_name]

Example:

The authentication service uses OAuth2.

[Source: security-guide.pdf]

"""



def build_citation_prompt(
    answer: str,
    sources: list[str],
) -> str:
    """
    Add citation request to generated answer.
    """

    return f"""
Answer:

{answer}


Available Sources:

{sources}


Add appropriate citations.
"""



###############################################################################
# Prompt Metadata
###############################################################################


def get_chat_prompt_metadata() -> dict[str, str]:
    """
    Return prompt information.

    Useful for:
    - Monitoring
    - Evaluation
    - Prompt versioning
    """

    return {

        "name": "rag_chat_prompt",

        "version": "1.0",

        "type": "retrieval_augmented_generation",

    }