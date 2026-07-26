"""
Ollama LLM Provider

Local LLM implementation using Ollama.

Supports:
- Local inference
- Chat completion
- Streaming responses
- Token usage tracking
- Latency measurement

Supported models:
- llama3.1
- llama3.3
- mistral
- qwen2.5
- gemma

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import time

from typing import AsyncIterator
from typing import Any


import httpx


from app.llm.providers.base import (
    BaseLLMProvider,
    LLMResponse,
    LLMStreamChunk,
)



###############################################################################
# Ollama Provider
###############################################################################


class OllamaProvider(
    BaseLLMProvider
):
    """
    Ollama local LLM provider.

    Example:

        llm = OllamaProvider(
            base_url="http://localhost:11434",
            model="llama3.1"
        )

        response = await llm.generate(
            "Explain RAG architecture"
        )

    """



    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1",
        temperature: float = 0.2,
        max_tokens: int = 2048,
        timeout: int = 120,
    ):

        self.base_url = (
            base_url.rstrip("/")
        )

        self.model = model

        self.temperature = temperature

        self.max_tokens = max_tokens


        self.client = httpx.AsyncClient(
            timeout=timeout
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
        Generate response using Ollama.

        Endpoint:

        POST /api/chat
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



        payload = {

            "model": self.model,

            "messages": messages,

            "stream": False,

            "options": {

                "temperature": kwargs.get(
                    "temperature",
                    self.temperature,
                ),

                "num_predict": kwargs.get(
                    "max_tokens",
                    self.max_tokens,
                ),

            },
        }



        response = await self.client.post(

            f"{self.base_url}/api/chat",

            json=payload,

        )


        response.raise_for_status()


        result = response.json()



        latency = (

            time.perf_counter()

            -

            start

        ) * 1000



        return LLMResponse(

            content=result["message"]["content"],

            model=self.model,

            latency_ms=latency,

            prompt_tokens=result.get(
                "prompt_eval_count",
                0,
            ),

            completion_tokens=result.get(
                "eval_count",
                0,
            ),

            metadata={

                "provider": "ollama",

                "done_reason": result.get(
                    "done_reason"
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
        Stream tokens from Ollama.
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



        payload = {

            "model": self.model,

            "messages": messages,

            "stream": True,

            "options": {

                "temperature": kwargs.get(
                    "temperature",
                    self.temperature,
                ),

                "num_predict": kwargs.get(
                    "max_tokens",
                    self.max_tokens,
                ),
            },
        }



        async with self.client.stream(

            "POST",

            f"{self.base_url}/api/chat",

            json=payload,

        ) as response:


            response.raise_for_status()


            async for line in response.aiter_lines():


                if not line:

                    continue


                data = httpx.Response(

                    200,

                    content=line

                ).json()



                content = (

                    data
                    .get("message", {})
                    .get("content")
                )


                if content:

                    yield LLMStreamChunk(

                        content=content,

                        model=self.model,

                        metadata={
                            "provider": "ollama"
                        },

                    )



    ###########################################################################
    # Model Information
    ###########################################################################


    async def list_models(
        self,
    ) -> list[str]:
        """
        Return available local models.

        Endpoint:

        GET /api/tags
        """


        response = await self.client.get(

            f"{self.base_url}/api/tags"

        )


        response.raise_for_status()


        data = response.json()


        return [

            model["name"]

            for model in data.get(
                "models",
                []
            )

        ]



    ###########################################################################
    # Provider Metadata
    ###########################################################################


    def get_model_name(
        self,
    ) -> str:
        """
        Current model name.
        """

        return self.model



    def get_provider_name(
        self,
    ) -> str:
        """
        Provider name.
        """

        return "ollama"



    ###########################################################################
    # Cleanup
    ###########################################################################


    async def close(
        self,
    ):
        """
        Close HTTP client.
        """

        await self.client.aclose()