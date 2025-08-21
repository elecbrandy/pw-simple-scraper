FROM python:3.11-bookworm

WORKDIR /app

RUN python -m pip install -U pip setuptools wheel \
 && python -m pip install ".[dev]" playwright \
 && python -m playwright install --with-deps chromium

CMD ["pytest", "-q"]
