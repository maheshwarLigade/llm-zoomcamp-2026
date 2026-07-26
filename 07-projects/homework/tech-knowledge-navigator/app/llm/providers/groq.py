"""
Groq LLM Provider

Implementation of Groq LLM client.

Supports:
- Chat completion
- Streaming responses
- Token usage tracking
- Latency measurement

Groq provides OpenAI-compatible APIs.

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import time

from typing import AsyncIterator
from typing import Any


from groq import AsyncGroq


from app.llm.providers.base import (
    BaseLLMProvider,
    LLMResponse,
    LLMStreamChunk,
)



###############################################################################
# Groq Provider
###############################################################################


class GroqProvider(
    BaseLLMProvider
):
    """
    Groq LLM implementation.

    Example:

        llm = GroqProvider(
            api_key="xxx",
            model="llama-3.1-70b-versatile"
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
    ):

        self.client = AsyncGroq(
            api_key=api_key
        )


        self.model = model

        self.temperature = temperature

        self.max_tokens = max_tokens



    ###########################################################################
    # Generate
    ###########################################################################


    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Generate completion.

        Used by:
        - Chat service
        - Query rewriting
        - Evaluation
        """

        start = time.perf_counter()


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

            model=self.model,

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
            start
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
                "provider": "groq",
                "finish_reason": choice.finish_reason,
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
        Stream tokens from Groq.
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

            model=self.model,

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
                        "provider": "groq"
                    },

                )



    ###########################################################################
    # Metadata
    ###########################################################################


    def get_model_name(
        self,
    ) -> str:
        """
        Return current model.
        """

        return self.model



    def get_provider_name(
        self,
    ) -> str:
        """
        Return provider name.
        """

        return "groq"