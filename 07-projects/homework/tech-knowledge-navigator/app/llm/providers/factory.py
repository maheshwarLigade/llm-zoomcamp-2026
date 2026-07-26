"""
LLM Provider Factory

Creates LLM provider instances based on configuration.

Supported providers:
- OpenAI
- Azure OpenAI
- Google Gemini
- Anthropic Claude
- Ollama

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from functools import lru_cache

from app.core.config import settings

from app.llm.providers.base import (
    BaseLLMProvider,
)


from app.llm.providers.openai import (
    OpenAIProvider,
)

from app.llm.providers.gemini import (
    GeminiProvider,
)

from app.llm.providers.ollama import (
    OllamaProvider,
)

from app.llm.providers.anthropic import (
    AnthropicProvider,
)



###############################################################################
# Provider Constants
###############################################################################


class LLMProviderType:

    OPENAI = "openai"

    AZURE_OPENAI = "azure_openai"

    GEMINI = "gemini"

    ANTHROPIC = "anthropic"

    OLLAMA = "ollama"



###############################################################################
# Factory
###############################################################################


class LLMProviderFactory:
    """
    Factory responsible for creating LLM providers.

    Example:

        llm = LLMProviderFactory.create()

        response = await llm.generate(
            prompt
        )
    """


    @staticmethod
    def create(
        provider: str | None = None,
    ) -> BaseLLMProvider:
        """
        Create LLM provider instance.

        Provider resolution order:

        1. Explicit argument
        2. Application configuration

        """


        selected_provider = (
            provider
            or settings.LLM_PROVIDER
        )


        selected_provider = (
            selected_provider.lower()
        )


        match selected_provider:


            case LLMProviderType.OPENAI:

                return OpenAIProvider(
                    api_key=settings.OPENAI_API_KEY,
                    model=settings.OPENAI_MODEL,
                )



            case LLMProviderType.AZURE_OPENAI:

                return OpenAIProvider(
                    api_key=settings.AZURE_OPENAI_KEY,

                    model=settings.AZURE_OPENAI_MODEL,

                    endpoint=settings.AZURE_OPENAI_ENDPOINT,

                    deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                )



            case LLMProviderType.GEMINI:

                return GeminiProvider(
                    api_key=settings.GEMINI_API_KEY,

                    model=settings.GEMINI_MODEL,
                )



            case LLMProviderType.ANTHROPIC:

                return AnthropicProvider(
                    api_key=settings.ANTHROPIC_API_KEY,

                    model=settings.ANTHROPIC_MODEL,
                )



            case LLMProviderType.OLLAMA:

                return OllamaProvider(
                    base_url=settings.OLLAMA_URL,

                    model=settings.OLLAMA_MODEL,
                )



            case _:

                raise ValueError(
                    f"Unsupported LLM provider: "
                    f"{selected_provider}"
                )



###############################################################################
# Cached Factory
###############################################################################


@lru_cache(maxsize=1)
def get_llm_provider() -> BaseLLMProvider:
    """
    Application singleton LLM instance.

    Avoids recreating clients for every request.

    Used by:
    - Chat service
    - Evaluation service
    - Query rewriting service
    """

    return LLMProviderFactory.create()