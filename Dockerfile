FROM python:3.10-slim

WORKDIR /app


RUN apt update -y \
    && apt install -y build-essential \
    && pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install

COPY . .
COPY scripts/* /scripts/
RUN chmod +x -R /scripts

ENTRYPOINT ["/scripts/dev-entrypoint.sh"]