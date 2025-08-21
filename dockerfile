FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install -U pip setuptools wheel \
 && python -m pip install ".[dev]" \
 && python -m pip install playwright

RUN python -m playwright install --with-deps chromium

CMD ["pytest", "-q]
