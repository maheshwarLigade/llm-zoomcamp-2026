"""
Document Management API

Provides APIs for managing indexed documents in the RAG
knowledge base.

Responsibilities
----------------
* List documents
* Retrieve document
* Search documents
* Upload document
* Delete document
* Re-index document
* Retrieve document chunks
* Document metadata

Business logic is delegated to DocumentService.

Author
------
Tech Knowledge Navigator
"""

from typing import List
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import Query
from fastapi import UploadFile
from fastapi import status

from pydantic import BaseModel
from pydantic import Field

from app.api.deps import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

###############################################################################
# Models
###############################################################################


class DocumentMetadata(BaseModel):
    document_id: UUID
    title: str
    source: str
    document_type: str
    author: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[int] = None
    chunks: int
    indexed_at: str


class DocumentSummary(BaseModel):
    document_id: UUID
    title: str
    source: str


class DocumentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    documents: List[DocumentSummary]


class ChunkResponse(BaseModel):
    chunk_id: str
    score: float
    text: str


class UploadResponse(BaseModel):
    document_id: UUID
    filename: str
    status: str
    message: str


###############################################################################
# Endpoints
###############################################################################


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List Documents",
)
async def list_documents(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: DocumentService = Depends(get_document_service),
):
    """
    Returns paginated indexed documents.
    """

    return await service.list_documents(
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentMetadata,
    summary="Get Document",
)
async def get_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """
    Retrieve document metadata.
    """

    document = await service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document


@router.get(
    "/{document_id}/chunks",
    response_model=List[ChunkResponse],
    summary="Document Chunks",
)
async def get_chunks(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """
    Returns all chunks for a document.
    """

    return await service.get_document_chunks(document_id)


@router.get(
    "/search",
    response_model=List[DocumentSummary],
    summary="Search Documents",
)
async def search_documents(
    q: str = Query(..., min_length=2),
    top_k: int = Query(default=10, ge=1, le=50),
    service: DocumentService = Depends(get_document_service),
):
    """
    Performs metadata search.
    """

    return await service.search_documents(
        query=q,
        top_k=top_k,
    )


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document",
)
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """
    Upload and ingest a new document.
    """

    return await service.upload_document(file)


@router.post(
    "/{document_id}/reindex",
    summary="Re-index Document",
)
async def reindex_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """
    Rebuild embeddings and search indexes.
    """

    await service.reindex_document(document_id)

    return {
        "status": "success",
        "message": "Document re-indexed successfully."
    }


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
)
async def delete_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """
    Deletes a document and all associated chunks.
    """

    await service.delete_document(document_id)