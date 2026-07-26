#!/usr/bin/env bash

###############################################################################
#
# Tech Knowledge Navigator
#
# bootstrap.sh
#
# Bootstrap script for local development.
#
# Responsibilities:
#   - Verify required tools
#   - Create project directories
#   - Create .env from template
#   - Create Python virtual environment
#   - Install Python dependencies
#   - Verify Docker installation
#   - Pull Docker images
#   - Initialize Git hooks (optional)
#
###############################################################################

set -Eeuo pipefail

###############################################################################
# Configuration
###############################################################################

PROJECT_NAME="Tech Knowledge Navigator"

PYTHON_VERSION="3.12"

VENV_DIR=".venv"

ENV_FILE=".env"

ENV_TEMPLATE=".env.example"

BACKEND_DIR="backend"

FRONTEND_DIR="frontend"

INGESTION_DIR="ingestion"

REQUIRED_COMMANDS=(
    git
    docker
    python3
    pip3
)

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

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

###############################################################################
# Banner
###############################################################################

echo ""
echo "=============================================================="
echo "            ${PROJECT_NAME}"
echo "              Bootstrap Script"
echo "=============================================================="
echo ""

###############################################################################
# Check Required Commands
###############################################################################

info "Checking required software..."

for cmd in "${REQUIRED_COMMANDS[@]}"
do
    if ! command -v "$cmd" >/dev/null 2>&1
    then
        error "$cmd is not installed."
        exit 1
    fi
done

success "Required software found."

###############################################################################
# Verify Docker
###############################################################################

info "Checking Docker..."

if ! docker info >/dev/null 2>&1
then
    error "Docker daemon is not running."
    exit 1
fi

success "Docker is running."

###############################################################################
# Create Directories
###############################################################################

info "Creating project directories..."

mkdir -p logs
mkdir -p tmp
mkdir -p benchmark-results
mkdir -p uploads
mkdir -p backups

success "Directories created."

###############################################################################
# Environment File
###############################################################################

if [[ ! -f "${ENV_FILE}" ]]
then
    if [[ -f "${ENV_TEMPLATE}" ]]
    then
        info "Creating .env from .env.example..."
        cp "${ENV_TEMPLATE}" "${ENV_FILE}"
        success ".env created."
    else
        warn ".env.example not found."
    fi
else
    info ".env already exists."
fi

###############################################################################
# Python Version
###############################################################################

info "Python Version"

python3 --version

###############################################################################
# Virtual Environment
###############################################################################

if [[ ! -d "${VENV_DIR}" ]]
then
    info "Creating Python virtual environment..."

    python3 -m venv "${VENV_DIR}"

    success "Virtual environment created."
else
    info "Virtual environment already exists."
fi

###############################################################################
# Activate VENV
###############################################################################

# shellcheck disable=SC1091

source "${VENV_DIR}/bin/activate"

###############################################################################
# Upgrade Pip
###############################################################################

info "Upgrading pip..."

pip install --upgrade pip wheel setuptools

###############################################################################
# Backend Dependencies
###############################################################################

if [[ -f "${BACKEND_DIR}/requirements.txt" ]]
then
    info "Installing backend dependencies..."

    pip install -r "${BACKEND_DIR}/requirements.txt"

    success "Backend dependencies installed."
else
    warn "backend/requirements.txt not found."
fi

###############################################################################
# Frontend Dependencies
###############################################################################

if [[ -f "${FRONTEND_DIR}/requirements.txt" ]]
then
    info "Installing frontend dependencies..."

    pip install -r "${FRONTEND_DIR}/requirements.txt"

    success "Frontend dependencies installed."
else
    warn "frontend/requirements.txt not found."
fi

###############################################################################
# Ingestion Dependencies
###############################################################################

if [[ -f "${INGESTION_DIR}/requirements.txt" ]]
then
    info "Installing ingestion dependencies..."

    pip install -r "${INGESTION_DIR}/requirements.txt"

    success "Ingestion dependencies installed."
fi

###############################################################################
# Pull Docker Images
###############################################################################

info "Pulling Docker images..."

docker compose pull || true

success "Docker images pulled."

###############################################################################
# Validate Docker Compose
###############################################################################

info "Validating docker-compose.yml..."

docker compose config >/dev/null

success "docker-compose.yml is valid."

###############################################################################
# Git Hooks
###############################################################################

if [[ -d ".git" ]]
then
    mkdir -p .git/hooks

    cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash

echo "Running basic validation..."

python -m compileall backend >/dev/null 2>&1

RESULT=$?

if [ $RESULT -ne 0 ]
then
    echo "Python compilation failed."

    exit 1
fi

echo "Validation successful."
EOF

    chmod +x .git/hooks/pre-commit

    success "Git pre-commit hook installed."
fi

###############################################################################
# Verify Project Structure
###############################################################################

info "Checking project folders..."

FOLDERS=(
backend
frontend
docs
scripts
tests
docker
evaluation
monitoring
)

for folder in "${FOLDERS[@]}"
do
    if [[ ! -d "$folder" ]]
    then
        warn "$folder directory missing."
    fi
done

###############################################################################
# Final Summary
###############################################################################

echo ""
echo "=============================================================="
echo "Bootstrap Completed"
echo "=============================================================="

echo ""

echo "Project              : ${PROJECT_NAME}"

echo "Python               : $(python3 --version)"

echo "Virtual Environment  : ${VENV_DIR}"

echo "Docker               : OK"

echo "Environment File     : ${ENV_FILE}"

echo ""

echo "Next Steps"

echo ""

echo "1. Activate virtual environment"

echo "   source ${VENV_DIR}/bin/activate"

echo ""

echo "2. Review .env"

echo ""

echo "3. Start the application"

echo ""

echo "   docker compose up --build"

echo ""

echo "4. Run ingestion"

echo ""

echo "   python ingestion/run_ingestion.py"

echo ""

echo "5. Open"

echo ""

echo "   API        : http://localhost:8000/docs"

echo "   Streamlit  : http://localhost:8501"

echo "   Grafana    : http://localhost:3000"

echo "   Prometheus : http://localhost:9090"

echo ""

success "Bootstrap completed successfully."