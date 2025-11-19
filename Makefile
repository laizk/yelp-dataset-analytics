# Paths to Docker Compose files
MAIN_COMPOSE = docker-compose.yml
AIRFLOW_COMPOSE = docker-compose.airflow.yml

# Default target
.PHONY: up
up:
	@echo "Starting full stack (Kafka, Yelp Producer, Airflow)..."
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) up -d --build

.PHONY: down
down:
	@echo "Stopping full stack..."
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) down

.PHONY: logs
logs:
	@echo "Showing logs for all services..."
	docker-compose -f $(MAIN_COMPOSE) -f $(AIRFLOW_COMPOSE) logs -f

.PHONY: restart
restart:
	@echo "Restarting full stack..."
	$(MAKE) down
	$(MAKE) up

.PHONY: airflow
airflow:
	@echo "Starting only Airflow..."
	docker-compose -f $(AIRFLOW_COMPOSE) up -d --build

.PHONY: airflow-down
airflow-down:
	@echo "Stopping only Airflow..."
	docker-compose -f $(AIRFLOW_COMPOSE) down

.PHONY: kafka
kafka:
	@echo "Starting Kafka stack..."
	docker-compose -f $(MAIN_COMPOSE) up -d --build

.PHONY: kafka-down
kafka-down:
	@echo "Stopping Kafka stack..."
	docker-compose -f $(MAIN_COMPOSE) down
