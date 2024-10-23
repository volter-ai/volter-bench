FROM --platform=linux/amd64 python:3.11-slim-buster AS builder

# Define build argument for the CodeArtifact token
ARG CODEARTIFACT_TOKEN

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry==1.7.1
RUN pip install uv

WORKDIR /code

COPY pyproject.toml poetry.lock ./

# Configure Poetry to use the CodeArtifact repository with the token
RUN poetry config repositories.codeartifact https://volter-533267259204.d.codeartifact.us-west-2.amazonaws.com/pypi/volter-pypi/simple/
RUN poetry config pypi-token.codeartifact $CODEARTIFACT_TOKEN
RUN poetry config http-basic.codeartifact aws $CODEARTIFACT_TOKEN

RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Runtime image
FROM --platform=linux/amd64 python:3.11-slim-buster AS runtime

ARG CODEARTIFACT_TOKEN

WORKDIR /code

ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH" \
    PYTHONPATH=/code

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN pip install uv
# Install required packages using pip
RUN uv pip install --extra-index-url https://aws:$CODEARTIFACT_TOKEN@volter-533267259204.d.codeartifact.us-west-2.amazonaws.com/pypi/volter-pypi/simple/ mini-game-engine
RUN uv pip install --extra-index-url https://aws:$CODEARTIFACT_TOKEN@volter-533267259204.d.codeartifact.us-west-2.amazonaws.com/pypi/volter-pypi/simple/ volter-common

COPY start.py .
COPY main_game ./main_game
COPY assets ./assets
COPY log_conf.yaml .

CMD ["python", "start.py"]