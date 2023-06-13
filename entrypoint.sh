#!/bin/bash

echo "Applying database migrations"
tries=5

while ! alembic upgrade head; do
    echo "Retrying in 5 seconds"
    sleep 5
    tries=$(($tries-1))
    if [ $tries == 0 ]; then
        echo "ERROR: failed running migrations, exhausted retries"
        exit 1
    fi
done

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload