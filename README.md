# API template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Running locally

If you wish to run the api locally you need to set up the `.env` file in the root of your project, build the docker image from `local/Dockerfile` and start the docker container with `local/docker-compose.yml`. **Please note** that the docker files from the root of the project are not for local deployment.

However, `startproject.py` conveniently does most of the work for you, using values from `.env.local`. To start your project simply run `python3 startproject.py your_project_name`.

If you wish to use different values for your local environment, `.env.template` has all the necessary values that you need to set up.

## Deploying

The project is deployed via serverless to an AWS Lambda, using an AWS ECR image. In order to deploy this project you need to set up previously the AWS account that will be used to make the deploy, making sure that it can execute Lambdas, as well as being able to push and pull from the ECR repo (a simple way of ensuring this is giving your user administrator access). Make sure to export the user's access and secret keys so that the serverless CLI uses the correct user.

To start the deploy you will need to set up a `serverless.yml` file in the root of the project, and run `serverless deploy`. If you used `startproject.py`, it will have also created a `serverless.yml` file for you!

If you want to create a `serverless.yml` file from scratch, `serverless.template.yml` provides a good starting point.
