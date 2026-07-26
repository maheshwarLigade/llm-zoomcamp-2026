"""
OpenAI LLM Provider

Implementation of OpenAI Chat Completion API.

Supports:
- GPT models
- Streaming responses
- Token tracking
- Latency measurement
- Metadata collection

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import time

from typing import Any
from typing import AsyncIterator


from openai import AsyncOpenAI


from app.llm.providers.base import (
    BaseLLMProvider,
    LLMResponse,
    LLMStreamChunk,
)



###############################################################################
# OpenAI Provider
###############################################################################


class OpenAIProvider(
    BaseLLMProvider
):
    """
    OpenAI LLM implementation.

    Example:

        llm = OpenAIProvider(
            api_key="xxxx",
            model="gpt-4.1-mini"
        )

        response = await llm.generate(
            "Explain RAG"
        )
    """


    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        endpoint: str | None = None,
        deployment: str | None = None,
    ):

        self.model = model

        self.temperature = temperature

        self.max_tokens = max_tokens

        self.deployment = deployment


        self.client = AsyncOpenAI(

            api_key=api_key,

            base_url=endpoint,

        )



    ###########################################################################
    # Generate Completion
    ###########################################################################


    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Generate response from OpenAI.

        Used by:

        - Chat generation
        - Query rewriting
        - Evaluation
        - Summarization
        """


        start_time = time.perf_counter()


        messages = []


        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )


        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )


        response = await self.client.chat.completions.create(

            model=self.deployment or self.model,

            messages=messages,

            temperature=kwargs.get(
                "temperature",
                self.temperature,
            ),

            max_tokens=kwargs.get(
                "max_tokens",
                self.max_tokens,
            ),

        )


        latency = (

            time.perf_counter()

            -

            start_time

        ) * 1000



        choice = response.choices[0]


        usage = response.usage



        return LLMResponse(

            content=choice.message.content,

            model=self.model,

            latency_ms=latency,


            prompt_tokens=(

                usage.prompt_tokens

                if usage

                else 0

            ),


            completion_tokens=(

                usage.completion_tokens

                if usage

                else 0

            ),


            metadata={

                "provider": "openai",

                "finish_reason":
                    choice.finish_reason,

                "system_fingerprint":
                    getattr(
                        response,
                        "system_fingerprint",
                        None,
                    ),

            },

        )



    ###########################################################################
    # Streaming
    ###########################################################################


    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream OpenAI response.

        Used for:
        - Chat UI streaming
        - Interactive responses
        """


        messages = []


        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )


        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )



        stream = await self.client.chat.completions.create(

            model=self.deployment or self.model,

            messages=messages,

            temperature=kwargs.get(
                "temperature",
                self.temperature,
            ),

            max_tokens=kwargs.get(
                "max_tokens",
                self.max_tokens,
            ),

            stream=True,

        )



        async for chunk in stream:


            delta = (

                chunk
                .choices[0]
                .delta
                .content

            )


            if delta:

                yield LLMStreamChunk(

                    content=delta,

                    model=self.model,

                    metadata={

                        "provider": "openai"

                    },

                )



    ###########################################################################
    # Embedding Support
    ###########################################################################


    async def create_embedding(
        self,
        text: str,
        embedding_model: str = "text-embedding-3-small",
    ) -> list[float]:
        """
        Generate embeddings.

        Used by:

        - Document ingestion
        - Semantic retrieval
        """


        response = await self.client.embeddings.create(

            model=embedding_model,

            input=text,

        )


        return (
            response
            .data[0]
            .embedding
        )



    ###########################################################################
    # Model Metadata
    ###########################################################################


    def get_model_name(
        self,
    ) -> str:
        """
        Return model name.
        """

        return self.model



    def get_provider_name(
        self,
    ) -> str:
        """
        Return provider name.
        """

        return "openai"



    ###########################################################################
    # Health Check
    ###########################################################################


    async def health_check(
        self,
    ) -> bool:
        """
        Validate OpenAI connectivity.
        """

        try:

            await self.client.models.list()

            return True


        except Exception:

            return False



    ###########################################################################
    # Cleanup
    ###########################################################################


    async def close(
        self,
    ):
        """
        Close OpenAI client.
        """

        await self.client.close()