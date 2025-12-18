# MLOps Platform Makefile

.PHONY: help setup build up down logs test clean format lint

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "MLOps Platform - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - create directories and install dependencies
	@echo "Setting up MLOps platform..."
	mkdir -p src/services src/events src/models config/prometheus config/grafana data models
	cp .env.example .env
	pip install -r requirements.txt
	@echo "Setup complete!"

build: ## Build all Docker images
	@echo "Building Docker images..."
	docker-compose build

up: ## Start all services
	@echo "Starting services..."
	docker-compose up -d
	@echo "Services started! Access:"
	@echo "  - API: http://localhost:8000"
	@echo "  - MLflow: http://localhost:5000"
	@echo "  - RabbitMQ Management: http://localhost:15672"
	@echo "  - Grafana: http://localhost:3000"
	@echo "  - Prometheus: http://localhost:9090"

down: ## Stop all services
	@echo "Stopping services..."
	docker-compose down

restart: down up ## Restart all services

logs: ## Show logs from all services
	docker-compose logs -f

logs-pytorch: ## Show PyTorch service logs
	docker-compose logs -f pytorch-service

logs-tensorflow: ## Show TensorFlow service logs
	docker-compose logs -f tensorflow-service

logs-rag: ## Show RAG service logs
	docker-compose logs -f rag-service

ps: ## Show running services
	docker-compose ps

# Development commands
test: ## Run tests
	@echo "Running tests..."
	pytest tests/ -v --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

test-unit: ## Run unit tests only
	pytest tests/unit/ -v

test-integration: ## Run integration tests only
	pytest tests/integration/ -v

format: ## Format code with black and isort
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "Code formatted!"

lint: ## Run linters
	@echo "Running linters..."
	flake8 src/ tests/
	mypy src/
	pylint src/

# Database commands
db-migrate: ## Run database migrations
	alembic upgrade head

db-rollback: ## Rollback last migration
	alembic downgrade -1

db-reset: ## Reset database
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	alembic upgrade head

# MLflow commands
mlflow-ui: ## Open MLflow UI
	@echo "Opening MLflow UI..."
	open http://localhost:5000

mlflow-clean: ## Clean MLflow experiments
	docker-compose exec mlflow mlflow gc

# Monitoring
grafana-ui: ## Open Grafana UI
	@echo "Opening Grafana UI..."
	open http://localhost:3000

prometheus-ui: ## Open Prometheus UI
	@echo "Opening Prometheus UI..."
	open http://localhost:9090

# Cleanup
clean: ## Clean up temporary files and caches
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	@echo "Cleanup complete!"

clean-docker: ## Remove all Docker containers, images, and volumes
	@echo "Removing Docker resources..."
	docker-compose down -v --rmi all --remove-orphans
	@echo "Docker cleanup complete!"

# Data management
data-download: ## Download sample datasets
	@echo "Downloading sample datasets..."
	python scripts/download_datasets.py

data-preprocess: ## Preprocess datasets
	@echo "Preprocessing datasets..."
	python scripts/preprocess_data.py

# Model management
model-train: ## Train models
	@echo "Training models..."
	python scripts/train_model.py

model-evaluate: ## Evaluate models
	@echo "Evaluating models..."
	python scripts/evaluate_model.py

model-export: ## Export models for deployment
	@echo "Exporting models..."
	python scripts/export_model.py

# Shell access
shell-pytorch: ## Open shell in PyTorch container
	docker-compose exec pytorch-service /bin/bash

shell-tensorflow: ## Open shell in TensorFlow container
	docker-compose exec tensorflow-service /bin/bash

shell-rag: ## Open shell in RAG container
	docker-compose exec rag-service /bin/bash

# Quick start
quickstart: setup build up ## Quick start - setup, build, and run everything
	@echo ""
	@echo "🚀 MLOps Platform is ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Check service status: make ps"
	@echo "  2. View logs: make logs"
	@echo "  3. Run tests: make test"
	@echo "  4. Open MLflow UI: make mlflow-ui"
	@echo ""

# Production deployment
deploy-prod: ## Deploy to production (requires kubectl)
	@echo "Deploying to production..."
	kubectl apply -f k8s/
	kubectl rollout status deployment/pytorch-service
	kubectl rollout status deployment/tensorflow-service
	@echo "Deployment complete!"

deploy-staging: ## Deploy to staging
	@echo "Deploying to staging..."
	kubectl apply -f k8s/ --namespace=staging
	@echo "Staging deployment complete!"
