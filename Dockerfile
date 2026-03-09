FROM  python:3.14-trixie

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

WORKDIR /app
RUN uv sync --locked

COPY . .

CMD []
