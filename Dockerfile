# -------------------------------- base image --------------------------------
FROM python:3.9-slim as python-base

# set environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="${PATH}:/root/.poetry/bin" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# ------------------------------- builder image -------------------------------
FROM python-base as builder-base

# Getting packages from apt
RUN apt update -y && apt install curl python3-opencv make -y

# Copying poetry config file
WORKDIR $PYSETUP_PATH

# POETRY
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_HOME python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create true

COPY pyproject.toml $PYSETUP_PATH
COPY poetry.lock $PYSETUP_PATH
RUN poetry install --no-dev --no-root

# ----------------------------- Development image -----------------------------
FROM builder-base as development

# Installing development dependencies
RUN poetry install --no-root

WORKDIR /app
COPY . /app

# Starting uvicorn
CMD uvicorn explicit_content_api.main:app --host 0.0.0.0 --port 80 --reload --log-level ${LOG_LEVEL}

# ----------------------------- production image -----------------------------
FROM python-base as production

# copy installed python packages from builder image
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /app

COPY ./explicit_content_api /app/explicit_content_api

# Starting uvicorn
# CMD sleep infinity
CMD uvicorn explicit_content_api.main:app --host 0.0.0.0 --port 80 --log-level ${LOG_LEVEL}
