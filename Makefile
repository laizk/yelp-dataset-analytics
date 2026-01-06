# -----------------------------------------
# File References
# -----------------------------------------
MAIN_COMPOSE = docker-compose.yml
AIRFLOW_COMPOSE = docker-compose.airflow.yml

# -----------------------------------------
# Helper
# -----------------------------------------
ifndef SERVICE
    SERVICE_MSG = "No service specified. Use: make <command> SERVICE=<name>"
endif

# -----------------------------------------
# Full Stack Operations
# -----------------------------------------

.PHONY: up-all
up-all:
	# Example: make up-all
	@echo "Starting ALL services..."
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) up -d --build

.PHONY: down-all
down-all:
	# Example: make down-all
	@echo "Stopping ALL services..."
	docker-compose -f $(MAIN_COMPOSE) --profile streaming stop streaming-reviews
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) down

.PHONY: restart-all
restart-all:
	# Example: make restart-all
	@echo "Restarting ALL services..."
	$(MAKE) down-all
	$(MAKE) up-all

.PHONY: logs-all
logs-all:
	# Example: make logs-all
	@echo "Showing logs for ALL services..."
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) logs -f

# -----------------------------------------
# Single-Service Operations (Generic)
# -----------------------------------------

.PHONY: up
up:
	# Example: make up SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Starting service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) up -d --no-deps --build $(SERVICE)

.PHONY: down
down:
	# Example: make down SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Stopping service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) stop $(SERVICE)

.PHONY: kill
kill:
	# Example: make kill SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Killing service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) kill $(SERVICE)

.PHONY: build
build:
	# Example: make build SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Building service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) build $(SERVICE)

.PHONY: restart
restart:
	# Example: make restart SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Restarting service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) stop $(SERVICE)
	docker-compose -f $(MAIN_COMPOSE) up -d --build $(SERVICE)

.PHONY: logs
logs:
	# Example: make logs SERVICE=serving-api
	@if [ -z "$(SERVICE)" ]; then echo $(SERVICE_MSG); exit 1; fi
	@echo "Logs for service: $(SERVICE)"
	docker-compose -f $(MAIN_COMPOSE) logs -f $(SERVICE)

# -----------------------------------------
# Streaming Jobs
# -----------------------------------------

.PHONY: streaming-reviews-up
streaming-reviews-up:
	# Example: make streaming-reviews-up
	@echo "Starting streaming-reviews..."
	docker-compose -f $(MAIN_COMPOSE) --profile streaming up -d --build streaming-reviews

.PHONY: streaming-reviews-down
streaming-reviews-down:
	# Example: make streaming-reviews-down
	@echo "Stopping streaming-reviews..."
	docker-compose -f $(MAIN_COMPOSE) stop streaming-reviews

.PHONY: streaming-reviews-logs
streaming-reviews-logs:
	# Example: make streaming-reviews-logs
	@echo "Logs for streaming-reviews..."
	docker-compose -f $(MAIN_COMPOSE) logs -f streaming-reviews

# -----------------------------------------
# Airflow Only
# -----------------------------------------

.PHONY: airflow-up
airflow-up:
	# Example: make airflow-up
	docker-compose -f $(AIRFLOW_COMPOSE) up -d --build

.PHONY: airflow-down
airflow-down:
	# Example: make airflow-down
	docker-compose -f $(AIRFLOW_COMPOSE) down

.PHONY: airflow-logs
airflow-logs:
	# Example: make airflow-logs
	docker-compose -f $(AIRFLOW_COMPOSE) logs -f
