.PHONY: run down restart logs ps build soft-restart

DOCKER_COMPOSE_FILE = dockers/docker-compose.yml
COMPOSE_BAKE = true

run:
	@COMPOSE_BAKE=$(COMPOSE_BAKE) docker compose -f $(DOCKER_COMPOSE_FILE) up --build

down:
	@docker compose -f $(DOCKER_COMPOSE_FILE) down

restart: down run

soft-restart: logs
	@docker compose -f $(DOCKER_COMPOSE_FILE) restart 

logs:
	@docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

ps:
	@docker compose -f $(DOCKER_COMPOSE_FILE) ps

build:
	@docker compose -f $(DOCKER_COMPOSE_FILE) build