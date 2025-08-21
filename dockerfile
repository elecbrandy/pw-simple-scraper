FROM mcr.microsoft.com/playwright:latest

WORKDIR /app

RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir -U pip setuptools

COPY pyproject.toml ./
RUN python3 -m pip install ".[dev]"

COPY src/ /app/src/
COPY tests/ /app/tests/

CMD ["pytest", "-q"]