"""
Qdrant Indexing Service

Vector database adapter for Qdrant.

Responsibilities:

- Create collections
- Store vectors
- Store metadata payload
- Bulk upsert vectors
- Delete vectors
- Manage collection lifecycle


Does not:

- Generate embeddings
- Chunk documents
- Clean documents
- Rank results


Pipeline:

Chunk
 |
 v
EmbeddingService
 |
 v
QdrantIndexer
 |
 v
Qdrant Vector Database


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
# External Contract
###############################################################################


class QdrantClient(Protocol):
    """
    Qdrant client abstraction.

    Implementation:

    - qdrant-client
    """

    async def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str,
    ):
        ...


    async def upsert(
        self,
        collection_name: str,
        points: list[dict],
    ):
        ...


    async def delete(
        self,
        collection_name: str,
        ids: list[str],
    ):
        ...


    async def collection_exists(
        self,
        collection_name: str,
    ) -> bool:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class VectorPoint:
    """
    Vector record stored in Qdrant.
    """

    id: str

    vector: list[float]

    content: str

    document_id: str

    chunk_id: str

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class QdrantIndexResult:
    """
    Index response.
    """

    id: str

    success: bool

    processing_time_ms: float

    indexed_at: datetime



@dataclass
class BulkIndexResult:
    """
    Bulk indexing result.
    """

    total: int

    successful: int

    failed: int

    errors: list[str] = field(
        default_factory=list
    )



###############################################################################
# Configuration
###############################################################################


@dataclass
class QdrantConfig:
    """
    Qdrant configuration.
    """

    collection_name: str = "rag_documents"

    vector_dimension: int = 1536

    distance: str = "Cosine"



###############################################################################
# Qdrant Indexer
###############################################################################


class QdrantIndexer:
    """
    Qdrant vector database indexer.

    """



    def __init__(
        self,
        client: QdrantClient,
        config: QdrantConfig | None = None,
    ):

        self.client = client


        self.config = (

            config

            or QdrantConfig()

        )



    ###########################################################################
    # Collection Management
    ###########################################################################


    async def create_collection(
        self,
    ):
        """
        Create Qdrant collection.
        """

        exists = await (

            self.client.collection_exists(

                self.config.collection_name

            )

        )


        if exists:

            logger.info(

                "Qdrant collection already exists: %s",

                self.config.collection_name,

            )

            return



        await self.client.create_collection(

            collection_name=
                self.config.collection_name,

            vector_size=
                self.config.vector_dimension,

            distance=
                self.config.distance,

        )



    ###########################################################################
    # Single Vector Index
    ###########################################################################


    async def index(
        self,
        point: VectorPoint,
    ) -> QdrantIndexResult:
        """
        Store single vector point.
        """

        start = time.perf_counter()



        payload = {

            "content":
                point.content,

            "document_id":
                point.document_id,

            "chunk_id":
                point.chunk_id,

            "metadata":
                point.metadata,

        }



        await self.client.upsert(

            collection_name=
                self.config.collection_name,

            points=[

                {

                    "id":
                        point.id,

                    "vector":
                        point.vector,

                    "payload":
                        payload,

                }

            ],

        )



        elapsed = (

            time.perf_counter()

            -

            start

        )



        return QdrantIndexResult(

            id=point.id,

            success=True,

            processing_time_ms=(

                elapsed * 1000

            ),

            indexed_at=datetime.utcnow(),

        )



    ###########################################################################
    # Bulk Index
    ###########################################################################


    async def bulk_index(
        self,
        points: list[VectorPoint],
    ) -> BulkIndexResult:
        """
        Bulk upsert vectors.
        """

        qdrant_points = []


        for point in points:

            qdrant_points.append(

                {

                    "id":
                        point.id,

                    "vector":
                        point.vector,

                    "payload":

                        {

                            "content":
                                point.content,

                            "document_id":
                                point.document_id,

                            "chunk_id":
                                point.chunk_id,

                            "metadata":
                                point.metadata,

                        }

                }

            )



        try:

            await self.client.upsert(

                collection_name=
                    self.config.collection_name,

                points=qdrant_points,

            )


            return BulkIndexResult(

                total=len(points),

                successful=len(points),

                failed=0,

            )


        except Exception as exc:

            logger.exception(
                "Qdrant bulk indexing failed"
            )


            return BulkIndexResult(

                total=len(points),

                successful=0,

                failed=len(points),

                errors=[

                    str(exc)

                ],

            )



    ###########################################################################
    # Delete
    ###########################################################################


    async def delete(
        self,
        ids: list[str],
    ):
        """
        Delete vectors from collection.
        """

        await self.client.delete(

            collection_name=
                self.config.collection_name,

            ids=ids,

        )