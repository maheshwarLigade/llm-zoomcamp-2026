"""
Semantic Chunking Strategy

Creates chunks based on semantic similarity
between sentences.

Pipeline:

Document
    |
    v
Sentence Splitting
    |
    v
Sentence Embeddings
    |
    v
Similarity Calculation
    |
    v
Boundary Detection
    |
    v
Semantic Chunks


Used for:

- Enterprise knowledge bases
- Research papers
- Technical documentation
- Long articles


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
# External Contracts
###############################################################################


class EmbeddingGenerator(Protocol):
    """
    Generates embeddings for sentences.
    """

    async def generate(
        self,
        text: str,
    ) -> list[float]:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class SemanticChunkMetadata:
    """
    Metadata for semantic chunk.
    """

    chunk_index: int

    sentence_count: int

    token_count: int

    similarity_score: float



@dataclass
class SemanticChunk:
    """
    Semantic chunk output.
    """

    content: str

    metadata: SemanticChunkMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class SemanticChunkConfig:
    """
    Semantic chunking configuration.
    """

    max_chunk_size: int = 500

    similarity_threshold: float = 0.75

    min_sentences: int = 2

    max_sentences: int = 20



    def validate(self):

        if self.max_chunk_size <= 0:

            raise ValueError(
                "max_chunk_size must be positive"
            )


        if not (
            0 < self.similarity_threshold <= 1
        ):

            raise ValueError(
                "similarity threshold must be between 0 and 1"
            )



###############################################################################
# Semantic Chunker
###############################################################################


class SemanticChunker:
    """
    Semantic based document splitter.

    Algorithm:

    1. Split document into sentences
    2. Generate embeddings
    3. Compare neighboring sentences
    4. Detect topic changes
    5. Create chunks

    """



    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        config: SemanticChunkConfig | None = None,
    ):

        self.embedding_generator = (
            embedding_generator
        )


        self.config = (

            config

            or SemanticChunkConfig()

        )


        self.config.validate()



    ###########################################################################
    # Public API
    ###########################################################################


    async def split(
        self,
        text: str,
    ) -> list[SemanticChunk]:
        """
        Split document semantically.
        """

        if not text.strip():

            return []



        sentences = (
            self._split_sentences(
                text
            )
        )


        if len(sentences) <= 1:

            return [

                self._create_chunk(

                    sentences,

                    0,

                    1.0,

                )

            ]



        embeddings = await (
            self._generate_embeddings(
                sentences
            )
        )



        groups = (
            self._detect_boundaries(
                sentences,
                embeddings,
            )
        )


        chunks = []


        for index, group in enumerate(groups):

            chunks.append(

                self._create_chunk(

                    group["sentences"],

                    index,

                    group["similarity"],

                )

            )



        logger.info(

            "Created %s semantic chunks",

            len(chunks),

        )


        return chunks



    ###########################################################################
    # Sentence Splitting
    ###########################################################################


    def _split_sentences(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into sentences.

        """

        sentences = re.split(

            r'(?<=[.!?])\s+',

            text.strip(),

        )


        return [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()

        ]



    ###########################################################################
    # Embedding Generation
    ###########################################################################


    async def _generate_embeddings(
        self,
        sentences: list[str],
    ) -> list[list[float]]:
        """
        Generate sentence embeddings.
        """

        embeddings = []


        for sentence in sentences:

            embedding = await (

                self.embedding_generator.generate(

                    sentence

                )

            )


            embeddings.append(
                embedding
            )


        return embeddings



    ###########################################################################
    # Boundary Detection
    ###########################################################################


    def _detect_boundaries(
        self,
        sentences: list[str],
        embeddings: list[list[float]],
    ) -> list[dict]:
        """
        Detect semantic boundaries.
        """

        groups = []


        current = []


        similarity_scores = []



        for index, sentence in enumerate(sentences):


            current.append(
                sentence
            )


            if index == len(sentences) - 1:

                break



            similarity = (
                self._cosine_similarity(

                    embeddings[index],

                    embeddings[index + 1],

                )
            )


            similarity_scores.append(
                similarity
            )


            should_split = (

                similarity
                <
                self.config.similarity_threshold

            )



            if should_split:


                groups.append(

                    {
                        "sentences": current,

                        "similarity":
                            sum(similarity_scores)
                            /
                            len(similarity_scores)
                            if similarity_scores
                            else 1.0,

                    }

                )


                current = []

                similarity_scores = []



        if current:

            groups.append(

                {

                    "sentences": current,

                    "similarity":
                        sum(similarity_scores)
                        /
                        len(similarity_scores)
                        if similarity_scores
                        else 1.0,

                }

            )


        return groups



    ###########################################################################
    # Similarity Calculation
    ###########################################################################


    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        """
        Calculate cosine similarity.
        """

        dot = sum(

            a * b

            for a, b

            in zip(
                vector_a,
                vector_b,
            )

        )


        norm_a = (

            sum(
                a * a
                for a in vector_a
            )
            ** 0.5

        )


        norm_b = (

            sum(
                b * b
                for b in vector_b
            )
            ** 0.5

        )


        if norm_a == 0 or norm_b == 0:

            return 0.0



        return dot / (
            norm_a * norm_b
        )



    ###########################################################################
    # Chunk Creation
    ###########################################################################


    def _create_chunk(
        self,
        sentences: list[str],
        index: int,
        similarity: float,
    ) -> SemanticChunk:

        content = "\n\n".join(
            sentences
        )


        return SemanticChunk(

            content=content,

            metadata=SemanticChunkMetadata(

                chunk_index=index,

                sentence_count=len(
                    sentences
                ),

                token_count=len(
                    content.split()
                ),

                similarity_score=similarity,

            ),

        )