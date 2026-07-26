"""
Feedback Repository Interface

Defines persistence contract for Feedback entity.

Responsibilities:
- Store user feedback
- Retrieve feedback records
- Support evaluation workflows
- Generate RAG quality insights
- Build improvement datasets

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from typing import Optional


from app.entities.feedback import (
    Feedback,
    FeedbackCategory,
    FeedbackStatus,
)



###############################################################################
# Feedback Repository Interface
###############################################################################


class FeedbackRepository(
    ABC
):
    """
    Repository contract for Feedback aggregate.

    Feedback lifecycle:

        User

          |
          v

       AI Answer

          |
          v

       Feedback

          |
          +----------------+
          |                |
          v                v

    Analytics        Evaluation Dataset

    """



    ###########################################################################
    # Create / Update
    ###########################################################################


    @abstractmethod
    async def save(
        self,
        feedback: Feedback,
    ) -> Feedback:
        """
        Save feedback.

        Creates new feedback record.
        """

        raise NotImplementedError



    @abstractmethod
    async def update(
        self,
        feedback: Feedback,
    ) -> Feedback:
        """
        Update feedback record.
        """

        raise NotImplementedError



    ###########################################################################
    # Retrieval Operations
    ###########################################################################


    @abstractmethod
    async def find_by_id(
        self,
        feedback_id: str,
    ) -> Optional[Feedback]:
        """
        Find feedback by id.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_message_id(
        self,
        message_id: str,
    ) -> Optional[Feedback]:
        """
        Retrieve feedback for AI message.

        One AI response can have one
        primary user feedback record.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_conversation_id(
        self,
        conversation_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Feedback]:
        """
        Retrieve feedback history
        for conversation.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: str,
        limit: int = 50,
    ) -> list[Feedback]:
        """
        Retrieve feedback submitted by user.
        """

        raise NotImplementedError



    ###########################################################################
    # Classification Queries
    ###########################################################################


    @abstractmethod
    async def find_by_category(
        self,
        category: FeedbackCategory,
        limit: int = 100,
    ) -> list[Feedback]:
        """
        Find feedback by category.

        Examples:

        - hallucination
        - incorrect
        - retrieval_issue

        """

        raise NotImplementedError



    @abstractmethod
    async def find_negative_feedback(
        self,
        limit: int = 100,
    ) -> list[Feedback]:
        """
        Retrieve poor quality responses.

        Used for:

        - Error analysis
        - Prompt improvement
        - Retrieval tuning

        """

        raise NotImplementedError



    @abstractmethod
    async def find_unreviewed(
        self,
        limit: int = 100,
    ) -> list[Feedback]:
        """
        Retrieve feedback waiting
        for human review.
        """

        raise NotImplementedError



    ###########################################################################
    # Evaluation Dataset Support
    ###########################################################################


    @abstractmethod
    async def get_evaluation_dataset(
        self,
        limit: int = 1000,
    ) -> list[dict]:
        """
        Convert feedback records into
        evaluation dataset format.

        Example:

        {
            question,
            answer,
            rating,
            category,
            sources
        }

        """

        raise NotImplementedError



    @abstractmethod
    async def export_training_examples(
        self,
        limit: int = 1000,
    ) -> list[dict]:
        """
        Export examples for:

        - Prompt evaluation
        - Fine tuning
        - RAG benchmark

        """

        raise NotImplementedError



    ###########################################################################
    # Status Management
    ###########################################################################


    @abstractmethod
    async def update_status(
        self,
        feedback_id: str,
        status: FeedbackStatus,
    ) -> None:
        """
        Update feedback workflow status.

        Example:

        SUBMITTED
            |
            v
        REVIEWED
            |
            v
        ACTIONED

        """

        raise NotImplementedError



    ###########################################################################
    # Analytics
    ###########################################################################


    @abstractmethod
    async def count(
        self,
    ) -> int:
        """
        Total feedback count.
        """

        raise NotImplementedError



    @abstractmethod
    async def count_by_category(
        self,
        category: FeedbackCategory,
    ) -> int:
        """
        Count feedback by category.
        """

        raise NotImplementedError



    @abstractmethod
    async def average_rating(
        self,
    ) -> float:
        """
        Calculate average user rating.
        """

        raise NotImplementedError



    @abstractmethod
    async def satisfaction_score(
        self,
    ) -> float:
        """
        Calculate satisfaction percentage.

        Example:

        Positive feedback /
        Total feedback

        """

        raise NotImplementedError



    ###########################################################################
    # Retrieval Quality Analysis
    ###########################################################################


    @abstractmethod
    async def find_retrieval_failures(
        self,
        limit: int = 100,
    ) -> list[Feedback]:
        """
        Find feedback indicating
        retrieval problems.

        Example:

        Category:

            RETRIEVAL_ISSUE

        """

        raise NotImplementedError



    @abstractmethod
    async def find_hallucinations(
        self,
        limit: int = 100,
    ) -> list[Feedback]:
        """
        Find hallucination cases.

        Used for:

        - Prompt improvement
        - Retrieval tuning
        - Model evaluation

        """

        raise NotImplementedError



    ###########################################################################
    # Delete Operations
    ###########################################################################


    @abstractmethod
    async def delete(
        self,
        feedback_id: str,
    ) -> bool:
        """
        Delete feedback record.
        """

        raise NotImplementedError



###############################################################################
# Feedback Search Criteria
###############################################################################


class FeedbackSearchCriteria:
    """
    Dynamic feedback search criteria.

    Example:

    {
        category:
            hallucination,

        status:
            submitted
    }

    """



    def __init__(
        self,
        category: FeedbackCategory | None = None,
        status: FeedbackStatus | None = None,
        user_id: str | None = None,
        rating: int | None = None,
        limit: int = 50,
    ):

        self.category = category

        self.status = status

        self.user_id = user_id

        self.rating = rating

        self.limit = limit



###############################################################################
# Evaluation Filter
###############################################################################


class EvaluationCriteria:
    """
    Criteria for building RAG evaluation sets.
    """



    def __init__(
        self,
        minimum_rating: int | None = None,
        category: FeedbackCategory | None = None,
        include_comments: bool = True,
    ):

        self.minimum_rating = minimum_rating

        self.category = category

        self.include_comments = include_comments