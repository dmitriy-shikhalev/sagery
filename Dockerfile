# BASE
FROM python:3.12-slim as base

WORKDIR /usr/src/app

ARG PYPI_INDEX_URL=https://pypi.python.org/simple
ARG POETRY_VERSION=1.8.2
ARG POETRY_PLUGIN_MIRROR_VERSION=0.4.2

COPY pyproject.toml poetry.lock ./
RUN export PIP_NO_CACHE_DIR=1 && \
    pip install "poetry==$POETRY_VERSION" poetry-plugin-pypi-mirror==${POETRY_PLUGIN_MIRROR_VERSION} && \
    poetry config --local virtualenvs.create false

RUN poetry install --no-root --no-interaction --without dev

COPY ./alembic ./alembic
COPY alembic.ini ./
COPY ./sagery ./sagery

RUN poetry install --without dev --compile

CMD ["echo", "DUMMY"]

# UNIT TESTS
FROM base as unit-tests

RUN pip install "poetry==$POETRY_VERSION" && \
    poetry install --no-root --no-interaction --only dev
COPY ./tests ./tests

CMD pytest
