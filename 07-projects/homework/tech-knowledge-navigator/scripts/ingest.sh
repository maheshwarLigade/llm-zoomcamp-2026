#!/usr/bin/env bash

###############################################################################
#
# Tech Knowledge Navigator
#
# ingest.sh
#
# End-to-End Knowledge Base Ingestion Pipeline
#
# Responsibilities
# ----------------
# ✓ Validate environment
# ✓ Verify required services
# ✓ Download datasets (optional)
# ✓ Parse documents
# ✓ Clean documents
# ✓ Chunk documents
# ✓ Generate embeddings
# ✓ Index into OpenSearch
# ✓ Index into Qdrant
# ✓ Store metadata
# ✓ Verify ingestion
# ✓ Generate ingestion report
#
###############################################################################

set -Eeuo pipefail

###############################################################################
# Configuration
###############################################################################

PROJECT_NAME="Tech Knowledge Navigator"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DATA_DIR="${PROJECT_ROOT}/data"

RAW_DATA="${DATA_DIR}/raw"

PROCESSED_DATA="${DATA_DIR}/processed"

LOG_DIR="${PROJECT_ROOT}/logs"

REPORT_DIR="${PROJECT_ROOT}/reports"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

LOG_FILE="${LOG_DIR}/ingestion-${TIMESTAMP}.log"

REPORT_FILE="${REPORT_DIR}/ingestion-report-${TIMESTAMP}.md"

DOWNLOAD_DATASET=${DOWNLOAD_DATASET:-false}

DATASET_URL=${DATASET_URL:-""}

###############################################################################
# Colors
###############################################################################

GREEN="\033[0;32m"
RED="\033[0;31m"
BLUE="\033[1;34m"
YELLOW="\033[1;33m"
NC="\033[0m"

###############################################################################
# Helper Functions
###############################################################################

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[INFO] $(date '+%F %T') $1" >> "${LOG_FILE}"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[SUCCESS] $(date '+%F %T') $1" >> "${LOG_FILE}"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[WARNING] $(date '+%F %T') $1" >> "${LOG_FILE}"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[ERROR] $(date '+%F %T') $1" >> "${LOG_FILE}"
}

###############################################################################
# Banner
###############################################################################

mkdir -p "${LOG_DIR}"
mkdir -p "${REPORT_DIR}"
mkdir -p "${RAW_DATA}"
mkdir -p "${PROCESSED_DATA}"

echo ""
echo "=============================================================="
echo "          ${PROJECT_NAME}"
echo "      Knowledge Base Ingestion Pipeline"
echo "=============================================================="
echo ""

###############################################################################
# Dependency Check
###############################################################################

REQUIRED_COMMANDS=(
python3
curl
docker
)

info "Checking required commands..."

for cmd in "${REQUIRED_COMMANDS[@]}"
do
    if ! command -v "$cmd" >/dev/null 2>&1
    then
        error "$cmd is not installed."

        exit 1
    fi
done

success "Dependencies verified."

###############################################################################
# Health Check
###############################################################################

check_service() {

    local url="$1"

    local service="$2"

    if curl --silent --fail "$url" >/dev/null
    then
        success "$service is available."
    else
        error "$service is unavailable."

        exit 1
    fi
}

info "Checking infrastructure..."

check_service http://localhost:8000/health FastAPI

check_service http://localhost:9200 OpenSearch

check_service http://localhost:6333 Qdrant

###############################################################################
# Optional Dataset Download
###############################################################################

if [[ "${DOWNLOAD_DATASET}" == "true" ]]
then

    if [[ -z "${DATASET_URL}" ]]
    then
        error "DATASET_URL not provided."

        exit 1
    fi

    info "Downloading dataset..."

    curl -L "${DATASET_URL}" \
        -o "${RAW_DATA}/dataset.zip"

    success "Dataset downloaded."
fi

###############################################################################
# Step 1 - Parse Documents
###############################################################################

info "Parsing documents..."

python ingestion/parse_documents.py \
    --input "${RAW_DATA}" \
    --output "${PROCESSED_DATA}"

success "Documents parsed."

###############################################################################
# Step 2 - Clean Documents
###############################################################################

info "Cleaning documents..."

python ingestion/clean_documents.py \
    --input "${PROCESSED_DATA}"

success "Cleaning completed."

###############################################################################
# Step 3 - Chunk Documents
###############################################################################

info "Chunking documents..."

python ingestion/chunk_documents.py \
    --input "${PROCESSED_DATA}" \
    --chunk-size 512 \
    --overlap 64

success "Chunking completed."

###############################################################################
# Step 4 - Metadata Extraction
###############################################################################

info "Extracting metadata..."

python ingestion/extract_metadata.py \
    --input "${PROCESSED_DATA}"

success "Metadata extracted."

###############################################################################
# Step 5 - Embedding Generation
###############################################################################

info "Generating embeddings..."

python ingestion/generate_embeddings.py \
    --input "${PROCESSED_DATA}"

success "Embeddings generated."

###############################################################################
# Step 6 - OpenSearch Index
###############################################################################

info "Indexing OpenSearch..."

python ingestion/index_opensearch.py \
    --input "${PROCESSED_DATA}"

success "OpenSearch indexing completed."

###############################################################################
# Step 7 - Qdrant Index
###############################################################################

info "Indexing Qdrant..."

python ingestion/index_qdrant.py \
    --input "${PROCESSED_DATA}"

success "Qdrant indexing completed."

###############################################################################
# Step 8 - Verification
###############################################################################

info "Running ingestion verification..."

python ingestion/verify_ingestion.py

success "Verification completed."

###############################################################################
# Generate Report
###############################################################################

TOTAL_DOCS=$(find "${RAW_DATA}" -type f | wc -l | xargs)

TOTAL_CHUNKS=$(find "${PROCESSED_DATA}" -name "*.json" 2>/dev/null | wc -l | xargs)

cat > "${REPORT_FILE}" <<EOF
# Ingestion Report

Generated

${TIMESTAMP}

---

## Summary

| Item | Count |
|------|------:|
| Raw Documents | ${TOTAL_DOCS} |
| Processed Chunks | ${TOTAL_CHUNKS} |

---

## Pipeline

- Dataset Validation
- Document Parsing
- Cleaning
- Chunking
- Metadata Extraction
- Embedding Generation
- OpenSearch Indexing
- Qdrant Indexing
- Verification

---

Status

**SUCCESS**

EOF

###############################################################################
# Summary
###############################################################################

echo ""
echo "=============================================================="
echo "Ingestion Summary"
echo "=============================================================="
echo ""

printf "%-30s %s\n" "Raw Documents" "${TOTAL_DOCS}"

printf "%-30s %s\n" "Processed Chunks" "${TOTAL_CHUNKS}"

printf "%-30s %s\n" "OpenSearch" "Indexed"

printf "%-30s %s\n" "Qdrant" "Indexed"

printf "%-30s %s\n" "Status" "SUCCESS"

echo ""

echo "Report"

echo "${REPORT_FILE}"

echo ""

echo "Log"

echo "${LOG_FILE}"

echo ""

success "Knowledge base ingestion completed successfully."

echo ""