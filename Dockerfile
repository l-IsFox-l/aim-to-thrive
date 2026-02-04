FROM python:3.14-slim

# Install system dependencies including PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1

RUN uv sync --frozen --no-cache

# Copy entrypoint and run the application.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]