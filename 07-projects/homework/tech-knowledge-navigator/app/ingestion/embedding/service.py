"""
Embedding Service

Central service responsible for generating
vector embeddings.

Responsibilities:

- Generate single embeddings
- Generate batch embeddings
- Validate input
- Track metadata
- Abstract embedding providers


Supported providers:

- OpenAI Embeddings
- Ollama Embeddings
- HuggingFace Embeddings
- Azure OpenAI


Pipeline:

Text
 |
 v
EmbeddingService
 |
 v
EmbeddingProvider
 |
 v
Vector
 |
 v
Vector Repository


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import time


from dataclasses import dataclass, field


from datetime import datetime


from typing import Protocol



logger = logging.getLogger(__name__)



###############################################################################
# External Contracts
###############################################################################


class EmbeddingProvider(Protocol):
    """
    Embedding provider abstraction.

    Implementations:

    - OpenAIEmbeddingProvider
    - OllamaEmbeddingProvider
    - HuggingFaceEmbeddingProvider

    """

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        ...


    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class EmbeddingRequest:
    """
    Embedding input.
    """

    text: str

    document_id: str | None = None

    chunk_id: str | None = None

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class EmbeddingResult:
    """
    Generated embedding result.
    """

    vector: list[float]

    dimension: int

    model: str | None

    document_id: str | None

    chunk_id: str | None

    created_at: datetime

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class BatchEmbeddingResult:
    """
    Batch embedding response.
    """

    embeddings: list[EmbeddingResult]

    total_processed: int

    processing_time_ms: float



###############################################################################
# Configuration
###############################################################################


@dataclass
class EmbeddingServiceConfig:
    """
    Embedding service configuration.
    """

    model_name: str = "default"

    batch_size: int = 50

    max_text_length: int = 10000

    enable_logging: bool = True



###############################################################################
# Embedding Service
###############################################################################


class EmbeddingService:
    """
    Application level embedding service.

    """



    def __init__(
        self,
        provider: EmbeddingProvider,
        config: EmbeddingServiceConfig | None = None,
    ):

        self.provider = provider


        self.config = (

            config

            or EmbeddingServiceConfig()

        )



    ###########################################################################
    # Single Embedding
    ###########################################################################


    async def generate(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResult:
        """
        Generate embedding for single text.
        """

        self._validate_text(
            request.text
        )


        start = time.perf_counter()



        vector = await (

            self.provider.embed(

                request.text

            )

        )



        elapsed = (

            time.perf_counter()

            -

            start

        )



        if self.config.enable_logging:

            logger.info(

                "Generated embedding dimension=%s time=%sms",

                len(vector),

                round(
                    elapsed * 1000,
                    2
                ),

            )



        return EmbeddingResult(

            vector=vector,

            dimension=len(
                vector
            ),

            model=self.config.model_name,

            document_id=request.document_id,

            chunk_id=request.chunk_id,

            created_at=datetime.utcnow(),

            metadata={

                **request.metadata,

                "processing_time_ms":

                    round(
                        elapsed * 1000,
                        2
                    ),

            },

        )



    ###########################################################################
    # Batch Embedding
    ###########################################################################


    async def generate_batch(
        self,
        requests: list[EmbeddingRequest],
    ) -> BatchEmbeddingResult:
        """
        Generate embeddings in batches.

        """

        start = time.perf_counter()



        all_results = []



        for batch in self._batch(
            requests
        ):


            texts = [

                item.text

                for item in batch

            ]



            vectors = await (

                self.provider.embed_batch(

                    texts

                )

            )



            for request, vector in zip(

                batch,

                vectors,

            ):

                all_results.append(

                    EmbeddingResult(

                        vector=vector,

                        dimension=len(
                            vector
                        ),

                        model=self.config.model_name,

                        document_id=request.document_id,

                        chunk_id=request.chunk_id,

                        created_at=datetime.utcnow(),

                        metadata=request.metadata,

                    )

                )



        elapsed = (

            time.perf_counter()

            -

            start

        )



        return BatchEmbeddingResult(

            embeddings=all_results,

            total_processed=len(
                all_results
            ),

            processing_time_ms=(

                elapsed * 1000

            ),

        )



    ###########################################################################
    # Helpers
    ###########################################################################


    def _validate_text(
        self,
        text: str,
    ):
        """
        Validate embedding input.
        """

        if not text:

            raise ValueError(
                "Text cannot be empty"
            )


        if len(text) > self.config.max_text_length:

            raise ValueError(

                "Text exceeds maximum embedding length"

            )



    def _batch(
        self,
        items: list[EmbeddingRequest],
    ):
        """
        Split requests into batches.
        """

        size = self.config.batch_size


        for index in range(

            0,

            len(items),

            size,

        ):

            yield items[
                index:
                index + size
            ]