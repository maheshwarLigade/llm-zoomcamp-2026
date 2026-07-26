"""
Document Ingestion Service

Coordinates document ingestion workflow
for Retrieval Augmented Generation.

Responsibilities:
- Create document
- Process content
- Create chunks
- Persist chunks
- Trigger embedding workflow
- Manage ingestion lifecycle

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from dataclasses import dataclass


from typing import Protocol


from app.entities.document import (
    Document,
    DocumentStatus,
    DocumentType,
)


from app.entities.chunk import (
    Chunk,
    ChunkType,
)


from app.domain.repositories.document_repository import (
    DocumentRepository,
)


from app.domain.repositories.chunk_repository import (
    ChunkRepository,
)



logger = logging.getLogger(__name__)



###############################################################################
# External Service Contracts
###############################################################################


class DocumentExtractor(Protocol):
    """
    Extracts text from source documents.
    """

    async def extract(
        self,
        location: str,
        document_type: DocumentType,
    ) -> str:
        ...



class TextChunker(Protocol):
    """
    Splits document text into chunks.
    """

    async def split(
        self,
        content: str,
    ) -> list[str]:
        ...



###############################################################################
# Request Model
###############################################################################


@dataclass
class IngestionRequest:
    """
    Input request for document ingestion.
    """

    document_id: str

    title: str

    location: str

    document_type: DocumentType

    owner_id: str | None = None

    metadata: dict | None = None



###############################################################################
# Ingestion Result
###############################################################################


@dataclass
class IngestionResult:
    """
    Result returned after ingestion.
    """

    document_id: str

    chunks_created: int

    status: DocumentStatus

    message: str



###############################################################################
# Ingestion Service
###############################################################################


class IngestionService:
    """
    Application domain service responsible
    for document ingestion.

    """



    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
        extractor: DocumentExtractor,
        chunker: TextChunker,
    ):

        self.document_repository = (
            document_repository
        )

        self.chunk_repository = (
            chunk_repository
        )

        self.extractor = extractor

        self.chunker = chunker



    ###########################################################################
    # Public API
    ###########################################################################


    async def ingest(
        self,
        request: IngestionRequest,
    ) -> IngestionResult:
        """
        Execute complete ingestion workflow.

        Steps:

        1. Create document
        2. Extract content
        3. Split into chunks
        4. Store chunks
        5. Mark document indexed

        """

        document = self._create_document(
            request
        )


        await self.document_repository.save(
            document
        )


        try:

            document.start_processing()


            await self.document_repository.update(
                document
            )


            content = await (
                self.extractor.extract(
                    request.location,
                    request.document_type,
                )
            )


            chunks = await (
                self._create_chunks(
                    document,
                    content,
                )
            )


            await self.chunk_repository.save_many(
                chunks
            )


            for chunk in chunks:

                document.add_chunk(
                    chunk.id
                )


            document.mark_indexed()


            await self.document_repository.update(
                document
            )


            logger.info(
                "Document ingestion completed: %s",
                document.id,
            )


            return IngestionResult(

                document_id=document.id,

                chunks_created=len(chunks),

                status=document.status,

                message="Document indexed successfully",

            )


        except Exception as exc:

            logger.exception(
                "Document ingestion failed"
            )


            document.mark_failed(
                str(exc)
            )


            await self.document_repository.update(
                document
            )


            return IngestionResult(

                document_id=document.id,

                chunks_created=0,

                status=document.status,

                message=str(exc),

            )



    ###########################################################################
    # Document Creation
    ###########################################################################


    def _create_document(
        self,
        request: IngestionRequest,
    ) -> Document:
        """
        Create document aggregate.
        """

        document = Document(

            id=request.document_id,

            title=request.title,

            document_type=request.document_type,

            owner_id=request.owner_id,

        )


        if request.metadata:

            document.update_metadata(
                request.metadata
            )


        return document



    ###########################################################################
    # Chunk Creation
    ###########################################################################


    async def _create_chunks(
        self,
        document: Document,
        content: str,
    ) -> list[Chunk]:
        """
        Convert extracted text into chunks.
        """

        texts = await (
            self.chunker.split(
                content
            )
        )


        chunks: list[Chunk] = []


        for index, text in enumerate(texts):

            chunk = Chunk(

                id=f"{document.id}_chunk_{index}",

                document_id=document.id,

                content=text,

                chunk_index=index,

                chunk_type=ChunkType.TEXT,

                character_count=len(text),

            )


            chunks.append(
                chunk
            )


        return chunks



    ###########################################################################
    # Utility Methods
    ###########################################################################


    async def retry_failed_ingestion(
        self,
        document_id: str,
    ) -> None:
        """
        Retry failed document processing.

        Actual retry scheduling should be
        handled by worker/queue layer.
        """

        document = await (
            self.document_repository.find_by_id(
                document_id
            )
        )


        if not document:

            raise ValueError(
                "Document not found"
            )


        document.status = (
            DocumentStatus.CREATED
        )


        await self.document_repository.update(
            document
        )