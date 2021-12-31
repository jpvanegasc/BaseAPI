# API template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project structure

The API can be divided on 3 main components: models & schemas, controllers and routers & utils, based on the functionalities each component has.

* Models and schemas are meant to be used for DB and data related management. Their main purpose is to define the database structure (models) and provide a tool for validating data through the API. They must not handle business logic.

* Controllers contain the core of the business logic. They are in charge of fetching data from the DB, processing it, and serve it in a way that is useful for the end user. Because a controller might be serving multiple endpoints, each with a particular need, try to keep the response unformatted and, if possible, do not raise exceptions within them. Managing these can become an unreadable mess, and this kind of logic is better suited for utils.

* Routers manage everything related with receiving requests and returning responses to the user, using the data that is being served by the controller. Any extra processing that goes beyond serializing or raising simple exceptions must be handled by an util. This way we ensure that the endpoints are foolproof: endpoints will only fail if the issue is a poorly constructed HTTP connection; any non-HTTP issue encountered can be traced to a faulty controller or util.

It is worth mentioning that the core itself of the API resides in the common folder. Any internal configuration that is not related to the project in particular but with the API as a whole should be stored in here.

## Running locally

If you wish to run the api locally you need to set up the `.env` file in the root of your project, build the docker image from `local/Dockerfile` and start the docker container with `docker-compose-local.yml`. **Please note** that the dockerfile from the root of the project is not for local deployment.

However, `startproject.py` conveniently does most of the work for you, using values from `.env.local`. To start your project simply run `python3 startproject.py your_project_name`. If you wish to use different values for your local environment, `.env.template` has all the necessary values that you need to set up.

After the docker container is running, enter the container command line via `docker exec -it your_project_name_backend /bin/bash` and start the local server with `uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload`.

## Deploying

The project is deployed via serverless to an AWS Lambda, using an AWS ECR image. In order to deploy this project you need to set up previously the AWS account that will be used to make the deploy, making sure that it can execute Lambdas, as well as being able to push and pull from the ECR repo (a simple way of ensuring this is giving your user administrator access). Make sure to export the user's access and secret keys so that the serverless CLI uses the correct user.

To start the deploy you will need to set up a `serverless.yml` file in the root of the project, and run `serverless deploy`. If you used `startproject.py`, it will have also created a `serverless.yml` file for you!

If you want to create a `serverless.yml` file from scratch, `serverless.template.yml` provides a good starting point.
