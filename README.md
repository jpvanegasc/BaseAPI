# API template

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project structure

The API can be divided on 3 main components: models & schemas, services, and routers & dependencies, based on the functionalities each component has.

- Models and schemas are meant to be used for DB and data related management. Their main purpose is to define the database structure (models) and provide a tool for validating data through the API (schemas). Please note that they must not handle business logic.

- Services contain the core of the business logic. They are in charge of fetching data from the DB, processing it, and serve it in a way that is useful for the end user. Because a service might be serving multiple endpoints, each with a particular need, try to keep the response unformatted and, if possible, do not raise exceptions within them. Managing these can become an unreadable mess, and this kind of logic is better suited for dependencies.

- Routers manage everything related with receiving requests and returning responses to the user, using the data that is being served by the controller. Any extra processing that goes beyond serializing or raising simple exceptions must be handled by an dependency. This way we ensure that the endpoints are foolproof: endpoints will only fail if the issue is a poorly constructed HTTP connection; any non-HTTP issue encountered can be traced to a faulty controller or dependency.

The project structure is:

```txt
BaseAPI
├── app
│   ├── dependencies
│   │   ├── __init__.py
│   │   └── user.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── common.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   └── user.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── settings.py
│   └── utils.py
├── migrations
│   ├── versions
│   │   └── 2023-06-06_base_migration.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── tests
│   ├── e2e
│   │   └── test_users_flow.py
│   ├── mock
│   │   └── user.json
│   ├── __init__.py
│   ├── client.py
│   ├── conftest.py
│   ├── pytest.ini
│   └── utils.py
├── .env
├── .flake8
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── Makefile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Running locally

If you wish to run the api locally you need to set up the `.env` file in the root of your project, build the docker image from `Dockerfile` and start the docker container with `docker-compose.yml`. The makefile conveniently does this for you running:

1. `make set-up` (if its the first time you run the project)
2. `make server`

