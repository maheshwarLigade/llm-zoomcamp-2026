"""
Tech Knowledge Navigator

Authentication Client

Responsibilities:

- User login
- JWT token handling
- Session management
- Token refresh
- User profile retrieval
- RBAC permission checks


Backend APIs:

POST /api/v1/auth/login

POST /api/v1/auth/refresh

GET  /api/v1/auth/me

POST /api/v1/auth/logout


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


from datetime import datetime, timedelta


import streamlit as st



from ui.services.api_client import APIClient



###############################################################################
# Logger
###############################################################################

logger = logging.getLogger(__name__)



###############################################################################
# Authentication Configuration
###############################################################################

class AuthConfig:

    TOKEN_KEY = "access_token"

    REFRESH_TOKEN_KEY = "refresh_token"

    USER_KEY = "current_user"

    EXPIRES_KEY = "token_expiry"



###############################################################################
# Exceptions
###############################################################################

class AuthenticationException(Exception):
    """
    Authentication failure.
    """



class AuthorizationException(Exception):
    """
    Permission denied.
    """



###############################################################################
# Auth Client
###############################################################################

class AuthClient:
    """
    Authentication client.

    Handles:

    - Login
    - Logout
    - JWT lifecycle
    - User permissions

    """



    def __init__(
        self,
        api_client: APIClient,
    ):

        self.api_client = api_client



    ###########################################################################
    # Login
    ###########################################################################

    def login(
        self,
        username: str,
        password: str,
    ) -> dict:
        """
        Authenticate user.

        """

        try:

            response = self.api_client.post(

                "/api/v1/auth/login",

                {

                    "username":
                        username,

                    "password":
                        password

                }

            )


            self._save_session(

                response

            )


            return response



        except Exception as exc:

            logger.error(

                "Login failed: %s",

                exc

            )


            raise AuthenticationException(

                "Invalid username or password"

            ) from exc



    ###########################################################################
    # Logout
    ###########################################################################

    def logout(self):

        try:

            self.api_client.post(

                "/api/v1/auth/logout"

            )


        except Exception:

            pass


        self.clear_session()



    ###########################################################################
    # Refresh Token
    ###########################################################################

    def refresh_token(self):

        refresh_token = (

            st.session_state.get(

                AuthConfig.REFRESH_TOKEN_KEY

            )

        )


        if not refresh_token:

            raise AuthenticationException(

                "Refresh token missing"

            )


        response = self.api_client.post(

            "/api/v1/auth/refresh",

            {

                "refresh_token":

                    refresh_token

            }

        )


        self._save_session(

            response

        )


        return response



    ###########################################################################
    # Current User
    ###########################################################################

    def current_user(self):

        return st.session_state.get(

            AuthConfig.USER_KEY

        )



    ###########################################################################
    # Token
    ###########################################################################

    def get_token(self):

        return st.session_state.get(

            AuthConfig.TOKEN_KEY

        )



    ###########################################################################
    # Authentication Check
    ###########################################################################

    def is_authenticated(self):

        return bool(

            self.get_token()

        )



    ###########################################################################
    # Permission Check
    ###########################################################################

    def has_role(
        self,
        role: str,
    ) -> bool:

        user = self.current_user()


        if not user:

            return False



        roles = user.get(

            "roles",

            []

        )


        return role in roles



    ###########################################################################
    # Permission Validation
    ###########################################################################

    def require_role(
        self,
        role: str,
    ):

        if not self.has_role(role):

            raise AuthorizationException(

                f"Role required: {role}"

            )



    ###########################################################################
    # Tenant Access
    ###########################################################################

    def tenant_id(self):

        user = self.current_user()


        if not user:

            return None


        return user.get(

            "tenant_id"

        )



    ###########################################################################
    # Session Storage
    ###########################################################################

    def _save_session(
        self,
        response: dict,
    ):

        st.session_state[

            AuthConfig.TOKEN_KEY

        ] = response.get(

            "access_token"

        )


        st.session_state[

            AuthConfig.REFRESH_TOKEN_KEY

        ] = response.get(

            "refresh_token"

        )


        st.session_state[

            AuthConfig.USER_KEY

        ] = response.get(

            "user"

        )


        expires_in = response.get(

            "expires_in",

            3600

        )


        st.session_state[

            AuthConfig.EXPIRES_KEY

        ] = (

            datetime.utcnow()

            +

            timedelta(

                seconds=expires_in

            )

        )



    ###########################################################################
    # Clear Session
    ###########################################################################

    def clear_session(self):

        keys = [

            AuthConfig.TOKEN_KEY,

            AuthConfig.REFRESH_TOKEN_KEY,

            AuthConfig.USER_KEY,

            AuthConfig.EXPIRES_KEY

        ]


        for key in keys:

            if key in st.session_state:

                del st.session_state[key]



    ###########################################################################
    # Token Expiry Check
    ###########################################################################

    def is_token_expired(self):

        expiry = st.session_state.get(

            AuthConfig.EXPIRES_KEY

        )


        if not expiry:

            return True



        return datetime.utcnow() >= expiry



###############################################################################
# Login UI Helper
###############################################################################

def render_login():

    """
    Reusable login component.

    """

    st.title(

        "🔐 Login"

    )


    username = st.text_input(

        "Username"

    )


    password = st.text_input(

        "Password",

        type="password"

    )



    if st.button(

        "Login"

    ):

        try:

            auth_client.login(

                username,

                password

            )


            st.success(

                "Login successful"

            )


            st.rerun()



        except AuthenticationException as exc:

            st.error(

                str(exc)

            )



###############################################################################
# Global Client Instance
###############################################################################

from ui.services.api_client import api_client



auth_client = AuthClient(

    api_client

)