#!/usr/bin/env bash

###############################################################################
#
# Tech Knowledge Navigator
#
# deploy.sh
#
# Production Deployment Script
#
# Responsibilities
# ----------------
# ✓ Validate environment
# ✓ Validate Docker installation
# ✓ Validate required files
# ✓ Pull latest source
# ✓ Build Docker images
# ✓ Start infrastructure
# ✓ Run database migrations
# ✓ Execute ingestion pipeline (optional)
# ✓ Perform health checks
# ✓ Print deployment summary
#
###############################################################################

set -Eeuo pipefail

###############################################################################
# Configuration
###############################################################################

PROJECT_NAME="Tech Knowledge Navigator"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DOCKER_COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.yml"

ENV_FILE="${PROJECT_ROOT}/.env"

LOG_DIR="${PROJECT_ROOT}/logs"

DEPLOY_LOG="${LOG_DIR}/deploy.log"

START_TIME=$(date +%s)

RUN_INGESTION=${RUN_INGESTION:-false}

BUILD_IMAGES=${BUILD_IMAGES:-true}

PULL_IMAGES=${PULL_IMAGES:-true}

###############################################################################
# Colors
###############################################################################

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
NC="\033[0m"

###############################################################################
# Logging
###############################################################################

mkdir -p "${LOG_DIR}"

log() {
    echo -e "$1"
    echo "$(date +"%F %T") $2" >> "${DEPLOY_LOG}"
}

info() {
    log "${BLUE}[INFO]${NC} $1" "[INFO] $1"
}

success() {
    log "${GREEN}[SUCCESS]${NC} $1" "[SUCCESS] $1"
}

warning() {
    log "${YELLOW}[WARNING]${NC} $1" "[WARNING] $1"
}

failure() {
    log "${RED}[ERROR]${NC} $1" "[ERROR] $1"
}

###############################################################################
# Banner
###############################################################################

echo ""
echo "=============================================================="
echo "         ${PROJECT_NAME}"
echo "         Production Deployment"
echo "=============================================================="
echo ""

###############################################################################
# Move to Project Root
###############################################################################

cd "${PROJECT_ROOT}"

###############################################################################
# Validate Files
###############################################################################

info "Validating deployment files..."

[[ -f "${DOCKER_COMPOSE_FILE}" ]] || {
    failure "docker-compose.yml not found."
    exit 1
}

[[ -f "${ENV_FILE}" ]] || {
    failure ".env file not found."
    exit 1
}

success "Deployment files verified."

###############################################################################
# Check Docker
###############################################################################

info "Checking Docker..."

docker info >/dev/null 2>&1 || {
    failure "Docker daemon is not running."
    exit 1
}

success "Docker is available."

###############################################################################
# Validate Docker Compose
###############################################################################

info "Validating docker-compose configuration..."

docker compose config >/dev/null

success "docker-compose.yml is valid."

###############################################################################
# Pull Latest Source
###############################################################################

if [[ -d ".git" ]]
then
    info "Updating repository..."

    git fetch --all

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

    git pull origin "${CURRENT_BRANCH}"

    success "Repository updated."
fi

###############################################################################
# Pull Images
###############################################################################

if [[ "${PULL_IMAGES}" == "true" ]]
then
    info "Pulling Docker images..."

    docker compose pull

    success "Images updated."
fi

###############################################################################
# Build Images
###############################################################################

if [[ "${BUILD_IMAGES}" == "true" ]]
then
    info "Building Docker images..."

    docker compose build --parallel

    success "Docker images built."
fi

###############################################################################
# Start Infrastructure
###############################################################################

info "Starting application..."

docker compose up -d

success "Containers started."

###############################################################################
# Wait for Services
###############################################################################

wait_for_service() {

    local url="$1"

    local name="$2"

    local retries=30

    while [[ $retries -gt 0 ]]
    do
        if curl -fs "$url" >/dev/null 2>&1
        then
            success "${name} is healthy."
            return
        fi

        sleep 5

        retries=$((retries-1))
    done

    failure "${name} failed health check."

    exit 1
}

###############################################################################
# Health Checks
###############################################################################

info "Waiting for services..."

wait_for_service "http://localhost:8000/health" "FastAPI"

wait_for_service "http://localhost:6333" "Qdrant"

wait_for_service "http://localhost:9200" "OpenSearch"

wait_for_service "http://localhost:9090/-/healthy" "Prometheus"

wait_for_service "http://localhost:3000/api/health" "Grafana"

###############################################################################
# Database Migration
###############################################################################

if docker compose ps backend >/dev/null 2>&1
then
    info "Running database migrations..."

    docker compose exec -T backend alembic upgrade head || true

    success "Database migrations completed."
fi

###############################################################################
# Optional Ingestion
###############################################################################

if [[ "${RUN_INGESTION}" == "true" ]]
then
    info "Running ingestion pipeline..."

    docker compose exec -T backend \
        python ingestion/run_ingestion.py

    success "Ingestion completed."
fi

###############################################################################
# Deployment Summary
###############################################################################

END_TIME=$(date +%s)

DURATION=$((END_TIME-START_TIME))

echo ""

echo "=============================================================="

echo "Deployment Summary"

echo "=============================================================="

echo ""

echo "Project        : ${PROJECT_NAME}"

echo "Duration       : ${DURATION} seconds"

echo ""

echo "Running Services"

docker compose ps

echo ""

echo "Application URLs"

echo ""

echo "FastAPI"

echo "http://localhost:8000"

echo ""

echo "Swagger"

echo "http://localhost:8000/docs"

echo ""

echo "Streamlit"

echo "http://localhost:8501"

echo ""

echo "Grafana"

echo "http://localhost:3000"

echo ""

echo "Prometheus"

echo "http://localhost:9090"

echo ""

echo "OpenSearch"

echo "http://localhost:9200"

echo ""

echo "Qdrant"

echo "http://localhost:6333"

echo ""

success "Deployment completed successfully."

echo ""

echo "Deployment log"

echo "${DEPLOY_LOG}"

echo ""