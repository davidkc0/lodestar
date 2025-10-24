# Flask API Boilerplate Makefile

.PHONY: help install dev test clean docker-build docker-up docker-down migrate upgrade

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  clean       - Clean up temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up   - Start Docker containers"
	@echo "  docker-down - Stop Docker containers"
	@echo "  migrate     - Create database migration"
	@echo "  upgrade     - Apply database migrations"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Lint code with flake8"

# Install dependencies
install:
	pip install -r requirements.txt

# Run development server
dev:
	python run.py

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-prod:
	docker-compose -f docker-compose.prod.yml up -d

# Database migrations
migrate:
	flask db migrate -m "$(MSG)"

upgrade:
	flask db upgrade

# Code formatting and linting
format:
	black .
	isort .

lint:
	flake8

# Setup development environment
setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp env.example .env
	@echo "Setup complete! Activate virtual environment with: source venv/bin/activate"
