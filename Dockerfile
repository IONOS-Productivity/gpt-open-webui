# syntax=docker/dockerfile:1
# Initialize device type args
# use build args in the docker build command with --build-arg="BUILDARG=true"

ARG BUILD_HASH=dev-build

######## WebUI frontend ########
FROM --platform=$BUILDPLATFORM node:22-alpine3.20 AS build
ARG BUILD_HASH

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
ENV APP_BUILD_HASH=${BUILD_HASH}
ENV NODE_OPTIONS=--max-old-space-size=3300
RUN npm run build

######## WebUI backend ########
FROM python:3.11-slim-bookworm AS base

## Basis ##
ENV ENV=prod \
    PORT=8080

# Disable tracking by library "unstructrured": SCARF_NO_ANALYTICS, DO_NOT_TRACK
ENV SCARF_NO_ANALYTICS=true \
    DO_NOT_TRACK=true

WORKDIR /app/backend

ENV HOME=/root

RUN apt-get update && \
    # Install pandoc, netcat and gcc
    apt-get install -y --no-install-recommends git build-essential pandoc gcc netcat-openbsd curl jq && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    # for RAG OCR
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
    # cleanup
    rm -rf /var/lib/apt/lists/*;

# install python dependencies
COPY uv.lock pyproject.toml .

# Make uv sync install dependencies from uv.lock to the
# system packages location, not a virtual environment
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# /root/.cache contains the download cache
RUN pip3 install --no-cache-dir uv && \
    uv sync --locked && \
    rm -rf /root/.cache/

# copy built frontend files
COPY --from=build /app/build /app/build
COPY --from=build /app/CHANGELOG.md /app/CHANGELOG.md
COPY --from=build /app/package.json /app/package.json

# copy backend files
COPY ./backend .

EXPOSE 8080

HEALTHCHECK CMD curl --silent --fail http://localhost:${PORT:-8080}/health | jq -ne 'input.status == true' || exit 1

ARG BUILD_HASH
ENV WEBUI_BUILD_VERSION=${BUILD_HASH}
ENV DOCKER=true

CMD [ "bash", "start.sh"]
