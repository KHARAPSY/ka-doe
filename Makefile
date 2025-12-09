IMAGE_NAME ?= ka-doe
REGISTRY ?=
TAG ?= latest

DOCKERFILE = dockers/Dockerfile
DOCKER_COMPOSE = dockers/docker-compose.yml
DOCKER_COMPOSE_DEV  = dockers/docker-compose.dev.yml
DOCKER_COMPOSE_DBS  = dockers/docker-compose.dbs.yml

FULL_IMAGE = $(if $(REGISTRY),$(REGISTRY)/)$(IMAGE_NAME):$(TAG)

# ─────────────────────────────────────────────────────────────
#  Build & Push Image
# ─────────────────────────────────────────────────────────────

.PHONY: build push

build:
	@echo "Building $(FULL_IMAGE) ..."
	docker buildx build --load -t $(FULL_IMAGE) -f $(DOCKERFILE) .

push: build
	@echo "Pushing $(FULL_IMAGE) ..."
	docker push $(FULL_IMAGE)

# ─────────────────────────────────────────────────────────────
#  Production
# ─────────────────────────────────────────────────────────────

.PHONY: prod prod-run prod-logs prod-down

prod: prod-run prod-logs

prod-run:
	docker compose -f $(DOCKER_COMPOSE) --build up -d

prod-logs:
	docker compose -f $(DOCKER_COMPOSE) logs -f

prod-down:
	docker compose -f $(DOCKER_COMPOSE) down

# ─────────────────────────────────────────────────────────────
#  Development
# ─────────────────────────────────────────────────────────────

.PHONY: dev dev-run dev-logs dev-down

dev: dev-run dev-logs

dev-run:
	docker compose -f $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) --build up -d

dev-logs:
	docker compose -f $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) logs -f

dev-down:
	docker compose -f $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) down

# ─────────────────────────────────────────────────────────────
#  with Databases
# ─────────────────────────────────────────────────────────────

.PHONY: dbs dbs-dev

dbs:
	docker compose -f $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DBS) --build up -d

dev-dbs:
	docker compose -f $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) -f $(DOCKER_COMPOSE_DBS) --build up -d


# ─────────────────────────────────────────────────────────────
#  Local Setup
# ─────────────────────────────────────────────────────────────

.PHONY: run run-dev venv deps migr start start-reload

run: venv deps migr start
run-dev: venv deps migr start-reload

venv:
	python3 -m venv venv
	source venv/bin/activate

deps:
	python3 -m pip install -r requirements.txt

migr:
	alembic upgrade head

start:
	uvicorn app.main: app --reload --host 0.0.0.0 --port 8000

start-reload:
	uvicorn app.main: app --reload --host 0.0.0.0 --port 8000 --reload