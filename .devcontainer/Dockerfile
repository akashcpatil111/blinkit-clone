FROM mcr.microsoft.com/devcontainers/python:0-3.10

# Install MongoDB tools to verify database connections
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends mongodb-clients
