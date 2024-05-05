FROM python:3.11

ARG ENV
ENV ENV $ENV

WORKDIR /api

COPY requirements.txt requirements.txt
COPY requirements.dev.txt requirements.dev.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && if [ ${ENV} = "dev" ] ; then pip install --no-cache-dir -r requirements.dev.txt; fi

COPY . .

CMD [ "./docker/entrypoint.sh" ]
