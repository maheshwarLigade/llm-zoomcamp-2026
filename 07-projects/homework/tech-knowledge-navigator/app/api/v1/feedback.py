"""
Feedback API

Collects user feedback for RAG responses.

Responsibilities
----------------
* Submit user feedback
* Retrieve feedback
* Update feedback
* Delete feedback
* Feedback analytics

Business logic is delegated to FeedbackService.
"""

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from pydantic import BaseModel
from pydantic import Field

from app.api.deps import get_feedback_service
from app.services.feedback_service import FeedbackService

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)

###############################################################################
# Enums
###############################################################################


class FeedbackRating(str, Enum):
    """
    User rating.
    """

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


###############################################################################
# Request Models
###############################################################################


class FeedbackRequest(BaseModel):
    """
    Feedback submission request.
    """

    session_id: UUID

    response_id: UUID

    rating: FeedbackRating

    comment: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    expected_answer: Optional[str] = Field(
        default=None,
        description="Optional expected answer supplied by the user.",
    )


class FeedbackUpdateRequest(BaseModel):
    """
    Update an existing feedback entry.
    """

    rating: Optional[FeedbackRating] = None

    comment: Optional[str] = None

    expected_answer: Optional[str] = None


###############################################################################
# Response Models
###############################################################################


class FeedbackResponse(BaseModel):
    """
    Feedback response.
    """

    feedback_id: UUID

    session_id: UUID

    response_id: UUID

    rating: FeedbackRating

    comment: Optional[str]

    expected_answer: Optional[str]

    created_at: datetime

    updated_at: datetime


class FeedbackListResponse(BaseModel):
    """
    Paginated feedback response.
    """

    total: int

    page: int

    page_size: int

    feedback: List[FeedbackResponse]


class FeedbackStatistics(BaseModel):
    """
    Feedback analytics.
    """

    total_feedback: int

    positive_feedback: int

    negative_feedback: int

    neutral_feedback: int

    positive_percentage: float

    average_rating: float


###############################################################################
# Submit Feedback
###############################################################################


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Feedback",
)
async def submit_feedback(
    request: FeedbackRequest,
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Submit user feedback for a generated answer.
    """

    return await service.submit_feedback(request)


###############################################################################
# List Feedback
###############################################################################


@router.get(
    "",
    response_model=FeedbackListResponse,
    summary="List Feedback",
)
async def list_feedback(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Returns paginated feedback.
    """

    return await service.list_feedback(
        page=page,
        page_size=page_size,
    )


###############################################################################
# Get Feedback
###############################################################################


@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    summary="Get Feedback",
)
async def get_feedback(
    feedback_id: UUID,
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Retrieve feedback by identifier.
    """

    feedback = await service.get_feedback(feedback_id)

    if feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found.",
        )

    return feedback


###############################################################################
# Update Feedback
###############################################################################


@router.put(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    summary="Update Feedback",
)
async def update_feedback(
    feedback_id: UUID,
    request: FeedbackUpdateRequest,
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Update feedback.
    """

    feedback = await service.update_feedback(
        feedback_id=feedback_id,
        request=request,
    )

    if feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found.",
        )

    return feedback


###############################################################################
# Delete Feedback
###############################################################################


@router.delete(
    "/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Feedback",
)
async def delete_feedback(
    feedback_id: UUID,
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Delete feedback.
    """

    deleted = await service.delete_feedback(feedback_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found.",
        )


###############################################################################
# Statistics
###############################################################################


@router.get(
    "/statistics/summary",
    response_model=FeedbackStatistics,
    summary="Feedback Statistics",
)
async def feedback_statistics(
    service: FeedbackService = Depends(get_feedback_service),
):
    """
    Returns aggregated feedback statistics.
    """

    return await service.get_statistics()