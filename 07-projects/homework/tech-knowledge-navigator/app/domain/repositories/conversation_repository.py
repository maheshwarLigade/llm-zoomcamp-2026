"""
Conversation Repository Interface

Defines persistence contract for Conversation entity.

Responsibilities:
- Store conversations
- Manage chat history
- Retrieve conversation context
- Support chat lifecycle
- Enable analytics

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from typing import Optional


from app.entities.conversation import (
    Conversation,
    ConversationStatus,
    ConversationMessage,
)



###############################################################################
# Conversation Repository Interface
###############################################################################


class ConversationRepository(
    ABC
):
    """
    Repository contract for Conversation aggregate.

    Conversation lifecycle:

        User

          |

          v

      Conversation

          |

          +---- Message

          |

          +---- Feedback


    """



    ###########################################################################
    # Create / Update
    ###########################################################################


    @abstractmethod
    async def save(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """
        Save conversation.

        Creates new conversation or updates
        existing conversation.
        """

        raise NotImplementedError



    @abstractmethod
    async def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
        """
        Update conversation state.
        """

        raise NotImplementedError



    ###########################################################################
    # Conversation Retrieval
    ###########################################################################


    @abstractmethod
    async def find_by_id(
        self,
        conversation_id: str,
    ) -> Optional[Conversation]:
        """
        Retrieve conversation by id.
        """

        raise NotImplementedError



    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Conversation]:
        """
        Retrieve conversations for user.

        Used for:

        - Chat history
        - User dashboard

        """

        raise NotImplementedError



    @abstractmethod
    async def find_active(
        self,
        user_id: str,
    ) -> list[Conversation]:
        """
        Retrieve active conversations.
        """

        raise NotImplementedError



    ###########################################################################
    # Message Operations
    ###########################################################################


    @abstractmethod
    async def add_message(
        self,
        conversation_id: str,
        message: ConversationMessage,
    ) -> ConversationMessage:
        """
        Add message to conversation.

        Used after:

        User question
        AI response

        """

        raise NotImplementedError



    @abstractmethod
    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 20,
    ) -> list[ConversationMessage]:
        """
        Retrieve conversation messages.

        Used for:

        - LLM context window
        - Follow-up questions

        """

        raise NotImplementedError



    @abstractmethod
    async def get_recent_context(
        self,
        conversation_id: str,
        message_limit: int = 10,
    ) -> list[ConversationMessage]:
        """
        Retrieve recent messages for LLM prompt.

        Example:

        Previous:
            User:
            Explain RAG

            Assistant:
            RAG combines retrieval and generation


        """

        raise NotImplementedError



    ###########################################################################
    # Search Operations
    ###########################################################################


    @abstractmethod
    async def search(
        self,
        query: str,
        user_id: str | None = None,
        limit: int = 10,
    ) -> list[Conversation]:
        """
        Search conversations.

        Possible implementations:

        - Full text search
        - Semantic search

        """

        raise NotImplementedError



    ###########################################################################
    # Lifecycle Management
    ###########################################################################


    @abstractmethod
    async def update_status(
        self,
        conversation_id: str,
        status: ConversationStatus,
    ) -> None:
        """
        Update conversation state.

        Example:

        ACTIVE
          |
          |
        COMPLETED
          |
          |
        ARCHIVED

        """

        raise NotImplementedError



    @abstractmethod
    async def close(
        self,
        conversation_id: str,
    ) -> None:
        """
        Close conversation.
        """

        raise NotImplementedError



    @abstractmethod
    async def archive(
        self,
        conversation_id: str,
    ) -> None:
        """
        Archive conversation.
        """

        raise NotImplementedError



    ###########################################################################
    # Context Management
    ###########################################################################


    @abstractmethod
    async def update_summary(
        self,
        conversation_id: str,
        summary: str,
    ) -> None:
        """
        Update conversation summary.

        Used for:

        - Long conversations
        - Token optimization

        """

        raise NotImplementedError



    @abstractmethod
    async def get_summary(
        self,
        conversation_id: str,
    ) -> Optional[str]:
        """
        Retrieve conversation summary.
        """

        raise NotImplementedError



    ###########################################################################
    # Delete Operations
    ###########################################################################


    @abstractmethod
    async def delete(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Delete conversation.

        Returns:

        True:
            deleted

        False:
            not found

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
        Total conversation count.
        """

        raise NotImplementedError



    @abstractmethod
    async def count_by_user(
        self,
        user_id: str,
    ) -> int:
        """
        Count conversations for user.
        """

        raise NotImplementedError



    @abstractmethod
    async def count_messages(
        self,
        conversation_id: str,
    ) -> int:
        """
        Count messages inside conversation.
        """

        raise NotImplementedError



###############################################################################
# Conversation Search Criteria
###############################################################################


class ConversationSearchCriteria:
    """
    Dynamic search criteria.

    Example:

    {
        "user_id": "user-1",
        "status": "active"
    }

    """



    def __init__(
        self,
        user_id: str | None = None,
        status: ConversationStatus | None = None,
        keyword: str | None = None,
        limit: int = 10,
    ):

        self.user_id = user_id

        self.status = status

        self.keyword = keyword

        self.limit = limit



###############################################################################
# Conversation Context Criteria
###############################################################################


class ConversationContextCriteria:
    """
    Defines how much history should
    be loaded for LLM.

    Used by chat service.

    """



    def __init__(
        self,
        max_messages: int = 10,
        max_tokens: int = 4000,
    ):

        self.max_messages = max_messages

        self.max_tokens = max_tokens