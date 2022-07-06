PROJECT_NAME = api

build-images:
	docker build -f local/Dockerfile -t ${PROJECT_NAME}_backend .

server: build-images
	docker-compose up -d

test:
	docker exec $(PROJECT_NAME)_backend coverage run -m pytest -c tests/pytest.ini tests/
	docker exec $(PROJECT_NAME)_backend coverage report