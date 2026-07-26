"""
Fixed Size Chunking Strategy

Splits documents into fixed-size chunks
with configurable overlap.

Used for:

- PDF documents
- Technical documentation
- Books
- Long text files


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass


from typing import Protocol


logger = logging.getLogger(__name__)



###############################################################################
# Tokenizer Contract
###############################################################################


class Tokenizer(Protocol):
    """
    Tokenizer abstraction.

    Implementations:

    - tiktoken
    - HuggingFace tokenizer
    - SentencePiece

    """

    def encode(
        self,
        text: str,
    ) -> list[int]:
        """
        Convert text into tokens.
        """
        ...


    def decode(
        self,
        tokens: list[int],
    ) -> str:
        """
        Convert tokens back to text.
        """
        ...



###############################################################################
# Chunk Models
###############################################################################


@dataclass
class ChunkMetadata:
    """
    Metadata attached to chunk.
    """

    chunk_index: int

    start_token: int

    end_token: int

    token_count: int

    character_count: int



@dataclass
class TextChunk:
    """
    Generated text chunk.
    """

    content: str

    metadata: ChunkMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class FixedChunkConfig:
    """
    Fixed chunking configuration.

    Example:

    chunk_size=500
    overlap=50

    """

    chunk_size: int = 500

    overlap: int = 50



    def validate(self):
        """
        Validate configuration.
        """

        if self.chunk_size <= 0:

            raise ValueError(
                "chunk_size must be greater than zero"
            )


        if self.overlap >= self.chunk_size:

            raise ValueError(
                "overlap must be smaller than chunk size"
            )


        if self.overlap < 0:

            raise ValueError(
                "overlap cannot be negative"
            )



###############################################################################
# Fixed Chunker
###############################################################################


class FixedChunker:
    """
    Fixed size text chunker.

    Algorithm:

    1. Tokenize document
    2. Create windows
    3. Move window by
       chunk_size - overlap
    4. Decode tokens

    """



    def __init__(
        self,
        tokenizer: Tokenizer,
        config: FixedChunkConfig | None = None,
    ):

        self.tokenizer = tokenizer


        self.config = (
            config
            or FixedChunkConfig()
        )


        self.config.validate()



    ###########################################################################
    # Public API
    ###########################################################################


    async def split(
        self,
        text: str,
    ) -> list[TextChunk]:
        """
        Split text into fixed chunks.

        """

        if not text:

            return []



        tokens = self.tokenizer.encode(
            text
        )


        chunks: list[TextChunk] = []


        start = 0

        index = 0



        while start < len(tokens):

            end = (
                start
                +
                self.config.chunk_size
            )


            chunk_tokens = tokens[
                start:end
            ]


            content = (
                self.tokenizer.decode(
                    chunk_tokens
                )
            )


            chunks.append(

                TextChunk(

                    content=content,

                    metadata=ChunkMetadata(

                        chunk_index=index,

                        start_token=start,

                        end_token=end,

                        token_count=
                            len(chunk_tokens),

                        character_count=
                            len(content),

                    ),

                )

            )


            index += 1



            ###################################################################
            # Move window
            ###################################################################

            start += (

                self.config.chunk_size

                -
                
                self.config.overlap

            )



        logger.info(

            "Created %s chunks using fixed strategy",

            len(chunks),

        )


        return chunks



    ###########################################################################
    # Utility Methods
    ###########################################################################


    def estimate_chunks(
        self,
        text: str,
    ) -> int:
        """
        Estimate number of chunks.

        Formula:

        ceil(
            tokens /
            (chunk_size - overlap)
        )

        """

        tokens = len(
            self.tokenizer.encode(text)
        )


        step = (

            self.config.chunk_size

            -
            
            self.config.overlap

        )


        return (
            (tokens + step - 1)
            //
            step
        )