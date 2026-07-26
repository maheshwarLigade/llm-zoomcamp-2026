"""
Tech Knowledge Navigator

Knowledge Ingestion Dashboard

Features:

- Upload documents
- Import external sources
- Configure ingestion pipeline
- Start ingestion jobs
- Track progress
- View ingestion history


Backend APIs:

POST /api/v1/ingestion/start

GET /api/v1/ingestion/jobs

GET /api/v1/ingestion/status/{job_id}


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

    page_title="Knowledge Ingestion",

    page_icon="📥",

    layout="wide",

)



###############################################################################
# Mock Backend Services
###############################################################################


def start_ingestion(
    source_type,
    source,
    config,
):
    """
    Replace with backend API call.

    POST /api/v1/ingestion/start

    """

    return {

        "job_id":
            "ING-20260726-001",

        "status":
            "RUNNING",

        "created_at":
            datetime.utcnow()
            .isoformat()

    }



def get_ingestion_jobs():

    """
    Replace with:

    GET /api/v1/ingestion/jobs

    """

    return [

        {

            "job_id":
                "ING-001",

            "source":
                "company-policy.pdf",

            "type":
                "PDF",

            "status":
                "COMPLETED",

            "chunks":
                450

        },


        {

            "job_id":
                "ING-002",

            "source":
                "youtube.com/video",

            "type":
                "YOUTUBE",

            "status":
                "RUNNING",

            "chunks":
                120

        },


        {

            "job_id":
                "ING-003",

            "source":
                "wiki article",

            "type":
                "WIKIPEDIA",

            "status":
                "FAILED",

            "chunks":
                0

        }

    ]



###############################################################################
# Sidebar Configuration
###############################################################################


def render_sidebar():

    st.sidebar.title(

        "⚙️ Pipeline Configuration"

    )


    chunking = st.sidebar.selectbox(

        "Chunking Strategy",

        [

            "Fixed Size",

            "Recursive",

            "Semantic"

        ]

    )


    embedding = st.sidebar.selectbox(

        "Embedding Model",

        [

            "text-embedding-3-small",

            "BGE Large",

            "E5 Large"

        ]

    )


    index = st.sidebar.selectbox(

        "Vector Index",

        [

            "Qdrant",

            "OpenSearch",

            "Pinecone"

        ]

    )


    return {

        "chunking":
            chunking,

        "embedding":
            embedding,

        "index":
            index

    }



###############################################################################
# Upload Section
###############################################################################


def render_upload():

    st.subheader(

        "📄 Upload Documents"

    )


    uploaded_files = st.file_uploader(

        "Choose files",

        type=[

            "pdf",

            "txt",

            "md",

            "docx"

        ],

        accept_multiple_files=True

    )


    if uploaded_files:

        st.success(

            f"{len(uploaded_files)} files selected"

        )


        for file in uploaded_files:

            st.write(

                f"📄 {file.name}"

            )



    return uploaded_files



###############################################################################
# External Sources
###############################################################################


def render_external_sources():

    st.subheader(

        "🌐 External Knowledge Sources"

    )


    source_type = st.selectbox(

        "Source Type",

        [

            "Website",

            "Wikipedia",

            "YouTube",

            "Article URL"

        ]

    )


    url = st.text_input(

        "Source URL"

    )


    return source_type, url



###############################################################################
# Pipeline Preview
###############################################################################


def render_pipeline():

    st.subheader(

        "🔄 Processing Pipeline"

    )


    pipeline = [

        "1️⃣ Document Collection",

        "2️⃣ Text Extraction",

        "3️⃣ Content Cleaning",

        "4️⃣ Chunk Generation",

        "5️⃣ Embedding Creation",

        "6️⃣ Vector Indexing"

    ]


    for step in pipeline:

        st.info(step)



###############################################################################
# Start Ingestion
###############################################################################


def render_start_button(
    config,
    files,
    source,
):

    st.divider()


    if st.button(

        "🚀 Start Ingestion",

        type="primary"

    ):


        if not files and not source:

            st.warning(

                "Please provide a document or source."

            )

            return



        with st.spinner(

            "Processing knowledge..."

        ):


            result = start_ingestion(

                source_type=
                    "FILE",

                source=
                    source,

                config=
                    config

            )



        st.success(

            "Ingestion started"

        )


        st.json(result)



###############################################################################
# Job History
###############################################################################


def render_jobs():

    st.subheader(

        "📋 Ingestion Jobs"

    )


    jobs = get_ingestion_jobs()


    st.dataframe(

        jobs,

        use_container_width=True

    )



###############################################################################
# Statistics
###############################################################################


def render_statistics():

    st.subheader(

        "📊 Knowledge Statistics"

    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(

            "Documents",

            "12,540"

        )


    with col2:

        st.metric(

            "Chunks",

            "350K"

        )


    with col3:

        st.metric(

            "Embeddings",

            "350K"

        )


    with col4:

        st.metric(

            "Index Size",

            "15 GB"

        )



###############################################################################
# Main
###############################################################################


def main():

    config = render_sidebar()


    st.title(

        "📥 Knowledge Ingestion"

    )


    st.markdown(

        """
        Import enterprise knowledge into
        Tech Knowledge Navigator.

        Supported sources:

        - PDF documents
        - Markdown
        - Websites
        - Wikipedia
        - YouTube
        - Articles

        """

    )


    files = render_upload()


    source_type, url = render_external_sources()



    render_pipeline()


    render_start_button(

        config,

        files,

        url

    )


    st.divider()


    render_statistics()


    st.divider()


    render_jobs()



###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    main()