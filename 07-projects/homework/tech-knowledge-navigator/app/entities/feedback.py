"""
Feedback Domain Entity

Represents user feedback collected
from RAG responses.

Responsibilities:
- Capture user satisfaction
- Evaluate answer quality
- Link feedback with responses
- Support RAG improvement loops
- Build evaluation datasets

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from dataclasses import dataclass, field

from datetime import datetime, timezone

from enum import Enum

from typing import Any



###############################################################################
# Feedback Type
###############################################################################


class FeedbackType(str, Enum):
    """
    Type of feedback provided by user.
    """

    LIKE = "like"

    DISLIKE = "dislike"

    RATING = "rating"

    COMMENT = "comment"



###############################################################################
# Feedback Category
###############################################################################


class FeedbackCategory(str, Enum):
    """
    Feedback classification.
    """

    ACCURATE = "accurate"

    INCORRECT = "incorrect"

    INCOMPLETE = "incomplete"

    IRRELEVANT = "irrelevant"

    HALLUCINATION = "hallucination"

    RETRIEVAL_ISSUE = "retrieval_issue"

    OTHER = "other"



###############################################################################
# Feedback Status
###############################################################################


class FeedbackStatus(str, Enum):
    """
    Feedback processing lifecycle.
    """

    SUBMITTED = "submitted"

    REVIEWED = "reviewed"

    ACTIONED = "actioned"

    DISMISSED = "dismissed"



###############################################################################
# Feedback Entity
###############################################################################


@dataclass
class Feedback:
    """
    Feedback aggregate entity.

    Represents evaluation of an AI response.

    Relationship:

        Conversation

             |

             |

        Message

             |

             |

        Feedback


    """


    ###########################################################################
    # Identity
    ###########################################################################

    id: str



    ###########################################################################
    # References
    ###########################################################################

    conversation_id: str


    message_id: str



    user_id: str | None = None



    ###########################################################################
    # Feedback Information
    ###########################################################################

    feedback_type: FeedbackType = (
        FeedbackType.COMMENT
    )


    category: FeedbackCategory = (
        FeedbackCategory.OTHER
    )



    rating: int | None = None



    comment: str | None = None



    ###########################################################################
    # RAG Evaluation Context
    ###########################################################################

    question: str | None = None


    answer: str | None = None



    retrieved_chunk_ids: list[str] = field(
        default_factory=list
    )



    sources: list[str] = field(
        default_factory=list
    )



    ###########################################################################
    # Model Information
    ###########################################################################

    model_name: str | None = None


    provider: str | None = None



    ###########################################################################
    # Processing
    ###########################################################################

    status: FeedbackStatus = (
        FeedbackStatus.SUBMITTED
    )



    ###########################################################################
    # Metadata
    ###########################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    ###########################################################################
    # Audit
    ###########################################################################

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        )
    )


    updated_at: datetime = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        )
    )



    ###########################################################################
    # Business Methods
    ###########################################################################


    def is_positive(
        self,
    ) -> bool:
        """
        Check whether feedback is positive.
        """

        return (

            self.feedback_type
            ==
            FeedbackType.LIKE

        )



    def is_negative(
        self,
    ) -> bool:
        """
        Check whether feedback indicates
        poor answer quality.
        """

        return (

            self.feedback_type
            ==
            FeedbackType.DISLIKE

        )



    def set_rating(
        self,
        rating: int,
    ):
        """
        Set numerical rating.

        Expected range:
        1-5
        """

        if rating < 1 or rating > 5:

            raise ValueError(
                "Rating must be between 1 and 5"
            )


        self.rating = rating

        self.feedback_type = (
            FeedbackType.RATING
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def add_comment(
        self,
        comment: str,
    ):
        """
        Add user comment.
        """

        self.comment = comment

        self.feedback_type = (
            FeedbackType.COMMENT
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def classify(
        self,
        category: FeedbackCategory,
    ):
        """
        Assign feedback category.
        """

        self.category = category

        self.updated_at = datetime.now(
            timezone.utc
        )



    def add_source(
        self,
        source: str,
    ):
        """
        Add answer source.
        """

        if source not in self.sources:

            self.sources.append(
                source
            )



    def add_chunk_reference(
        self,
        chunk_id: str,
    ):
        """
        Track retrieved chunks.

        Useful for:
        - retrieval debugging
        - bad document detection
        """

        if chunk_id not in self.retrieved_chunk_ids:

            self.retrieved_chunk_ids.append(
                chunk_id
            )



    def mark_reviewed(
        self,
    ):
        """
        Mark feedback reviewed.
        """

        self.status = (
            FeedbackStatus.REVIEWED
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def mark_actioned(
        self,
    ):
        """
        Mark improvement action completed.
        """

        self.status = (
            FeedbackStatus.ACTIONED
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    def dismiss(
        self,
    ):
        """
        Dismiss feedback.
        """

        self.status = (
            FeedbackStatus.DISMISSED
        )

        self.updated_at = datetime.now(
            timezone.utc
        )



    ###########################################################################
    # Evaluation Dataset Support
    ###########################################################################


    def to_evaluation_record(
        self,
    ) -> dict[str, Any]:
        """
        Convert feedback into evaluation dataset format.

        Useful for:

        - LLM fine tuning
        - RAG evaluation
        - Benchmark datasets

        """

        return {

            "question":
                self.question,

            "answer":
                self.answer,

            "rating":
                self.rating,

            "category":
                self.category.value,

            "feedback":
                self.comment,

            "sources":
                self.sources,

            "chunks":
                self.retrieved_chunk_ids,

        }



    ###########################################################################
    # Serialization
    ###########################################################################


    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize feedback entity.
        """

        return {

            "id":
                self.id,

            "conversation_id":
                self.conversation_id,

            "message_id":
                self.message_id,

            "type":
                self.feedback_type.value,

            "category":
                self.category.value,

            "rating":
                self.rating,

            "status":
                self.status.value,

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat(),

        }