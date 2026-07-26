"""
Distributed Tracing

Provides tracing abstraction for the RAG platform.

Tracks:

- Request lifecycle
- Component execution
- Latency
- Errors
- Metadata propagation


Designed for integration with:

- OpenTelemetry
- Jaeger
- Grafana Tempo
- Zipkin


Example trace:

chat_request
 |
 +-- retrieval
 |      |
 |      +-- embedding
 |      |
 |      +-- vector_search
 |
 +-- llm_generation


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import uuid


import time


from contextlib import contextmanager


from dataclasses import dataclass, field


from datetime import datetime, timezone


from typing import Any, Generator



logger = logging.getLogger(__name__)



###############################################################################
# Models
###############################################################################


@dataclass
class TraceContext:
    """
    Trace context propagated across services.
    """

    trace_id: str

    span_id: str

    parent_span_id: str | None = None

    service: str | None = None

    tenant_id: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class Span:
    """
    Represents execution span.
    """

    trace_id: str

    span_id: str

    name: str

    service: str

    parent_span_id: str | None

    started_at: datetime

    ended_at: datetime | None = None

    duration_ms: float | None = None

    status: str = "RUNNING"

    error: str | None = None

    attributes: dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class TraceRecord:
    """
    Complete trace record.
    """

    trace_id: str

    spans: list[Span]

    created_at: datetime



###############################################################################
# Configuration
###############################################################################


@dataclass
class TracingConfig:
    """
    Tracing configuration.
    """

    enabled: bool = True

    service_name: str = "rag-platform"

    retain_traces: int = 5000



###############################################################################
# Tracing Service
###############################################################################


class TracingService:
    """
    Central tracing service.

    """



    def __init__(
        self,
        config: TracingConfig | None = None,
    ):

        self.config = (

            config

            or TracingConfig()

        )


        self.traces: dict[str, TraceRecord] = {}



    ###########################################################################
    # Trace Management
    ###########################################################################


    def create_trace(
        self,
        service: str | None = None,
        tenant_id: str | None = None,
        metadata: dict | None = None,
    ) -> TraceContext:
        """
        Create new trace.
        """

        trace_id = uuid.uuid4().hex


        span_id = uuid.uuid4().hex



        context = TraceContext(

            trace_id=trace_id,

            span_id=span_id,

            service=service
            or self.config.service_name,

            tenant_id=tenant_id,

            metadata=metadata or {},

        )



        self.traces[trace_id] = TraceRecord(

            trace_id=trace_id,

            spans=[],

            created_at=datetime.now(
                timezone.utc
            ),

        )



        return context



    ###########################################################################
    # Span Handling
    ###########################################################################


    def start_span(
        self,
        name: str,
        context: TraceContext,
        attributes: dict | None = None,
    ) -> Span:
        """
        Start child span.
        """

        span = Span(

            trace_id=context.trace_id,

            span_id=uuid.uuid4().hex,

            name=name,

            service=context.service
            or self.config.service_name,

            parent_span_id=context.span_id,

            started_at=datetime.now(
                timezone.utc
            ),

            attributes=attributes or {},

        )


        self.traces[
            context.trace_id
        ].spans.append(
            span
        )


        return span



    def end_span(
        self,
        span: Span,
        error: Exception | None = None,
    ):
        """
        Complete span.
        """

        ended = datetime.now(
            timezone.utc
        )


        span.ended_at = ended


        span.duration_ms = (

            ended -

            span.started_at

        ).total_seconds() * 1000



        if error:

            span.status = "ERROR"

            span.error = str(
                error
            )

        else:

            span.status = "SUCCESS"



    ###########################################################################
    # Context Manager API
    ###########################################################################


    @contextmanager
    def span(
        self,
        name: str,
        context: TraceContext,
        attributes: dict | None = None,
    ) -> Generator[Span, None, None]:
        """
        Convenience span wrapper.

        Example:

            with tracer.span(
                "vector_search",
                context
            ):
                search()
        """

        span = self.start_span(

            name,

            context,

            attributes,

        )


        try:

            yield span


            self.end_span(
                span
            )


        except Exception as exc:

            self.end_span(

                span,

                exc,

            )

            raise



    ###########################################################################
    # Query APIs
    ###########################################################################


    def get_trace(
        self,
        trace_id: str,
    ) -> TraceRecord | None:
        """
        Fetch trace details.
        """

        return self.traces.get(
            trace_id
        )



    def get_slow_spans(
        self,
        threshold_ms: float = 1000,
    ) -> list[Span]:
        """
        Find slow operations.
        """

        result = []


        for trace in self.traces.values():

            for span in trace.spans:

                if (

                    span.duration_ms

                    and

                    span.duration_ms
                    > threshold_ms

                ):

                    result.append(
                        span
                    )


        return result



    ###########################################################################
    # Cleanup
    ###########################################################################


    def cleanup(
        self,
    ):
        """
        Remove old traces.
        """

        if len(self.traces) <= self.config.retain_traces:

            return



        remove_count = (

            len(self.traces)

            -

            self.config.retain_traces

        )


        for trace_id in list(
            self.traces.keys()
        )[:remove_count]:

            del self.traces[
                trace_id
            ]