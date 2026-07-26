"""
Tokenizer Utilities

Provides token counting, text splitting, and token
management utilities for the RAG pipeline.

Used for:
- Chunk creation
- Prompt optimization
- Context window management
- LLM cost estimation
- Retrieval filtering

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass
from typing import Iterator


###############################################################################
# Optional tokenizer imports
###############################################################################

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True

except ImportError:

    TIKTOKEN_AVAILABLE = False



try:
    from transformers import AutoTokenizer

    TRANSFORMERS_AVAILABLE = True

except ImportError:

    TRANSFORMERS_AVAILABLE = False



###############################################################################
# Token Information
###############################################################################


@dataclass
class TokenInfo:
    """
    Token statistics.
    """

    text_length: int

    token_count: int

    average_token_length: float



###############################################################################
# Tokenizer Provider
###############################################################################


class Tokenizer:
    """
    Generic tokenizer abstraction.

    Supports:

    - OpenAI tiktoken
    - HuggingFace tokenizer
    - Approximation fallback


    Example:

        tokenizer = Tokenizer(
            model="gpt-4o"
        )

        count = tokenizer.count(
            "Hello world"
        )

    """

    def __init__(
        self,
        model: str = "gpt-4o",
    ):

        self.model = model

        self.encoder = None


        self._initialize()



    def _initialize(self):

        """
        Initialize tokenizer backend.
        """

        if TIKTOKEN_AVAILABLE:

            try:

                self.encoder = (
                    tiktoken.encoding_for_model(
                        self.model
                    )
                )

                return

            except Exception:

                pass



        if TRANSFORMERS_AVAILABLE:

            try:

                self.encoder = (
                    AutoTokenizer.from_pretrained(
                        self.model
                    )
                )

                return

            except Exception:

                pass



    ###########################################################################
    # Encoding
    ###########################################################################


    def encode(
        self,
        text: str,
    ) -> list[int]:
        """
        Convert text into token IDs.
        """

        if self.encoder is None:

            return self._fallback_encode(
                text
            )


        if TIKTOKEN_AVAILABLE and hasattr(
            self.encoder,
            "encode",
        ):

            return self.encoder.encode(
                text
            )


        return self.encoder(
            text
        ).input_ids



    def decode(
        self,
        tokens: list[int],
    ) -> str:
        """
        Convert tokens back to text.
        """

        if self.encoder is None:

            return ""



        if hasattr(
            self.encoder,
            "decode",
        ):

            return self.encoder.decode(
                tokens
            )


        return self.encoder.decode(
            tokens
        )



    ###########################################################################
    # Counting
    ###########################################################################


    def count(
        self,
        text: str,
    ) -> int:
        """
        Count tokens.
        """

        return len(
            self.encode(text)
        )



    def info(
        self,
        text: str,
    ) -> TokenInfo:
        """
        Return token statistics.
        """

        tokens = self.count(
            text
        )

        return TokenInfo(

            text_length=len(text),

            token_count=tokens,

            average_token_length=(
                len(text) / tokens
                if tokens
                else 0
            ),
        )



    ###########################################################################
    # Chunking
    ###########################################################################


    def split_by_tokens(
        self,
        text: str,
        max_tokens: int = 512,
        overlap: int = 50,
    ) -> list[str]:
        """
        Split text into token based chunks.

        Used during ingestion.

        Example:

        Document
            |
            |
        Tokenizer
            |
            |
        Chunk1
        Chunk2
        Chunk3

        """

        tokens = self.encode(
            text
        )


        chunks = []


        start = 0


        while start < len(tokens):

            end = (
                start
                +
                max_tokens
            )


            chunk_tokens = tokens[
                start:end
            ]


            chunks.append(
                self.decode(
                    chunk_tokens
                )
            )


            start = (
                end
                -
                overlap
            )


            if start < 0:

                start = 0


        return chunks



###############################################################################
# Context Window Management
###############################################################################


def truncate_tokens(
    text: str,
    max_tokens: int,
    tokenizer: Tokenizer,
) -> str:
    """
    Truncate text to token limit.
    """

    tokens = tokenizer.encode(
        text
    )


    if len(tokens) <= max_tokens:

        return text



    return tokenizer.decode(
        tokens[:max_tokens]
    )



def fit_context_window(
    contexts: list[str],
    max_tokens: int,
    tokenizer: Tokenizer,
) -> list[str]:
    """
    Select contexts that fit into
    LLM context window.

    Used in RAG prompt construction.
    """

    selected = []

    total = 0


    for context in contexts:

        count = tokenizer.count(
            context
        )


        if (
            total + count
            >
            max_tokens
        ):
            break


        selected.append(
            context
        )


        total += count


    return selected



###############################################################################
# Prompt Token Estimation
###############################################################################


def estimate_prompt_tokens(
    system_prompt: str,
    user_prompt: str,
    contexts: list[str],
    tokenizer: Tokenizer,
) -> int:
    """
    Estimate total prompt tokens.
    """

    total_text = (

        system_prompt

        +

        user_prompt

        +

        "\n".join(contexts)

    )


    return tokenizer.count(
        total_text
    )



###############################################################################
# Fallback Tokenizer
###############################################################################


def _fallback_encode(
    text: str,
) -> list[int]:
    """
    Simple approximation tokenizer.

    Used when no tokenizer
    library is available.

    Approximation:
        1 token ~= 4 chars
    """

    return list(
        range(
            max(
                1,
                len(text)//4
            )
        )
    )



###############################################################################
# Factory
###############################################################################


def get_tokenizer(
    model: str = "gpt-4o",
) -> Tokenizer:
    """
    Create tokenizer instance.
    """

    return Tokenizer(
        model=model
    )