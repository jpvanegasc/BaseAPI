FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
