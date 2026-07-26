"""
Tech Knowledge Navigator

Platform Settings

Features:

- LLM configuration
- Embedding configuration
- Vector database settings
- Retrieval tuning
- RAG parameters
- Security configuration
- Feature flags


Backend APIs:

GET  /api/v1/settings

PUT  /api/v1/settings


Author:
Tech Knowledge Navigator
"""

from __future__ import annotations


import streamlit as st



###############################################################################
# Page Configuration
###############################################################################

st.set_page_config(

    page_title="Platform Settings",

    page_icon="⚙️",

    layout="wide",

)



###############################################################################
# Mock Settings API
###############################################################################

def load_settings():

    """
    Replace with:

    GET /api/v1/settings

    """

    return {

        "llm": {

            "provider":
                "OpenAI",

            "model":
                "gpt-5",

            "temperature":
                0.2,

            "max_tokens":
                2048

        },


        "embedding": {

            "model":
                "text-embedding-3-small",

            "dimension":
                1536

        },


        "vector_db": {

            "provider":
                "Qdrant",

            "collection":
                "knowledge"

        },


        "retrieval": {

            "top_k":
                5,

            "reranking":
                True,

            "similarity_threshold":
                0.75

        },


        "security": {

            "authentication":
                "JWT",

            "audit_logging":
                True

        }

    }



def save_settings(settings):

    """
    Replace with:

    PUT /api/v1/settings

    """

    return True



###############################################################################
# LLM Settings
###############################################################################

def render_llm_settings(settings):

    st.subheader(

        "🤖 LLM Configuration"

    )


    llm = settings["llm"]


    provider = st.selectbox(

        "Provider",

        [

            "OpenAI",

            "Groq",

            "Ollama",

            "Anthropic"

        ],

        index=[

            "OpenAI",

            "Groq",

            "Ollama",

            "Anthropic"

        ].index(

            llm["provider"]

        )

    )


    model = st.text_input(

        "Model Name",

        value=llm["model"]

    )


    temperature = st.slider(

        "Temperature",

        0.0,

        1.0,

        llm["temperature"],

        0.1

    )


    max_tokens = st.number_input(

        "Maximum Tokens",

        value=llm["max_tokens"]

    )


    return {

        "provider":
            provider,

        "model":
            model,

        "temperature":
            temperature,

        "max_tokens":
            max_tokens

    }



###############################################################################
# Embedding Settings
###############################################################################

def render_embedding_settings(settings):

    st.subheader(

        "🧠 Embedding Configuration"

    )


    embedding = settings["embedding"]


    model = st.selectbox(

        "Embedding Model",

        [

            "text-embedding-3-small",

            "text-embedding-3-large",

            "BGE Large",

            "E5 Large"

        ],

        index=0

    )


    dimension = st.number_input(

        "Vector Dimension",

        value=embedding["dimension"]

    )


    return {

        "model":
            model,

        "dimension":
            dimension

    }



###############################################################################
# Vector Database Settings
###############################################################################

def render_vector_settings(settings):

    st.subheader(

        "🗄 Vector Database"

    )


    vector = settings["vector_db"]


    provider = st.selectbox(

        "Vector Store",

        [

            "Qdrant",

            "OpenSearch",

            "Pinecone",

            "Weaviate"

        ],

        index=0

    )


    collection = st.text_input(

        "Collection Name",

        value=vector["collection"]

    )


    return {

        "provider":
            provider,

        "collection":
            collection

    }



###############################################################################
# Retrieval Settings
###############################################################################

def render_retrieval_settings(settings):

    st.subheader(

        "🔍 Retrieval Configuration"

    )


    retrieval = settings["retrieval"]


    top_k = st.slider(

        "Top K Results",

        1,

        50,

        retrieval["top_k"]

    )


    threshold = st.slider(

        "Similarity Threshold",

        0.0,

        1.0,

        retrieval["similarity_threshold"]

    )


    reranking = st.checkbox(

        "Enable Re-ranking",

        value=retrieval["reranking"]

    )


    return {

        "top_k":
            top_k,

        "threshold":
            threshold,

        "reranking":
            reranking

    }



###############################################################################
# Security Settings
###############################################################################

def render_security_settings(settings):

    st.subheader(

        "🔐 Security"

    )


    security = settings["security"]


    authentication = st.selectbox(

        "Authentication",

        [

            "JWT",

            "OAuth2",

            "SAML"

        ]

    )


    audit_logging = st.checkbox(

        "Enable Audit Logging",

        value=security["audit_logging"]

    )


    return {

        "authentication":
            authentication,

        "audit_logging":
            audit_logging

    }



###############################################################################
# Feature Flags
###############################################################################

def render_features():

    st.subheader(

        "🚀 Feature Flags"

    )


    col1, col2 = st.columns(2)


    with col1:

        st.checkbox(

            "Enable Streaming Responses",

            value=True

        )


        st.checkbox(

            "Enable Citations",

            value=True

        )


    with col2:

        st.checkbox(

            "Enable Feedback Collection",

            value=True

        )


        st.checkbox(

            "Enable Conversation Memory",

            value=True

        )



###############################################################################
# Main
###############################################################################

def main():

    st.title(

        "⚙️ Platform Settings"

    )


    st.markdown(

        """
        Configure your Tech Knowledge Navigator
        AI platform.

        Changes affect:

        - LLM generation
        - Retrieval quality
        - Vector indexing
        - Security

        """

    )


    settings = load_settings()



    with st.form(

        "settings_form"

    ):


        llm = render_llm_settings(

            settings

        )


        st.divider()


        embedding = render_embedding_settings(

            settings

        )


        st.divider()


        vector = render_vector_settings(

            settings

        )


        st.divider()


        retrieval = render_retrieval_settings(

            settings

        )


        st.divider()


        security = render_security_settings(

            settings

        )


        st.divider()


        render_features()



        submitted = st.form_submit_button(

            "💾 Save Settings"

        )



        if submitted:


            updated = {

                "llm":
                    llm,

                "embedding":
                    embedding,

                "vector_db":
                    vector,

                "retrieval":
                    retrieval,

                "security":
                    security

            }



            if save_settings(updated):

                st.success(

                    "Settings saved successfully"

                )



###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    main()