DUMP_PATH ?= ~/db_dumps/plm_development_clean_snapshots.pgdump
TEST_PATH := test/

.SILENT: 

.env:
	echo "Creating .env file... modify it to your needs"
	cp .env.example .env

.PHONY:

run:
	docker compose up

build: .env
	docker compose build

format:
	docker compose exec api black .

lint: format
	docker compose exec api ruff check --fix .
	docker compose exec api mypy .

test:
	docker compose run api docker/dockertest.sh

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
=======
	rm -rf .coverage

load_db :
	docker compose exec database dropdb --if-exists -U postgres plm_development
	docker compose exec database createdb -U postgres plm_development
	docker compose exec -T database pg_restore --verbose --clean --no-acl --no-owner -U postgres -d plm_development < $(DUMP_PATH)

.env:
	@echo "Creating .env file... modify it to your needs"
	cp .env.example .env
