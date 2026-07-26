"""
Application Metrics Collection

Provides metrics abstraction for the RAG platform.

Tracks:

- API requests
- Processing latency
- LLM calls
- Embedding generation
- Retrieval performance
- Ingestion statistics
- Errors


Can integrate with:

- Prometheus
- OpenTelemetry
- Grafana
- Datadog


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import time


from dataclasses import dataclass, field


from datetime import datetime, timezone


from collections import defaultdict


from typing import Any



logger = logging.getLogger(__name__)



###############################################################################
# Models
###############################################################################


@dataclass
class MetricEvent:
    """
    Represents a metric event.
    """

    name: str

    value: float

    metric_type: str

    service: str

    component: str | None = None

    tenant_id: str | None = None

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    labels: dict[str, str] = field(
        default_factory=dict
    )



@dataclass
class MetricsSnapshot:
    """
    Aggregated metrics snapshot.
    """

    counters: dict[str, float]

    averages: dict[str, float]

    gauges: dict[str, float]

    generated_at: datetime



###############################################################################
# Configuration
###############################################################################


@dataclass
class MetricsConfig:
    """
    Metrics configuration.
    """

    enabled: bool = True

    retain_events: int = 10000

    track_tenant_metrics: bool = True



###############################################################################
# Timer Utility
###############################################################################


class MetricTimer:
    """
    Measures execution duration.

    Example:

        async with metrics.timer("llm_latency"):
            await llm.call()

    """

    def __init__(
        self,
        collector,
        metric_name: str,
        service: str,
    ):

        self.collector = collector

        self.metric_name = metric_name

        self.service = service

        self.start_time = None



    def __enter__(self):

        self.start_time = time.perf_counter()

        return self



    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        elapsed = (

            time.perf_counter()

            -

            self.start_time

        )


        self.collector.record(

            name=self.metric_name,

            value=elapsed * 1000,

            metric_type="timer",

            service=self.service,

        )



###############################################################################
# Metrics Collector
###############################################################################


class MetricsCollector:
    """
    Central metrics collection service.

    """



    def __init__(
        self,
        config: MetricsConfig | None = None,
    ):

        self.config = (

            config

            or MetricsConfig()

        )


        self.events: list[MetricEvent] = []



        self.counters = defaultdict(
            float
        )



        self.values = defaultdict(
            list
        )



        self.gauges = defaultdict(
            float
        )



    ###########################################################################
    # Record Metrics
    ###########################################################################


    def record(
        self,
        name: str,
        value: float,
        metric_type: str,
        service: str,
        component: str | None = None,
        tenant_id: str | None = None,
        labels: dict[str, str] | None = None,
    ):
        """
        Record metric event.
        """

        if not self.config.enabled:

            return



        event = MetricEvent(

            name=name,

            value=value,

            metric_type=metric_type,

            service=service,

            component=component,

            tenant_id=tenant_id,

            labels=labels or {},

        )


        self.events.append(
            event
        )


        if metric_type == "counter":

            self.counters[name] += value



        elif metric_type == "timer":

            self.values[name].append(
                value
            )



        elif metric_type == "gauge":

            self.gauges[name] = value



        self._cleanup()



    ###########################################################################
    # Common Application Metrics
    ###########################################################################


    def record_api_request(
        self,
        endpoint: str,
        latency_ms: float,
        status_code: int,
    ):
        """
        Record API request metrics.
        """

        self.record(

            name="api_requests_total",

            value=1,

            metric_type="counter",

            service="api",

            labels={

                "endpoint":
                    endpoint,

                "status":
                    str(status_code),

            },

        )


        self.record(

            name="api_latency_ms",

            value=latency_ms,

            metric_type="timer",

            service="api",

        )



    def record_llm_call(
        self,
        provider: str,
        latency_ms: float,
        tokens: int,
        success: bool,
    ):
        """
        Record LLM metrics.
        """

        self.record(

            name="llm_requests_total",

            value=1,

            metric_type="counter",

            service="llm",

            labels={

                "provider":
                    provider,

            },

        )


        self.record(

            name="llm_latency_ms",

            value=latency_ms,

            metric_type="timer",

            service="llm",

        )


        self.record(

            name="llm_tokens_total",

            value=tokens,

            metric_type="counter",

            service="llm",

        )


        if not success:

            self.record(

                name="llm_failures_total",

                value=1,

                metric_type="counter",

                service="llm",

            )



    def record_embedding(
        self,
        model: str,
        chunks: int,
        latency_ms: float,
    ):
        """
        Record embedding metrics.
        """

        self.record(

            name="embedding_chunks_total",

            value=chunks,

            metric_type="counter",

            service="embedding",

            labels={

                "model":
                    model

            },

        )


        self.record(

            name="embedding_latency_ms",

            value=latency_ms,

            metric_type="timer",

            service="embedding",

        )



    def record_retrieval(
        self,
        query: str,
        results: int,
        latency_ms: float,
    ):
        """
        Record retrieval metrics.
        """

        self.record(

            name="retrieval_requests_total",

            value=1,

            metric_type="counter",

            service="retrieval",

        )


        self.record(

            name="retrieval_results",

            value=results,

            metric_type="gauge",

            service="retrieval",

        )


        self.record(

            name="retrieval_latency_ms",

            value=latency_ms,

            metric_type="timer",

            service="retrieval",

        )



    ###########################################################################
    # Reporting
    ###########################################################################


    def snapshot(
        self,
    ) -> MetricsSnapshot:
        """
        Generate metrics snapshot.
        """

        averages = {}


        for name, values in self.values.items():

            if values:

                averages[name] = (

                    sum(values)

                    /

                    len(values)

                )



        return MetricsSnapshot(

            counters=dict(
                self.counters
            ),

            averages=averages,

            gauges=dict(
                self.gauges
            ),

            generated_at=datetime.now(
                timezone.utc
            ),

        )



    ###########################################################################
    # Helpers
    ###########################################################################


    def timer(
        self,
        name: str,
        service: str,
    ):

        return MetricTimer(

            collector=self,

            metric_name=name,

            service=service,

        )



    def _cleanup(
        self,
    ):

        if len(self.events) > self.config.retain_events:

            self.events = self.events[
                -self.config.retain_events:
            ]