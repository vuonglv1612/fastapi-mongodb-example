FROM python:3.6-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && \
    useradd -u 1612 fastapi && \
    mkdir /app && \
    chown fastapi:fastapi /app

USER fastapi

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .
