"""
Tech Knowledge Navigator

Semantic Search Page

Features:

- Natural language search
- Hybrid search selection
- Result filtering
- Similarity score display
- Metadata inspection
- Source navigation


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

    page_title="Knowledge Search",

    page_icon="🔍",

    layout="wide",

)



###############################################################################
# Mock Search Client
###############################################################################
# Replace this with FastAPI client later
#
# Example:
#
# response = requests.post(
#     "/api/v1/search",
#     json={
#        "query": query
#     }
# )
#
###############################################################################


def search_documents(
    query: str,
    mode: str,
    limit: int,
):
    """
    Temporary search implementation.

    Replace with backend API call.

    """

    return [

        {
            "title":
                "Introduction to Retrieval Augmented Generation",

            "content":
                "RAG combines retrieval systems with large language models to provide grounded answers.",

            "score":
                0.92,

            "source":
                "rag-architecture.pdf",

            "page":
                12,

            "tags":
                [
                    "AI",
                    "RAG"
                ]

        },


        {
            "title":
                "Vector Database Design",

            "content":
                "Vector databases store embeddings and enable semantic similarity search.",

            "score":
                0.87,

            "source":
                "vector-search.md",

            "page":
                4,

            "tags":
                [
                    "Vector DB",
                    "Search"
                ]

        }

    ][:limit]



###############################################################################
# Sidebar Filters
###############################################################################


def render_sidebar():

    st.sidebar.header(
        "Search Configuration"
    )


    mode = st.sidebar.selectbox(

        "Search Mode",

        [

            "Semantic Search",

            "Hybrid Search",

            "Keyword Search"

        ]

    )


    result_count = st.sidebar.slider(

        "Number of Results",

        min_value=1,

        max_value=20,

        value=5,

    )


    min_score = st.sidebar.slider(

        "Minimum Similarity Score",

        min_value=0.0,

        max_value=1.0,

        value=0.5,

        step=0.05,

    )


    return {

        "mode":
            mode,

        "limit":
            result_count,

        "min_score":
            min_score,

    }



###############################################################################
# Search Result Card
###############################################################################


def render_result(
    result: dict,
    index: int,
):

    st.markdown(

        f"""
        ## {index}. {result["title"]}

        **Similarity Score:** 
        `{result["score"]}`


        **Source:** 
        `{result["source"]}`


        **Page:** 
        `{result["page"]}`

        """

    )


    st.write(

        result["content"]

    )


    st.caption(

        "Tags: "

        +

        ", ".join(
            result["tags"]
        )

    )


    with st.expander(
        "View Metadata"
    ):

        st.json(

            {

                "document":
                    result["title"],

                "source":
                    result["source"],

                "page":
                    result["page"],

                "indexed_at":
                    datetime.utcnow()
                    .isoformat(),

                "retrieval":
                    {

                        "method":
                            "vector_similarity",

                        "score":
                            result["score"]

                    }

            }

        )


    st.divider()



###############################################################################
# Main Page
###############################################################################


def main():

    st.title(
        "🔍 Knowledge Search"
    )


    st.markdown(

        """
        Search your enterprise knowledge base using
        natural language.

        Examples:

        - "How does RAG architecture work?"
        - "Explain Redis persistence"
        - "What are our deployment guidelines?"

        """

    )


    config = render_sidebar()



    query = st.text_input(

        "Ask your knowledge base",

        placeholder=
        "Enter your question..."

    )



    search_clicked = st.button(

        "🔍 Search",

        type="primary"

    )



    if search_clicked:


        if not query.strip():

            st.warning(

                "Please enter a search query."

            )

            return



        with st.spinner(

            "Searching knowledge base..."

        ):


            results = search_documents(

                query=query,

                mode=config["mode"],

                limit=config["limit"]

            )



        filtered_results = [

            result

            for result in results

            if result["score"]
            >=
            config["min_score"]

        ]



        st.success(

            f"Found {len(filtered_results)} relevant documents"

        )



        if not filtered_results:

            st.info(

                "No matching knowledge found."

            )

            return



        for index, result in enumerate(

            filtered_results,

            start=1

        ):

            render_result(

                result,

                index

            )



###############################################################################
# Entry Point
###############################################################################


if __name__ == "__main__":

    main()