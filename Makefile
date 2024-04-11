# .SILENT: 
.PHONY:

run: build
	docker compose up

build:
	docker compose build

format:
	docker compose exec backend black .

lint: format
	docker compose exec backend ruff check --fix .

type-check:
	docker compose exec backend mypy .

test:
	docker compose run backend docker/dockertest.sh

clean:
	rm -rf .ruff_cache
	rm -rf **/.ruff_cache
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf **/__pycache__
	rm -rf .pytest_cache

.env:
	@echo "Creating .env file... modify it to your needs"
	cp .env.example .env