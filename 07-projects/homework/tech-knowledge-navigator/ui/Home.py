"""
Tech Knowledge Navigator

Main UI Application Entry Point.

Provides:

- AI knowledge assistant interface
- Document ingestion navigation
- Search and chat
- Monitoring dashboard
- System information


Framework:

Streamlit


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import streamlit as st


from pathlib import Path



###############################################################################
# Internal Imports
###############################################################################

from ui.styles.theme import apply_theme

from ui.components.sidebar import render_sidebar

from ui.components.metrics_card import render_system_metrics



###############################################################################
# Page Configuration
###############################################################################


st.set_page_config(

    page_title="Tech Knowledge Navigator",

    page_icon="🧠",

    layout="wide",

    initial_sidebar_state="expanded",

)



###############################################################################
# Load Styling
###############################################################################


apply_theme()



###############################################################################
# Application Header
###############################################################################


def render_header():

    st.title(
        "🧠 Tech Knowledge Navigator"
    )


    st.markdown(
        """
        Enterprise AI Knowledge Assistant powered by:

        - Retrieval Augmented Generation (RAG)
        - Vector Search
        - LLM Reasoning
        - Knowledge Ingestion Pipelines

        """
    )



###############################################################################
# Hero Section
###############################################################################


def render_home():

    st.header(
        "Welcome 👋"
    )


    st.write(

        """
        Tech Knowledge Navigator helps teams transform
        documents, videos, websites, and internal knowledge
        into an intelligent AI assistant.

        """

    )


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(

            label="Documents",

            value="10,000+"

        )



    with col2:

        st.metric(

            label="Knowledge Chunks",

            value="250K+"

        )



    with col3:

        st.metric(

            label="AI Queries",

            value="1M+"

        )



###############################################################################
# Feature Cards
###############################################################################


def render_features():

    st.subheader(
        "Platform Capabilities"
    )


    features = [

        (
            "📄 Knowledge Ingestion",

            "PDF, Wikipedia, YouTube, Websites and enterprise documents"

        ),

        (

            "🔍 Intelligent Search",

            "Semantic search powered by embeddings"

        ),

        (

            "🤖 AI Assistant",

            "Context-aware answers with citations"

        ),

        (

            "📊 Monitoring",

            "Track latency, usage and system health"

        ),

    ]



    cols = st.columns(4)



    for index, feature in enumerate(features):

        with cols[index]:

            st.info(

                f"""

                ### {feature[0]}


                {feature[1]}

                """

            )



###############################################################################
# Quick Actions
###############################################################################


def render_quick_actions():

    st.subheader(
        "Quick Actions"
    )


    col1, col2, col3 = st.columns(3)



    with col1:

        if st.button(
            "💬 Start Chat"
        ):

            st.switch_page(

                "pages/chat.py"

            )



    with col2:

        if st.button(
            "📚 Upload Knowledge"
        ):

            st.switch_page(

                "pages/ingestion.py"

            )



    with col3:

        if st.button(
            "📈 View Monitoring"
        ):

            st.switch_page(

                "pages/monitoring.py"

            )



###############################################################################
# Footer
###############################################################################


def render_footer():

    st.divider()


    st.caption(

        """
        Tech Knowledge Navigator

        Enterprise RAG Platform

        """

    )



###############################################################################
# Main
###############################################################################


def main():

    render_sidebar()


    render_header()


    render_home()


    render_features()


    render_quick_actions()


    render_footer()



if __name__ == "__main__":

    main()