FROM python:3.11

ARG ENV

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && if [[ ${ENV} == "dev" ]] ; then pip install --no-cache-dir -r requirements.dev.txt; fi

COPY . .

CMD [ "./docker/entrypoint.sh" ]
