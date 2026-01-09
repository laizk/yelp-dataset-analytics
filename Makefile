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
	docker-compose -f $(MAIN_COMPOSE) --profile streaming stop streaming-reviews-enriched
	docker-compose -f $(MAIN_COMPOSE) --profile streaming stop streaming-bronze
	docker-compose -f $(MAIN_COMPOSE) --profile streaming stop streaming-mongo-multiplex
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

.PHONY: streaming-reviews-enriched-up
streaming-reviews-enriched-up:
	# Example: make streaming-reviews-enriched-up
	@echo "Starting streaming-reviews-enriched..."
	docker-compose -f $(MAIN_COMPOSE) --profile streaming up -d --build streaming-reviews-enriched

.PHONY: streaming-reviews-enriched-down
streaming-reviews-enriched-down:
	# Example: make streaming-reviews-enriched-down
	@echo "Stopping streaming-reviews-enriched..."
	docker-compose -f $(MAIN_COMPOSE) stop streaming-reviews-enriched

.PHONY: streaming-reviews-enriched-logs
streaming-reviews-enriched-logs:
	# Example: make streaming-reviews-enriched-logs
	@echo "Logs for streaming-reviews-enriched..."
	docker-compose -f $(MAIN_COMPOSE) logs -f streaming-reviews-enriched

.PHONY: streaming-bronze-up
streaming-bronze-up:
	# Example: make streaming-bronze-up
	@echo "Starting streaming-bronze..."
	docker-compose -f $(MAIN_COMPOSE) --profile streaming up -d --build streaming-bronze

.PHONY: streaming-bronze-down
streaming-bronze-down:
	# Example: make streaming-bronze-down
	@echo "Stopping streaming-bronze..."
	docker-compose -f $(MAIN_COMPOSE) stop streaming-bronze

.PHONY: streaming-bronze-logs
streaming-bronze-logs:
	# Example: make streaming-bronze-logs
	@echo "Logs for streaming-bronze..."
	docker-compose -f $(MAIN_COMPOSE) logs -f streaming-bronze

.PHONY: streaming-mongo-multiplex-up
streaming-mongo-multiplex-up:
	# Example: make streaming-mongo-multiplex-up
	@echo "Starting streaming-mongo-multiplex..."
	docker-compose -f $(MAIN_COMPOSE) --profile streaming up -d --build streaming-mongo-multiplex

.PHONY: streaming-mongo-multiplex-down
streaming-mongo-multiplex-down:
	# Example: make streaming-mongo-multiplex-down
	@echo "Stopping streaming-mongo-multiplex..."
	docker-compose -f $(MAIN_COMPOSE) stop streaming-mongo-multiplex

.PHONY: streaming-mongo-multiplex-logs
streaming-mongo-multiplex-logs:
	# Example: make streaming-mongo-multiplex-logs
	@echo "Logs for streaming-mongo-multiplex..."
	docker-compose -f $(MAIN_COMPOSE) logs -f streaming-mongo-multiplex

# -----------------------------------------
# Kafka Connect
# -----------------------------------------

.PHONY: kafka-connect-restart
kafka-connect-restart:
	# Example: make kafka-connect-restart
	@echo "Restarting kafka-connect and kafka-connect-init..."
	docker-compose -f $(MAIN_COMPOSE) stop kafka-connect kafka-connect-init
	docker-compose -f $(MAIN_COMPOSE) rm -f kafka-connect kafka-connect-init
	docker-compose -f $(MAIN_COMPOSE) up -d --build kafka-connect kafka-connect-init

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
