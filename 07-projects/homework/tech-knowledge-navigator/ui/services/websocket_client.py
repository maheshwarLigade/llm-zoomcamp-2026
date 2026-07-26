"""
Tech Knowledge Navigator

WebSocket Client

Responsibilities:

- Real-time communication
- Streaming responses
- Chat token streaming
- Ingestion progress updates
- Evaluation progress
- Monitoring events


Backend:

FastAPI WebSocket


Endpoints:

/ws/chat/{conversation_id}

/ws/ingestion/{job_id}

/ws/monitoring


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import json

import logging

from typing import Callable, Generator


import websocket



from ui.services.auth_client import auth_client



###############################################################################
# Logger
###############################################################################

logger = logging.getLogger(__name__)



###############################################################################
# Configuration
###############################################################################

class WebSocketConfig:


    BASE_URL = (

        "ws://localhost:8000"

    )


    TIMEOUT = 30



###############################################################################
# Exceptions
###############################################################################

class WebSocketClientException(Exception):
    """
    WebSocket communication error.
    """



class WebSocketConnectionException(
    WebSocketClientException
):
    """
    Connection failure.
    """



###############################################################################
# Base WebSocket Client
###############################################################################

class WebSocketClient:
    """
    Generic WebSocket client.

    Handles:

    - Connection
    - Authentication
    - Message receiving
    - Closing connection

    """



    def __init__(
        self,
        base_url: str | None = None,
    ):


        self.base_url = (

            base_url

            or WebSocketConfig.BASE_URL

        ).rstrip("/")



        self.socket = None



    ###########################################################################
    # Authentication Header
    ###########################################################################

    def _headers(self):

        token = auth_client.get_token()


        if token:

            return [

                f"Authorization: Bearer {token}"

            ]


        return []



    ###########################################################################
    # Connect
    ###########################################################################

    def connect(
        self,
        endpoint: str,
    ):

        url = (

            f"{self.base_url}"

            f"{endpoint}"

        )


        try:

            self.socket = websocket.WebSocket()

            self.socket.connect(

                url,

                header=self._headers()

            )


        except Exception as exc:


            logger.error(

                "WebSocket connection failed: %s",

                exc

            )


            raise WebSocketConnectionException(

                "Unable to connect WebSocket"

            ) from exc



    ###########################################################################
    # Send Message
    ###########################################################################

    def send(
        self,
        payload: dict,
    ):

        if not self.socket:

            raise WebSocketClientException(

                "WebSocket not connected"

            )


        self.socket.send(

            json.dumps(payload)

        )



    ###########################################################################
    # Receive
    ###########################################################################

    def receive(self):

        if not self.socket:

            raise WebSocketClientException(

                "WebSocket not connected"

            )


        message = self.socket.recv()


        return json.loads(

            message

        )



    ###########################################################################
    # Stream Messages
    ###########################################################################

    def stream(
        self,
    ) -> Generator[dict, None, None]:

        while True:


            try:

                message = self.receive()


                yield message



                if message.get(

                    "event"

                ) == "completed":

                    break



            except Exception:

                break



    ###########################################################################
    # Close
    ###########################################################################

    def close(self):

        if self.socket:

            self.socket.close()

            self.socket = None



###############################################################################
# Chat Streaming Client
###############################################################################

class ChatStreamClient:
    """
    Streaming LLM responses.

    Example event:

    {
       "event":"token",
       "content":"Hello"
    }

    """



    def __init__(
        self,
        client: WebSocketClient,
    ):

        self.client = client



    def stream_chat(
        self,
        conversation_id: str,
        message: str,
    ):


        self.client.connect(

            f"/ws/chat/{conversation_id}"

        )


        self.client.send(

            {

                "message":
                    message

            }

        )


        for event in self.client.stream():


            yield event



        self.client.close()



###############################################################################
# Ingestion Progress Client
###############################################################################

class IngestionStreamClient:
    """
    Real-time ingestion updates.

    Events:

    - extracting
    - cleaning
    - chunking
    - embedding
    - indexing
    - completed

    """



    def __init__(
        self,
        client: WebSocketClient,
    ):

        self.client = client



    def watch_job(
        self,
        job_id: str,
    ):


        self.client.connect(

            f"/ws/ingestion/{job_id}"

        )


        for event in self.client.stream():

            yield event



        self.client.close()



###############################################################################
# Monitoring Stream Client
###############################################################################

class MonitoringStreamClient:
    """
    Real-time monitoring events.

    """



    def __init__(
        self,
        client: WebSocketClient,
    ):

        self.client = client



    def subscribe(self):

        self.client.connect(

            "/ws/monitoring"

        )


        for event in self.client.stream():

            yield event



        self.client.close()



###############################################################################
# Singleton Instances
###############################################################################

ws_client = WebSocketClient()



chat_stream_client = ChatStreamClient(

    ws_client

)



ingestion_stream_client = IngestionStreamClient(

    ws_client

)



monitoring_stream_client = MonitoringStreamClient(

    ws_client

)