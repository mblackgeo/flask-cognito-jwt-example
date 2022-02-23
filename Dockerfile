FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.1.12

RUN apt-get update && apt-get install -y g++ dumb-init libev-dev && rm -rf /var/lib/apt/lists/*
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

COPY pyproject.toml poetry.lock /src/
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --force-reinstall -r requirements.txt

COPY . /src
WORKDIR /src
RUN pip install .

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python3", "src/webapp/run.bjoern.py"]