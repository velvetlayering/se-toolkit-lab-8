# Multi-stage build for nanobot agent
# Follows same pattern as backend/Dockerfile

# ---
# Stage 1: build the application in the `/app` directory.
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, use system interpreter
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY --from=workspace pyproject.toml uv.lock /app/
COPY --from=workspace mcp/ /app/mcp/
COPY --from=workspace nanobot-websocket-channel/ /app/nanobot-websocket-channel/
COPY pyproject.toml /app/nanobot/pyproject.toml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# ---
# Stage 2: use a final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Declare build args for this stage
ARG APP_UID=999
ARG APP_GID=999

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Setup a non-root user with configurable UID/GID
RUN groupadd --system --gid ${APP_GID} nonroot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot

# Copy the application from the builder
COPY --from=builder /app /app

# Fix permissions on workspace directory before switching to nonroot
RUN chown -R nonroot:nonroot /app/nanobot/workspace

# Place executables in the environment at the front of the path
ENV PATH="/app/nanobot/.venv/bin:$PATH"

# Use the non-root user to run our application
USER nonroot

# Use `/app/nanobot` as the working directory
WORKDIR /app/nanobot

# Run the nanobot entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
