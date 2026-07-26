"""
Chat Service

Main orchestration service for RAG conversations.

Responsibilities:

- Manage conversation flow
- Retrieve context
- Generate LLM response
- Store messages
- Maintain conversation state


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass, field


from typing import Protocol, Any


from app.domain.repositories.conversation_repository import (
    ConversationRepository,
)


from app.domain.services.retrieval_service import (
    RetrievalService,
    RetrievalRequest,
)


from app.domain.services.reranking_service import (
    RerankingService,
    RerankingRequest,
)



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class LLMProvider(Protocol):
    """
    Contract for LLM providers.

    Implementations:

    - OpenAI
    - Groq
    - Ollama
    - Gemini
    - Claude

    """

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> "LLMResponse":
        ...



class PromptBuilder(Protocol):
    """
    Builds final LLM prompt.
    """

    def build(
        self,
        question: str,
        history: list[Any],
        context: str,
    ) -> list[dict[str, str]]:
        ...



###############################################################################
# Request / Response Models
###############################################################################


@dataclass
class ChatRequest:
    """
    Incoming chat request.
    """

    conversation_id: str

    user_id: str

    message: str

    temperature: float = 0.2

    retrieval_top_k: int = 10

    rerank_top_k: int = 5



@dataclass
class LLMResponse:
    """
    Response returned by LLM provider.
    """

    content: str

    model: str

    input_tokens: int = 0

    output_tokens: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class ChatResponse:
    """
    Final chat response.
    """

    conversation_id: str

    answer: str

    sources: list[str]

    model: str

    usage: dict[str, int]



###############################################################################
# Chat Service
###############################################################################


class ChatService:
    """
    Orchestrates complete RAG chat workflow.

    """



    def __init__(
        self,
        conversation_repository: ConversationRepository,
        retrieval_service: RetrievalService,
        reranking_service: RerankingService,
        llm_provider: LLMProvider,
        prompt_builder: PromptBuilder,
    ):

        self.conversation_repository = (
            conversation_repository
        )

        self.retrieval_service = (
            retrieval_service
        )

        self.reranking_service = (
            reranking_service
        )

        self.llm_provider = (
            llm_provider
        )

        self.prompt_builder = (
            prompt_builder
        )



    ###########################################################################
    # Main Chat API
    ###########################################################################


    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Execute RAG chat workflow.

        Steps:

        1. Load conversation history
        2. Store user message
        3. Retrieve documents
        4. Rerank results
        5. Build prompt
        6. Generate answer
        7. Store assistant response

        """

        try:

            ###################################################################
            # Conversation History
            ###################################################################

            history = await (
                self.conversation_repository
                .get_recent_context(
                    request.conversation_id,
                    message_limit=10,
                )
            )



            ###################################################################
            # Save User Message
            ###################################################################

            await (
                self.conversation_repository
                .add_message(
                    request.conversation_id,
                    {
                        "role": "user",
                        "content": request.message,
                    },
                )
            )



            ###################################################################
            # Retrieval
            ###################################################################

            retrieval_response = await (
                self.retrieval_service.retrieve(

                    RetrievalRequest(

                        query=request.message,

                        top_k=request.retrieval_top_k,

                    )

                )
            )



            ###################################################################
            # Reranking
            ###################################################################

            rerank_response = await (
                self.reranking_service.rerank(

                    RerankingRequest(

                        query=request.message,

                        candidates=
                            retrieval_response.results,

                        top_k=request.rerank_top_k,

                    )

                )
            )



            context = (
                self.reranking_service
                .build_context(
                    rerank_response
                )
            )



            ###################################################################
            # Prompt Construction
            ###################################################################

            messages = (
                self.prompt_builder.build(

                    question=request.message,

                    history=history,

                    context=context,

                )
            )



            ###################################################################
            # LLM Generation
            ###################################################################

            llm_response = await (
                self.llm_provider.generate(

                    messages,

                    temperature=request.temperature,

                )
            )



            ###################################################################
            # Save Assistant Response
            ###################################################################

            await (
                self.conversation_repository
                .add_message(

                    request.conversation_id,

                    {
                        "role": "assistant",

                        "content":
                            llm_response.content,

                    },

                )
            )



            ###################################################################
            # Return Response
            ###################################################################

            sources = [

                result.chunk.id

                for result
                in rerank_response.results

            ]



            return ChatResponse(

                conversation_id=
                    request.conversation_id,

                answer=
                    llm_response.content,

                sources=sources,

                model=
                    llm_response.model,

                usage={

                    "input_tokens":
                        llm_response.input_tokens,

                    "output_tokens":
                        llm_response.output_tokens,

                },

            )



        except Exception as exc:

            logger.exception(
                "Chat processing failed"
            )

            raise exc



    ###########################################################################
    # Streaming Support
    ###########################################################################


    async def stream_chat(
        self,
        request: ChatRequest,
    ):
        """
        Streaming response support.

        Useful for:

        - ChatGPT style UI
        - Token streaming

        """

        response = await self.chat(
            request
        )


        yield response.answer



    ###########################################################################
    # Conversation Management
    ###########################################################################


    async def get_history(
        self,
        conversation_id: str,
    ):

        return await (
            self.conversation_repository
            .get_messages(
                conversation_id
            )
        )



    async def clear_context(
        self,
        conversation_id: str,
    ):

        await (
            self.conversation_repository
            .update_summary(
                conversation_id,
                "",
            )
        )