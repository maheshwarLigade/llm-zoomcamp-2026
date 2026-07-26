"""
OpenSearch Indexing Service

Provides indexing capabilities for RAG applications.

Features:

- Create vector indexes
- Index document chunks
- Bulk indexing
- Delete documents
- Update documents
- Hybrid search preparation


OpenSearch stores:

- Chunk text
- Document metadata
- Embedding vectors


Pipeline:

Chunk
 |
 v
Embedding
 |
 v
OpenSearchIndexer
 |
 v
OpenSearch


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


class OpenSearchClient(Protocol):
    """
    OpenSearch client abstraction.

    Implementation:

    - opensearch-py client
    """

    async def create_index(
        self,
        index_name: str,
        mapping: dict,
    ):
        ...


    async def index(
        self,
        index_name: str,
        document_id: str,
        body: dict,
    ):
        ...


    async def bulk(
        self,
        operations: list[dict],
    ):
        ...


    async def delete(
        self,
        index_name: str,
        document_id: str,
    ):
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class VectorDocument:
    """
    Search document stored in OpenSearch.
    """

    id: str

    content: str

    embedding: list[float]

    document_id: str

    chunk_id: str

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class IndexingResult:
    """
    Indexing operation response.
    """

    document_id: str

    indexed: bool

    processing_time_ms: float

    indexed_at: datetime



@dataclass
class BulkIndexResult:
    """
    Bulk indexing response.
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
class OpenSearchConfig:
    """
    OpenSearch configuration.
    """

    index_name: str = "rag_documents"

    vector_dimension: int = 1536

    similarity: str = "cosine"



###############################################################################
# OpenSearch Indexer
###############################################################################


class OpenSearchIndexer:
    """
    Indexes RAG chunks into OpenSearch.

    """



    def __init__(
        self,
        client: OpenSearchClient,
        config: OpenSearchConfig | None = None,
    ):

        self.client = client


        self.config = (

            config

            or OpenSearchConfig()

        )



    ###########################################################################
    # Index Creation
    ###########################################################################


    async def create_index(
        self,
    ):
        """
        Create OpenSearch vector index.
        """

        mapping = {

            "settings": {

                "index": {

                    "knn": True

                }

            },

            "mappings": {

                "properties": {

                    "content": {

                        "type": "text"

                    },


                    "document_id": {

                        "type": "keyword"

                    },


                    "chunk_id": {

                        "type": "keyword"

                    },


                    "embedding": {

                        "type": "knn_vector",

                        "dimension":
                            self.config.vector_dimension,

                        "method": {

                            "name":
                                "hnsw",

                            "space_type":
                                self.config.similarity,

                        }

                    },


                    "metadata": {

                        "type": "object"

                    }

                }

            }

        }


        await self.client.create_index(

            self.config.index_name,

            mapping,

        )



    ###########################################################################
    # Single Index
    ###########################################################################


    async def index(
        self,
        document: VectorDocument,
    ) -> IndexingResult:
        """
        Index one document chunk.
        """

        start = time.perf_counter()



        body = {

            "content":
                document.content,

            "document_id":
                document.document_id,

            "chunk_id":
                document.chunk_id,

            "embedding":
                document.embedding,

            "metadata":
                document.metadata,

        }



        await self.client.index(

            index_name=self.config.index_name,

            document_id=document.id,

            body=body,

        )



        elapsed = (

            time.perf_counter()

            -

            start

        )



        return IndexingResult(

            document_id=document.id,

            indexed=True,

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
        documents: list[VectorDocument],
    ) -> BulkIndexResult:
        """
        Bulk index documents.
        """

        operations = []


        for document in documents:

            operations.append(

                {

                    "_index":
                        self.config.index_name,

                    "_id":
                        document.id,

                    "_source":

                        {

                            "content":
                                document.content,

                            "document_id":
                                document.document_id,

                            "chunk_id":
                                document.chunk_id,

                            "embedding":
                                document.embedding,

                            "metadata":
                                document.metadata,

                        }

                }

            )



        response = await self.client.bulk(

            operations

        )



        return BulkIndexResult(

            total=len(
                documents
            ),

            successful=response.get(
                "successful",
                0,
            ),

            failed=response.get(
                "failed",
                0,
            ),

            errors=response.get(
                "errors",
                [],
            ),

        )



    ###########################################################################
    # Delete
    ###########################################################################


    async def delete(
        self,
        document_id: str,
    ):
        """
        Delete indexed document.
        """

        await self.client.delete(

            index_name=self.config.index_name,

            document_id=document_id,

        )