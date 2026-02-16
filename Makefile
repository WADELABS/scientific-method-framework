.PHONY: help install test test-integration test-unit docker-build docker-up docker-down docs clean

help:
	@echo "Scientific Method Framework - Available Commands"
	@echo "=================================================="
	@echo "  make install           - Install dependencies"
	@echo "  make test              - Run unit tests"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make test-all          - Run all tests"
	@echo "  make docker-build      - Build Docker image"
	@echo "  make docker-up         - Start Docker Compose"
	@echo "  make docker-down       - Stop Docker Compose"
	@echo "  make docker-dev        - Start development environment"
	@echo "  make docs              - Serve documentation locally"
	@echo "  make api               - Run API server locally"
	@echo "  make clean             - Clean build artifacts"
	@echo "  make lint              - Run code linters"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -r api/requirements.txt
	@echo "✓ Dependencies installed"

test-unit:
	@echo "Running unit tests..."
	pytest tests/ -v --cov=core --cov=src -m "not integration and not docker"

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v -m integration

test-all:
	@echo "Running all tests..."
	pytest tests/ -v --cov=core --cov=src

test: test-unit

docker-build:
	@echo "Building Docker image..."
	docker build -t smf:latest .
	@echo "✓ Docker image built"

docker-up:
	@echo "Starting Docker Compose..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo "  MkDocs: http://localhost:8080"

docker-down:
	@echo "Stopping Docker Compose..."
	docker-compose down
	@echo "✓ Services stopped"

docker-dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up
	@echo "✓ Development environment ready"

docs:
	@echo "Serving documentation..."
	@echo "Documentation will be available at http://localhost:8000"
	mkdocs serve

api:
	@echo "Starting API server..."
	@echo "API will be available at http://localhost:8000"
	@echo "Swagger docs at http://localhost:8000/docs"
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	@echo "Running flake8..."
	flake8 core/ src/ api/ --max-line-length=120 --ignore=E501,W503

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/
	@echo "✓ Clean complete"
