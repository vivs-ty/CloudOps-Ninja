.PHONY: help setup dev run test deploy-aws deploy-gcp monitor clean

# CloudOps Ninja Makefile
# Quick commands for common tasks

help:
	@echo "🥷 CloudOps Ninja - Quick Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Run app locally"
	@echo "  make run            - Run with Docker Compose"
	@echo "  make stop           - Stop Docker containers"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-aws     - Deploy to AWS"
	@echo "  make deploy-gcp     - Deploy to GCP"
	@echo ""
	@echo "Monitoring:"
	@echo "  make monitor        - View Grafana dashboard"
	@echo "  make logs           - Tail application logs"
	@echo "  make health         - Run health check"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make clean-all      - Full cleanup including .terraform"

setup:
	@echo "🔧 Setting up CloudOps Ninja..."
	chmod +x scripts/*.sh
	./scripts/setup-linux.sh
	pip3 install -r backend/requirements.txt

dev:
	@echo "🚀 Running Flask app in development mode..."
	cd backend && python3 -m flask run --debug

run:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "✅ Containers started!"
	@echo "  - App: http://localhost:5000"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Grafana: http://localhost:3000 (admin/admin)"

stop:
	@echo "⏹️  Stopping containers..."
	docker-compose down

test:
	@echo "🧪 Running tests..."
	pytest backend/tests/ -v

deploy-aws:
	@echo "☁️  Deploying to AWS..."
	./scripts/deploy.sh aws 1.0.0 production

deploy-gcp:
	@echo "☁️  Deploying to GCP..."
	./scripts/deploy.sh gcp 1.0.0 production

monitor:
	@echo "📊 Opening Grafana dashboard..."
	open http://localhost:3000 || xdg-open http://localhost:3000 || echo "Visit http://localhost:3000"

logs:
	@echo "📝 Tail application logs..."
	docker-compose logs -f app

health:
	@echo "🏥 Running health check..."
	chmod +x scripts/health-check.sh
	./scripts/health-check.sh

build:
	@echo "🔨 Building Docker image..."
	docker build -t cloudops-ninja:latest backend/

psql:
	@echo "📊 Connecting to database..."
	@read -p "Enter DB host (default: localhost): " host; \
	read -p "Enter DB user (default: postgres): " user; \
	psql -h $${host:-localhost} -U $${user:-postgres}

terraform-init:
	@echo "🏗️  Initializing Terraform..."
	cd infrastructure/aws && terraform init
	cd infrastructure/gcp && terraform init

terraform-plan:
	@echo "📋 Planning Terraform changes..."
	cd infrastructure/aws && terraform plan
	cd infrastructure/gcp && terraform plan

clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f

clean-all:
	@echo "🧹 Full cleanup..."
	docker-compose down -v
	docker system prune -af
	rm -rf infrastructure/aws/.terraform infrastructure/aws/.terraform.lock.hcl
	rm -rf infrastructure/gcp/.terraform infrastructure/gcp/.terraform.lock.hcl
	rm -rf backend/__pycache__ backend/*.pyc

.DEFAULT_GOAL := help
