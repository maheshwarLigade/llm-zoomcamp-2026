"""
Tech Knowledge Navigator

AI Chat Assistant Page

Features:

- Conversational AI interface
- RAG powered responses
- Conversation history
- Source citations
- Feedback collection
- Context-aware follow-up questions


Backend:

POST /api/v1/chat


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import streamlit as st


from datetime import datetime



###############################################################################
# Page Configuration
###############################################################################

st.set_page_config(

    page_title="AI Knowledge Chat",

    page_icon="🤖",

    layout="wide",

)



###############################################################################
# Mock Backend Client
###############################################################################
# Replace with FastAPI integration
#
# Example:
#
# requests.post(
#   "/api/v1/chat",
#   json={
#       "message": question,
#       "conversation_id": id
#   }
# )
#
###############################################################################


def ask_knowledge_assistant(
    question: str,
    conversation_id: str,
):
    """
    Temporary mock response.

    Replace with backend API.

    """

    return {

        "answer": """
        Retrieval Augmented Generation (RAG)
        combines information retrieval with
        Large Language Models.

        The system first searches relevant
        knowledge chunks and then provides
        those chunks as context to the LLM.
        """,

        "sources": [

            {

                "title":
                    "RAG Architecture Guide",

                "page":
                    10,

                "score":
                    0.94,

            },


            {

                "title":
                    "Vector Database Design",

                "page":
                    5,

                "score":
                    0.88,

            }

        ]

    }



###############################################################################
# Session Initialization
###############################################################################


def initialize_session():

    if "messages" not in st.session_state:

        st.session_state.messages = []


    if "conversation_id" not in st.session_state:

        st.session_state.conversation_id = (

            datetime.utcnow()
            .strftime(
                "%Y%m%d%H%M%S"
            )

        )



###############################################################################
# Sidebar
###############################################################################


def render_sidebar():

    st.sidebar.title(

        "🤖 Chat Settings"

    )


    model = st.sidebar.selectbox(

        "LLM Model",

        [

            "GPT-5",

            "Claude",

            "Llama",

            "Gemma"

        ]

    )


    temperature = st.sidebar.slider(

        "Response Creativity",

        min_value=0.0,

        max_value=1.0,

        value=0.2,

    )


    show_sources = st.sidebar.checkbox(

        "Show Sources",

        value=True,

    )


    clear = st.sidebar.button(

        "Clear Conversation"

    )


    if clear:

        st.session_state.messages = []

        st.rerun()



    return {

        "model": model,

        "temperature": temperature,

        "show_sources": show_sources,

    }



###############################################################################
# Chat Message Renderer
###############################################################################


def render_message(
    role: str,
    content: str,
):

    with st.chat_message(role):

        st.markdown(
            content
        )



###############################################################################
# Source Renderer
###############################################################################


def render_sources(
    sources: list,
):

    st.subheader(
        "📚 Sources"
    )


    for index, source in enumerate(
        sources,
        start=1
    ):

        with st.expander(

            f"{index}. {source['title']}"

        ):

            st.write(

                f"""

                **Page:** {source['page']}


                **Similarity Score:**
                {source['score']}

                """

            )



###############################################################################
# Feedback Component
###############################################################################


def render_feedback():

    st.caption(

        "Was this answer useful?"

    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(

            "👍 Helpful"

        ):

            st.success(

                "Thanks for feedback!"

            )


    with col2:

        if st.button(

            "👎 Not Helpful"

        ):

            st.warning(

                "Feedback recorded"

            )



###############################################################################
# Main Page
###############################################################################


def main():

    initialize_session()


    config = render_sidebar()



    st.title(

        "🤖 AI Knowledge Assistant"

    )


    st.markdown(

        """
        Ask questions about your organization's
        knowledge base.

        The assistant uses:

        - Semantic Retrieval
        - Document Ranking
        - LLM Reasoning
        - Source Citations

        """

    )



    ###########################################################################
    # Existing Messages
    ###########################################################################


    for message in st.session_state.messages:

        render_message(

            message["role"],

            message["content"]

        )



    ###########################################################################
    # User Input
    ###########################################################################


    question = st.chat_input(

        "Ask something..."

    )



    if question:


        st.session_state.messages.append(

            {

                "role":
                    "user",

                "content":
                    question

            }

        )


        render_message(

            "user",

            question

        )



        with st.spinner(

            "Thinking..."

        ):


            response = ask_knowledge_assistant(

                question,

                st.session_state.conversation_id

            )



        answer = response["answer"]



        st.session_state.messages.append(

            {

                "role":
                    "assistant",

                "content":
                    answer

            }

        )


        render_message(

            "assistant",

            answer

        )



        if config["show_sources"]:

            render_sources(

                response["sources"]

            )



        render_feedback()



###############################################################################
# Application Entry
###############################################################################


if __name__ == "__main__":

    main()