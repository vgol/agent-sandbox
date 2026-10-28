FROM mcr.microsoft.com/devcontainers/base:bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
COPY --from=ovhcom/ovhcloud-cli:v0.16.0 /usr/local/bin/ovhcloud /usr/local/bin/ovhcloud
