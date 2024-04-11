#!/bin/bash

tries=5
while ! alembic upgrade head; do
    tries=$(($tries-1))
    if [ $tries == 0 ]; then
        echo "Couldn't apply migrations, exiting"
        exit 1
    fi
    echo "Migration failed, retrying in 5 seconds"
    sleep 5
done

uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
