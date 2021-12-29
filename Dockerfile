FROM public.ecr.aws/lambda/python:3.8

ARG FUNCTION_DIR="/var/task"

RUN mkdir -p ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

COPY . ${FUNCTION_DIR}

RUN pip install -r requirements.txt

CMD [ "api.main.handler" ]