"""
Conversation Domain Entity

Represents a user conversation session
inside the RAG application.

Responsibilities:
- Maintain chat history
- Track messages
- Preserve context
- Store conversation metadata
- Support multi-turn conversations

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
# Conversation Status
###############################################################################


class ConversationStatus(str, Enum):
    """
    Conversation lifecycle states.
    """

    ACTIVE = "active"

    COMPLETED = "completed"

    ARCHIVED = "archived"



###############################################################################
# Message Role
###############################################################################


class MessageRole(str, Enum):
    """
    Chat message roles.
    """

    USER = "user"

    ASSISTANT = "assistant"

    SYSTEM = "system"



###############################################################################
# Conversation Message
###############################################################################


@dataclass
class ConversationMessage:
    """
    Individual message inside conversation.
    """


    id: str


    role: MessageRole


    content: str



    ###########################################################################
    # RAG Metadata
    ###########################################################################

    retrieved_chunks: list[str] = field(
        default_factory=list
    )


    sources: list[str] = field(
        default_factory=list
    )


    model: str | None = None


    provider: str | None = None



    ###########################################################################
    # Token Tracking
    ###########################################################################

    prompt_tokens: int = 0


    completion_tokens: int = 0



    ###########################################################################
    # Performance
    ###########################################################################

    latency_ms: float = 0.0



    ###########################################################################
    # Audit
    ###########################################################################

    created_at: datetime = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        )
    )



    def add_source(
        self,
        source: str,
    ):
        """
        Add answer source reference.
        """

        if source not in self.sources:

            self.sources.append(
                source
            )



    def add_chunk(
        self,
        chunk_id: str,
    ):
        """
        Add retrieved chunk reference.
        """

        if chunk_id not in self.retrieved_chunks:

            self.retrieved_chunks.append(
                chunk_id
            )



    def token_usage(self) -> int:
        """
        Total token usage.
        """

        return (
            self.prompt_tokens
            +
            self.completion_tokens
        )



###############################################################################
# Conversation Entity
###############################################################################


@dataclass
class Conversation:
    """
    Conversation aggregate root.

    Represents complete user interaction.

    Example:

        Conversation

            |
            +-- User Question

            |
            +-- AI Answer

            |
            +-- User Follow-up

    """


    ###########################################################################
    # Identity
    ###########################################################################

    id: str


    user_id: str | None = None



    ###########################################################################
    # Conversation Information
    ###########################################################################

    title: str | None = None


    status: ConversationStatus = (
        ConversationStatus.ACTIVE
    )



    messages: list[ConversationMessage] = field(
        default_factory=list
    )



    ###########################################################################
    # RAG Context
    ###########################################################################

    summary: str | None = None


    context_window_tokens: int = 0



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


    def add_message(
        self,
        message: ConversationMessage,
    ):
        """
        Add message to conversation.
        """

        self.messages.append(
            message
        )


        self.updated_at = datetime.now(
            timezone.utc
        )



    def add_user_message(
        self,
        message_id: str,
        content: str,
    ):
        """
        Add user message.
        """

        self.add_message(

            ConversationMessage(

                id=message_id,

                role=MessageRole.USER,

                content=content,

            )

        )



    def add_assistant_message(
        self,
        message_id: str,
        content: str,
        model: str | None = None,
        latency_ms: float = 0,
    ):
        """
        Add assistant response.
        """

        self.add_message(

            ConversationMessage(

                id=message_id,

                role=MessageRole.ASSISTANT,

                content=content,

                model=model,

                latency_ms=latency_ms,

            )

        )



    def get_history(
        self,
        limit: int | None = None,
    ) -> list[ConversationMessage]:
        """
        Return conversation history.

        Used by:
        - Query rewriting
        - Context generation
        """

        if limit is None:

            return self.messages


        return self.messages[-limit:]



    def get_prompt_history(
        self,
        limit: int = 10,
    ) -> list[dict[str, str]]:
        """
        Convert messages into LLM format.
        """

        history = []


        for message in self.get_history(
            limit
        ):

            history.append(

                {
                    "role":
                        message.role.value,

                    "content":
                        message.content,
                }

            )


        return history



    def calculate_token_usage(
        self,
    ) -> int:
        """
        Calculate total conversation tokens.
        """

        return sum(

            message.token_usage()

            for message in self.messages

        )



    def close(
        self,
    ):
        """
        Complete conversation.
        """

        self.status = (
            ConversationStatus.COMPLETED
        )



        self.updated_at = datetime.now(
            timezone.utc
        )



    def archive(
        self,
    ):
        """
        Archive conversation.
        """

        self.status = (
            ConversationStatus.ARCHIVED
        )



    def update_metadata(
        self,
        values: dict[str, Any],
    ):
        """
        Update conversation metadata.
        """

        self.metadata.update(
            values
        )



    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize conversation.
        """

        return {

            "id": self.id,

            "user_id": self.user_id,

            "title": self.title,

            "status": self.status.value,

            "message_count":
                len(self.messages),

            "token_usage":
                self.calculate_token_usage(),

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat(),

        }