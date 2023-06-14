PROJECT_NAME = baseapi

build-images:
	docker build -t ${PROJECT_NAME}_backend .

server: build-images
	docker-compose -f docker-compose.yml up -d

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
	docker exec ${PROJECT_NAME}_backend interrogate .