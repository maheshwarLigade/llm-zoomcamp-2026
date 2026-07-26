"""
Feedback API Schemas

Pydantic models used for collecting,
storing, and analyzing user feedback.

Author
------
Tech Knowledge Navigator
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


###############################################################################
# Feedback Enums
###############################################################################


class FeedbackRating(str, Enum):
    """
    Overall feedback rating.
    """

    POSITIVE = "positive"

    NEGATIVE = "negative"

    NEUTRAL = "neutral"



class FeedbackCategory(str, Enum):
    """
    Feedback classification.
    """

    ANSWER_QUALITY = "answer_quality"

    RETRIEVAL_QUALITY = "retrieval_quality"

    HALLUCINATION = "hallucination"

    MISSING_INFORMATION = "missing_information"

    WRONG_CONTEXT = "wrong_context"

    PERFORMANCE = "performance"

    OTHER = "other"



###############################################################################
# Create Feedback
###############################################################################


class FeedbackCreateRequest(BaseModel):
    """
    Request payload for submitting feedback.
    """

    conversation_id: UUID

    message_id: UUID

    rating: FeedbackRating

    score: int = Field(
        default=5,
        ge=1,
        le=5,
        description="Rating from 1 to 5",
    )

    category: FeedbackCategory | None = None

    comment: str | None = Field(
        default=None,
        max_length=2000,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )



###############################################################################
# Update Feedback
###############################################################################


class FeedbackUpdateRequest(BaseModel):
    """
    Update existing feedback.
    """

    rating: FeedbackRating | None = None

    score: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    category: FeedbackCategory | None = None

    comment: str | None = Field(
        default=None,
        max_length=2000,
    )



###############################################################################
# Feedback Response
###############################################################################


class FeedbackResponse(BaseModel):
    """
    Feedback response.
    """

    feedback_id: UUID = Field(
        default_factory=uuid4,
    )

    conversation_id: UUID

    message_id: UUID

    rating: FeedbackRating

    score: int

    category: FeedbackCategory | None = None

    comment: str | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    updated_at: datetime | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )



###############################################################################
# Feedback Search
###############################################################################


class FeedbackFilterRequest(BaseModel):
    """
    Filtering feedback records.
    """

    rating: FeedbackRating | None = None

    category: FeedbackCategory | None = None

    start_date: datetime | None = None

    end_date: datetime | None = None

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )



###############################################################################
# Feedback Analytics
###############################################################################


class FeedbackStatistics(BaseModel):
    """
    Aggregated feedback metrics.

    Used by monitoring dashboard.
    """

    total_feedback: int

    positive_count: int

    negative_count: int

    neutral_count: int

    average_score: float

    positive_percentage: float

    negative_percentage: float



###############################################################################
# Feedback Dashboard
###############################################################################


class FeedbackTrendPoint(BaseModel):
    """
    Time-series feedback data.
    """

    date: str

    total: int

    positive: int

    negative: int

    average_score: float



class FeedbackAnalyticsResponse(BaseModel):
    """
    Feedback dashboard response.
    """

    statistics: FeedbackStatistics

    trends: list[FeedbackTrendPoint]

    top_issues: list[str]

    category_distribution: dict[str, int]



###############################################################################
# Feedback List
###############################################################################


class FeedbackListResponse(BaseModel):
    """
    Paginated feedback response.
    """

    items: list[FeedbackResponse]

    total: int

    page: int

    page_size: int



###############################################################################
# API Wrapper
###############################################################################


class FeedbackApiResponse(BaseModel):
    """
    Standard API response wrapper.
    """

    success: bool = True

    data: FeedbackResponse

    request_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )

    model_config = ConfigDict(
        from_attributes=True,
    )