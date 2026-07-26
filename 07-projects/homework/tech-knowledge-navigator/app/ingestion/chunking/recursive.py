"""
Recursive Text Chunking Strategy

Splits documents while preserving semantic boundaries.

Splitting priority:

1. Paragraph
2. New line
3. Sentence
4. Word
5. Token


Used for:

- Technical documentation
- Knowledge bases
- Books
- Enterprise documents


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import re


from dataclasses import dataclass, field


from typing import Protocol


logger = logging.getLogger(__name__)



###############################################################################
# Tokenizer Contract
###############################################################################


class Tokenizer(Protocol):
    """
    Tokenizer abstraction.
    """

    def encode(
        self,
        text: str,
    ) -> list[int]:
        ...


    def decode(
        self,
        tokens: list[int],
    ) -> str:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class RecursiveChunkMetadata:
    """
    Chunk metadata.
    """

    chunk_index: int

    level: str

    token_count: int

    character_count: int

    start_position: int

    end_position: int



@dataclass
class RecursiveChunk:
    """
    Generated chunk.
    """

    content: str

    metadata: RecursiveChunkMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class RecursiveChunkConfig:
    """
    Recursive splitting configuration.
    """

    chunk_size: int = 500

    overlap: int = 50


    separators: list[str] = field(

        default_factory=lambda: [

            "\n\n",      # Paragraph

            "\n",        # Line

            ". ",        # Sentence

            ", ",        # Clause

            " ",         # Word

        ]

    )



    def validate(self):

        if self.chunk_size <= 0:

            raise ValueError(
                "chunk_size must be positive"
            )


        if self.overlap >= self.chunk_size:

            raise ValueError(
                "overlap must be smaller than chunk size"
            )



###############################################################################
# Recursive Chunker
###############################################################################


class RecursiveChunker:
    """
    Recursive document splitter.

    Strategy:

    Try large semantic separators first.

    If resulting pieces are too large,
    recursively split using smaller separators.

    """



    def __init__(
        self,
        tokenizer: Tokenizer,
        config: RecursiveChunkConfig | None = None,
    ):

        self.tokenizer = tokenizer


        self.config = (

            config

            or RecursiveChunkConfig()

        )


        self.config.validate()



    ###########################################################################
    # Public API
    ###########################################################################


    async def split(
        self,
        text: str,
    ) -> list[RecursiveChunk]:
        """
        Split document recursively.
        """

        if not text:

            return []


        pieces = await self._recursive_split(

            text,

            self.config.separators,

        )


        chunks = (
            self._merge_pieces(
                pieces
            )
        )


        logger.info(

            "Created %s recursive chunks",

            len(chunks),

        )


        return chunks



    ###########################################################################
    # Recursive Splitting
    ###########################################################################


    async def _recursive_split(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:
        """
        Recursive splitting algorithm.
        """

        token_count = len(

            self.tokenizer.encode(
                text
            )

        )


        #
        # Already small enough
        #

        if token_count <= self.config.chunk_size:

            return [
                text.strip()
            ]



        #
        # No separators left
        #

        if not separators:

            return (
                self._split_by_tokens(
                    text
                )
            )



        separator = separators[0]


        parts = text.split(
            separator
        )


        result = []


        current_level = (
            separators[1:]
        )



        for part in parts:


            if not part.strip():

                continue



            child_chunks = await (

                self._recursive_split(

                    part,

                    current_level,

                )

            )


            result.extend(
                child_chunks
            )


        return result



    ###########################################################################
    # Token Level Split
    ###########################################################################


    def _split_by_tokens(
        self,
        text: str,
    ) -> list[str]:
        """
        Final fallback split.

        """

        tokens = (
            self.tokenizer.encode(
                text
            )
        )


        chunks = []


        step = (

            self.config.chunk_size

            -

            self.config.overlap

        )


        start = 0


        while start < len(tokens):

            end = (

                start

                +

                self.config.chunk_size

            )


            chunk_tokens = tokens[
                start:end
            ]


            chunks.append(

                self.tokenizer.decode(
                    chunk_tokens
                )

            )


            start += step



        return chunks



    ###########################################################################
    # Merge Small Pieces
    ###########################################################################


    def _merge_pieces(
        self,
        pieces: list[str],
    ) -> list[RecursiveChunk]:
        """
        Merge small pieces together
        until chunk size is reached.
        """

        chunks = []


        buffer = ""


        index = 0


        position = 0



        for piece in pieces:


            candidate = (

                buffer

                +

                "\n"

                +

                piece

            )



            candidate_tokens = len(

                self.tokenizer.encode(
                    candidate
                )

            )



            if (

                candidate_tokens
                <=
                self.config.chunk_size

            ):

                buffer = candidate


            else:


                if buffer.strip():

                    chunks.append(

                        self._create_chunk(

                            buffer,

                            index,

                            position,

                        )

                    )


                    index += 1


                    position += len(buffer)



                buffer = piece



        if buffer.strip():

            chunks.append(

                self._create_chunk(

                    buffer,

                    index,

                    position,

                )

            )



        return chunks



    ###########################################################################
    # Create Chunk
    ###########################################################################


    def _create_chunk(
        self,
        content: str,
        index: int,
        position: int,
    ) -> RecursiveChunk:

        token_count = len(

            self.tokenizer.encode(
                content
            )

        )


        return RecursiveChunk(

            content=content.strip(),


            metadata=RecursiveChunkMetadata(

                chunk_index=index,

                level="recursive",

                token_count=token_count,

                character_count=len(content),

                start_position=position,

                end_position=(
                    position
                    +
                    len(content)
                ),

            ),

        )