"""
Tech Knowledge Navigator

Backend API Client

Central HTTP client for Streamlit UI.

Responsibilities:

- API communication
- Authentication handling
- Error handling
- Request retries
- Response validation


Backend:

FastAPI


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import time


from typing import Any


import requests



###############################################################################
# Logger
###############################################################################

logger = logging.getLogger(__name__)



###############################################################################
# Configuration
###############################################################################

class APIConfig:
    """
    API client configuration.
    """


    BASE_URL = (

        "http://localhost:8000"

    )


    TIMEOUT = 30


    MAX_RETRIES = 3




###############################################################################
# Exceptions
###############################################################################

class APIClientException(Exception):
    """
    Base API client exception.
    """



class APIConnectionException(
    APIClientException
):
    """
    Backend unavailable.
    """



class APIResponseException(
    APIClientException
):
    """
    Invalid backend response.
    """



###############################################################################
# API Client
###############################################################################

class APIClient:
    """
    Generic FastAPI client.

    Used by all UI pages.

    Example:

        client = APIClient()

        response = client.post(
            "/api/v1/chat",
            payload
        )

    """



    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
    ):

        self.base_url = (

            base_url

            or APIConfig.BASE_URL

        ).rstrip("/")



        self.token = token



    ###########################################################################
    # Headers
    ###########################################################################

    def _headers(self):

        headers = {

            "Content-Type":
                "application/json"

        }


        if self.token:

            headers[
                "Authorization"
            ] = (

                f"Bearer {self.token}"

            )


        return headers



    ###########################################################################
    # Request Executor
    ###########################################################################

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """
        Execute HTTP request.

        Includes:

        - Retry
        - Timeout
        - Error handling

        """

        url = (

            f"{self.base_url}"

            f"{endpoint}"

        )


        last_exception = None



        for attempt in range(

            APIConfig.MAX_RETRIES

        ):


            try:


                response = requests.request(

                    method,

                    url,

                    json=payload,

                    params=params,

                    headers=self._headers(),

                    timeout=
                        APIConfig.TIMEOUT

                )



                if response.status_code >= 400:

                    raise APIResponseException(

                        f"""

                        API Error:

                        {response.status_code}

                        {response.text}

                        """

                    )



                return response.json()



            except requests.exceptions.ConnectionError as exc:


                last_exception = exc


                logger.error(

                    "Backend connection failed: %s",

                    exc

                )


                time.sleep(

                    attempt + 1

                )



            except requests.exceptions.Timeout as exc:


                last_exception = exc


                logger.error(

                    "Backend timeout"

                )



        raise APIConnectionException(

            "Backend unavailable"

        ) from last_exception



    ###########################################################################
    # GET
    ###########################################################################

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ):

        return self._request(

            "GET",

            endpoint,

            params=params

        )



    ###########################################################################
    # POST
    ###########################################################################

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
    ):

        return self._request(

            "POST",

            endpoint,

            payload=payload

        )



    ###########################################################################
    # PUT
    ###########################################################################

    def put(
        self,
        endpoint: str,
        payload: dict | None = None,
    ):

        return self._request(

            "PUT",

            endpoint,

            payload=payload

        )



    ###########################################################################
    # DELETE
    ###########################################################################

    def delete(
        self,
        endpoint: str,
    ):

        return self._request(

            "DELETE",

            endpoint

        )



###############################################################################
# Domain Specific Clients
###############################################################################

class SearchAPIClient:
    """
    Search API wrapper.
    """



    def __init__(
        self,
        client: APIClient,
    ):

        self.client = client



    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict | None = None,
    ):


        return self.client.post(

            "/api/v1/search",

            {

                "query":
                    query,

                "limit":
                    limit,

                "filters":
                    filters or {}

            }

        )



###############################################################################


class ChatAPIClient:
    """
    Chat API wrapper.
    """



    def __init__(
        self,
        client: APIClient,
    ):

        self.client = client



    def chat(
        self,
        message: str,
        conversation_id: str,
    ):


        return self.client.post(

            "/api/v1/chat",

            {

                "message":
                    message,

                "conversation_id":
                    conversation_id

            }

        )



###############################################################################


class IngestionAPIClient:
    """
    Ingestion API wrapper.
    """



    def __init__(
        self,
        client: APIClient,
    ):

        self.client = client



    def start(
        self,
        source_type: str,
        source: str,
        config: dict,
    ):


        return self.client.post(

            "/api/v1/ingestion/start",

            {

                "source_type":
                    source_type,

                "source":
                    source,

                "config":
                    config

            }

        )



    def jobs(self):

        return self.client.get(

            "/api/v1/ingestion/jobs"

        )



###############################################################################


class MonitoringAPIClient:
    """
    Monitoring API wrapper.
    """



    def __init__(
        self,
        client: APIClient,
    ):

        self.client = client



    def metrics(self):

        return self.client.get(

            "/api/v1/monitoring/metrics"

        )



    def traces(self):

        return self.client.get(

            "/api/v1/monitoring/traces"

        )



###############################################################################
# Singleton
###############################################################################

api_client = APIClient()


search_client = SearchAPIClient(

    api_client

)


chat_client = ChatAPIClient(

    api_client

)


ingestion_client = IngestionAPIClient(

    api_client

)


monitoring_client = MonitoringAPIClient(

    api_client

)