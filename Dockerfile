FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-install-project

COPY src/ ./src/
COPY main.py ./
COPY config.toml ./

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["sh", "-c", "uv run python -m devmate.mcp.server"]
