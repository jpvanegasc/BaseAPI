PROJECT_NAME = api

build-images:
	docker build -f local/Dockerfile -t ${PROJECT_NAME}_backend .

server: build-images
	docker-compose -f docker-compose.local.yml up -d
	sleep 1
	docker exec ${PROJECT_NAME}_backend alembic upgrade head
	docker exec ${PROJECT_NAME}_backend uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

server-stop:
	docker-compose -f docker-compose.local.yml down

logs:
	docker logs ${PROJECT_NAME}_backend

migrate:
	docker exec ${PROJECT_NAME}_backend alembic upgrade head

container-bash:
	docker exec -it ${PROJECT_NAME}_backend /bin/bash

lint:
	docker exec ${PROJECT_NAME}_backend black .
	docker exec ${PROJECT_NAME}_backend flake8 .

test:
	docker exec ${PROJECT_NAME}_backend coverage run -m pytest -c tests/pytest.ini tests/
	docker exec ${PROJECT_NAME}_backend coverage report