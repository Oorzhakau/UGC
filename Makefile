start_dev:
	docker-compose -f docker-compose.dev.yml up

start_dev_build:
	docker-compose -f docker-compose.dev.yml up --build

stop_dev:
	docker-compose -f docker-compose.dev.yml down

start_prod:
	docker-compose -f docker-compose.yml up

start_prod_build:
	docker-compose -f docker-compose.yml up --build

stop_prod:
	docker-compose -f docker-compose.yml down
