# API template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Running locally

If you wish to run the api locally you need to set up the `.env` file in the root of your project, build the docker image from `local/Dockerfile` and start the docker container with `local/docker-compose.yml`. **Please note** that the docker files from the root of the project are not for local deployment.

However, `startproject.py` conveniently does most of the work for you, using values from `.env.local`. To start your project simply run `python3 startproject.py your_project_name`.

If you wish to use different values for your local environment, `.env.template` has all the necessary values that you need to set up.
