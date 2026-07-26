"""
Timer Utilities

Reusable timing utilities for measuring execution time
across the RAG application.

Used for:
- API latency
- Retrieval performance
- LLM latency
- Embedding generation
- Ingestion pipeline monitoring

Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations

import asyncio
import functools
import time

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Callable



###############################################################################
# Timer Result
###############################################################################


@dataclass
class TimerResult:
    """
    Timer execution result.
    """

    name: str

    elapsed_ms: float

    started_at: datetime

    completed_at: datetime



###############################################################################
# Basic Timer
###############################################################################


class Timer:
    """
    Simple execution timer.

    Example:

        timer = Timer("embedding")

        timer.start()

        generate_embeddings()

        result = timer.stop()

        print(result.elapsed_ms)
    """

    def __init__(
        self,
        name: str = "operation",
    ):

        self.name = name

        self.start_time: float | None = None

        self.end_time: float | None = None

        self.started_at: datetime | None = None

        self.completed_at: datetime | None = None



    def start(self) -> None:
        """
        Start timer.
        """

        self.start_time = time.perf_counter()

        self.started_at = datetime.now(
            timezone.utc
        )



    def stop(self) -> TimerResult:
        """
        Stop timer and return result.
        """

        if self.start_time is None:
            raise RuntimeError(
                "Timer was not started"
            )


        self.end_time = time.perf_counter()

        self.completed_at = datetime.now(
            timezone.utc
        )


        return TimerResult(
            name=self.name,
            elapsed_ms=(
                self.end_time
                -
                self.start_time
            )
            * 1000,

            started_at=self.started_at,

            completed_at=self.completed_at,
        )



    @property
    def elapsed_ms(self) -> float:
        """
        Get elapsed milliseconds.
        """

        if (
            self.start_time is None
            or self.end_time is None
        ):
            return 0.0


        return (
            self.end_time
            -
            self.start_time
        ) * 1000



###############################################################################
# Context Manager Timer
###############################################################################


class TimerContext:
    """
    Context manager timer.

    Example:

        with TimerContext("retrieval") as timer:

            search_documents()


        print(timer.elapsed_ms)
    """

    def __init__(
        self,
        name: str,
    ):

        self.timer = Timer(name)

        self.result: TimerResult | None = None



    def __enter__(self):

        self.timer.start()

        return self.timer



    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        self.result = self.timer.stop()



###############################################################################
# Function Decorator
###############################################################################


def measure_time(
    name: str | None = None,
):
    """
    Measure synchronous function execution time.

    Example:

        @measure_time("embedding")

        def create_embeddings():
            pass

    """

    def decorator(
        function: Callable,
    ):

        @functools.wraps(function)
        def wrapper(
            *args,
            **kwargs,
        ):

            timer_name = (
                name
                or function.__name__
            )

            timer = Timer(timer_name)

            timer.start()

            try:

                return function(
                    *args,
                    **kwargs,
                )

            finally:

                result = timer.stop()

                print(
                    f"{result.name}: "
                    f"{result.elapsed_ms:.2f} ms"
                )


        return wrapper


    return decorator



###############################################################################
# Async Function Decorator
###############################################################################


def measure_async_time(
    name: str | None = None,
):
    """
    Measure async function execution time.

    Example:

        @measure_async_time("llm_call")

        async def call_llm():
            pass

    """

    def decorator(
        function: Callable,
    ):


        @functools.wraps(function)
        async def wrapper(
            *args,
            **kwargs,
        ):

            timer_name = (
                name
                or function.__name__
            )


            timer = Timer(
                timer_name
            )

            timer.start()


            try:

                return await function(
                    *args,
                    **kwargs,
                )

            finally:

                result = timer.stop()

                print(
                    f"{result.name}: "
                    f"{result.elapsed_ms:.2f} ms"
                )


        return wrapper


    return decorator



###############################################################################
# Pipeline Timer
###############################################################################


class PipelineTimer:
    """
    Measure multiple pipeline stages.

    Example:

        pipeline = PipelineTimer()

        pipeline.start("retrieval")

        search()

        pipeline.stop("retrieval")


    Output:

        {
            "retrieval":120,
            "reranking":50,
            "llm":800
        }
    """

    def __init__(self):

        self.timers: dict[str, Timer] = {}

        self.results: dict[str, float] = {}



    def start(
        self,
        step: str,
    ):

        timer = Timer(step)

        timer.start()

        self.timers[step] = timer



    def stop(
        self,
        step: str,
    ):

        timer = self.timers.get(step)

        if timer is None:
            raise RuntimeError(
                f"Timer not found: {step}"
            )


        result = timer.stop()

        self.results[step] = (
            result.elapsed_ms
        )



    def summary(self) -> dict[str, float]:
        """
        Return pipeline timing summary.
        """

        return self.results



###############################################################################
# Utility Functions
###############################################################################


def current_timestamp_ms() -> int:
    """
    Current epoch timestamp milliseconds.
    """

    return int(
        time.time() * 1000
    )



def sleep_ms(
    milliseconds: int,
):
    """
    Sleep for milliseconds.
    """

    time.sleep(
        milliseconds / 1000
    )



async def async_sleep_ms(
    milliseconds: int,
):
    """
    Async sleep for milliseconds.
    """

    await asyncio.sleep(
        milliseconds / 1000
    )