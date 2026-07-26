"""
Tech Knowledge Navigator

Monitoring Dashboard

Features:

- System health monitoring
- API metrics
- LLM performance
- Retrieval metrics
- Error monitoring
- Trace inspection
- Tenant usage


Backend:

GET /api/v1/monitoring/metrics
GET /api/v1/monitoring/traces
GET /api/v1/monitoring/logs


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

    page_title="System Monitoring",

    page_icon="📈",

    layout="wide",

)



###############################################################################
# Mock Monitoring API
###############################################################################

def get_system_metrics():

    """
    Replace with:

    GET /api/v1/monitoring/metrics

    """

    return {

        "api": {

            "requests": 125000,

            "latency": 180,

            "error_rate": 0.012

        },

        "llm": {

            "requests": 45000,

            "avg_latency": 1250,

            "tokens": 8500000,

            "failures": 120

        },

        "retrieval": {

            "queries": 98000,

            "latency": 85,

            "avg_results": 8

        },

        "embedding": {

            "processed_chunks": 250000,

            "latency": 220

        }

    }



def get_recent_logs():

    """
    Replace with logging API.
    """

    return [

        {

            "time":
                "10:20:10",

            "level":
                "ERROR",

            "service":
                "llm-service",

            "message":
                "Provider timeout"

        },

        {

            "time":
                "10:21:30",

            "level":
                "WARNING",

            "service":
                "retrieval",

            "message":
                "High latency detected"

        },

        {

            "time":
                "10:22:01",

            "level":
                "INFO",

            "service":
                "embedding",

            "message":
                "Batch completed"

        }

    ]



def get_traces():

    """
    Replace with tracing API.
    """

    return [

        {

            "trace":
                "abc123",

            "operation":
                "chat_request",

            "latency":
                1450,

            "status":
                "SUCCESS"

        },

        {

            "trace":
                "xyz789",

            "operation":
                "vector_search",

            "latency":
                90,

            "status":
                "SUCCESS"

        }

    ]



###############################################################################
# Sidebar
###############################################################################

def render_sidebar():

    st.sidebar.title(

        "Monitoring Controls"

    )


    refresh = st.sidebar.slider(

        "Refresh Interval (seconds)",

        5,

        60,

        15

    )


    environment = st.sidebar.selectbox(

        "Environment",

        [

            "Production",

            "Staging",

            "Development"

        ]

    )


    return {

        "refresh": refresh,

        "environment": environment

    }



###############################################################################
# System Health
###############################################################################

def render_health():

    st.subheader(

        "🟢 System Health"

    )


    col1, col2, col3, col4 = st.columns(4)



    with col1:

        st.metric(

            "API Status",

            "Healthy"

        )


    with col2:

        st.metric(

            "Vector DB",

            "Healthy"

        )


    with col3:

        st.metric(

            "LLM Provider",

            "Healthy"

        )


    with col4:

        st.metric(

            "Workers",

            "12 Active"

        )



###############################################################################
# API Metrics
###############################################################################

def render_api_metrics(metrics):

    st.subheader(

        "🌐 API Metrics"

    )


    api = metrics["api"]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "Total Requests",

            f"{api['requests']:,}"

        )


    with col2:

        st.metric(

            "Average Latency",

            f"{api['latency']} ms"

        )


    with col3:

        st.metric(

            "Error Rate",

            f"{api['error_rate']*100:.2f}%"

        )



###############################################################################
# AI Metrics
###############################################################################

def render_ai_metrics(metrics):

    st.subheader(

        "🤖 AI Pipeline Metrics"

    )


    llm = metrics["llm"]

    retrieval = metrics["retrieval"]

    embedding = metrics["embedding"]



    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "LLM Requests",

            f"{llm['requests']:,}"

        )


        st.metric(

            "LLM Latency",

            f"{llm['avg_latency']} ms"

        )


    with col2:

        st.metric(

            "Retrieval Queries",

            f"{retrieval['queries']:,}"

        )


        st.metric(

            "Search Latency",

            f"{retrieval['latency']} ms"

        )


    with col3:

        st.metric(

            "Processed Chunks",

            f"{embedding['processed_chunks']:,}"

        )


        st.metric(

            "Embedding Latency",

            f"{embedding['latency']} ms"

        )



###############################################################################
# Logs
###############################################################################

def render_logs():

    st.subheader(

        "📜 Recent Logs"

    )


    logs = get_recent_logs()


    st.dataframe(

        logs,

        use_container_width=True

    )



###############################################################################
# Trace Viewer
###############################################################################

def render_traces():

    st.subheader(

        "🔎 Distributed Traces"

    )


    traces = get_traces()


    st.dataframe(

        traces,

        use_container_width=True

    )



###############################################################################
# Alerts
###############################################################################

def render_alerts():

    st.subheader(

        "🚨 Active Alerts"

    )


    alerts = [

        {

            "severity":
                "HIGH",

            "message":
                "LLM timeout rate increasing"

        },

        {

            "severity":
                "MEDIUM",

            "message":
                "Vector search latency above threshold"

        }

    ]


    for alert in alerts:

        st.warning(

            f"""

            **{alert['severity']}**

            {alert['message']}

            """

        )



###############################################################################
# Main
###############################################################################

def main():

    render_sidebar()


    st.title(

        "📈 Platform Monitoring"

    )


    st.markdown(

        """
        Real-time observability for:

        - RAG pipeline
        - AI services
        - Infrastructure
        - User activity

        """

    )


    metrics = get_system_metrics()


    render_health()


    st.divider()


    render_api_metrics(

        metrics

    )


    st.divider()


    render_ai_metrics(

        metrics

    )


    st.divider()


    render_alerts()


    st.divider()


    render_logs()


    st.divider()


    render_traces()



###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    main()