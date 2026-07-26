#!/usr/bin/env bash

###############################################################################
#
# Tech Knowledge Navigator
#
# benchmark.sh
#
# Benchmark the RAG API
#
###############################################################################

set -e

###############################################################################
# Configuration
###############################################################################

API_URL=${API_URL:-"http://localhost:8000/api/v1/chat"}

OUTPUT_DIR="benchmark-results"

REPORT_FILE="${OUTPUT_DIR}/report.txt"

CSV_FILE="${OUTPUT_DIR}/benchmark.csv"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

REQUESTS=${REQUESTS:-100}

CONCURRENCY=${CONCURRENCY:-10}

TIMEOUT=120

mkdir -p "${OUTPUT_DIR}"

###############################################################################
# Colors
###############################################################################

GREEN="\033[0;32m"

BLUE="\033[1;34m"

RED="\033[0;31m"

YELLOW="\033[1;33m"

NC="\033[0m"

###############################################################################
# Test Queries
###############################################################################

QUERIES=(
"Explain Kafka Consumer Groups"
"What is Retrieval Augmented Generation?"
"What is BM25?"
"What is Hybrid Search?"
"Explain Reciprocal Rank Fusion"
"What is Vector Search?"
"What is Prompt Injection?"
"What is Query Rewriting?"
"Explain Docker Compose"
"Difference between OpenSearch and Elasticsearch"
)

###############################################################################
# Header
###############################################################################

echo ""
echo "==============================================================="
echo "Tech Knowledge Navigator Benchmark"
echo "==============================================================="
echo ""

echo "Timestamp     : ${TIMESTAMP}"
echo "API           : ${API_URL}"
echo "Requests      : ${REQUESTS}"
echo "Concurrency   : ${CONCURRENCY}"
echo ""

###############################################################################
# Dependency Check
###############################################################################

if ! command -v hey >/dev/null 2>&1
then
    echo "ERROR: hey benchmark tool is not installed."
    echo ""
    echo "Install:"
    echo "go install github.com/rakyll/hey@latest"
    exit 1
fi

###############################################################################
# Health Check
###############################################################################

echo "Checking API..."

curl --silent \
     --fail \
     http://localhost:8000/health >/dev/null

echo -e "${GREEN}API is UP${NC}"
echo ""

###############################################################################
# Generate Payload
###############################################################################

PAYLOAD=$(cat <<EOF
{
  "query":"Explain Kafka Consumer Groups"
}
EOF
)

###############################################################################
# Run Benchmark
###############################################################################

echo ""
echo "Running benchmark..."
echo ""

hey \
-z 60s \
-c ${CONCURRENCY} \
-m POST \
-H "Content-Type: application/json" \
-d "${PAYLOAD}" \
${API_URL} \
> "${REPORT_FILE}"

###############################################################################
# Parse Results
###############################################################################

TOTAL=$(grep "Total:" "${REPORT_FILE}" | awk '{print $2}')

SLOWEST=$(grep "Slowest:" "${REPORT_FILE}" | awk '{print $2}')

FASTEST=$(grep "Fastest:" "${REPORT_FILE}" | awk '{print $2}')

AVERAGE=$(grep "Average:" "${REPORT_FILE}" | awk '{print $2}')

RPS=$(grep "Requests/sec:" "${REPORT_FILE}" | awk '{print $2}')

###############################################################################
# CSV
###############################################################################

echo "timestamp,total,average,fastest,slowest,rps" > "${CSV_FILE}"

echo "${TIMESTAMP},${TOTAL},${AVERAGE},${FASTEST},${SLOWEST},${RPS}" >> "${CSV_FILE}"

###############################################################################
# Summary
###############################################################################

echo ""
echo "======================================================="
echo "Benchmark Summary"
echo "======================================================="
echo ""

echo -e "${BLUE}Total Time${NC}       : ${TOTAL}"

echo -e "${BLUE}Average${NC}          : ${AVERAGE}"

echo -e "${BLUE}Fastest${NC}          : ${FASTEST}"

echo -e "${BLUE}Slowest${NC}          : ${SLOWEST}"

echo -e "${BLUE}Requests/sec${NC}     : ${RPS}"

echo ""

echo "CSV report"

echo "${CSV_FILE}"

echo ""

echo "Detailed report"

echo "${REPORT_FILE}"

echo ""

###############################################################################
# Success Rate
###############################################################################

SUCCESS=$(grep "2xx" "${REPORT_FILE}" || true)

if [ -n "$SUCCESS" ]
then
    echo -e "${GREEN}Benchmark Completed Successfully${NC}"
else
    echo -e "${RED}Benchmark Completed with Errors${NC}"
fi

echo ""