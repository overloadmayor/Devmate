FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock* .

RUN pip install --no-cache-dir uv
RUN uv sync

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run python src/devmate/mcp/server.py & uv run python main.py"]
