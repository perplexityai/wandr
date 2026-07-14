FROM python:3.12.11-slim-trixie@sha256:47ae396f09c1303b8653019811a8498470603d7ffefc29cb07c88f1f8cb3d19f

ARG UV_VERSION=0.8.24

ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_CACHE_DIR=/opt/uv-cache
ENV UV_PROJECT_ENVIRONMENT=/opt/wandr-venv
ENV UV_LINK_MODE=copy
ENV UV_HTTP_TIMEOUT=120
ENV UV_HTTP_RETRIES=8
ENV UV_CONCURRENT_DOWNLOADS=4

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        fonts-liberation \
        libasound2t64 \
        libatk-bridge2.0-0t64 \
        libatk1.0-0t64 \
        libatspi2.0-0t64 \
        libcairo2 \
        libcups2 \
        libdbus-1-3 \
        libdbus-glib-1-2 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0t64 \
        libnss3 \
        libpango-1.0-0 \
        libx11-xcb1 \
        libxcb-shm0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libxshmfence1 \
        libxss1 \
        libxtst6 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir "uv==${UV_VERSION}" camoufox==0.4.11 \
    && test -s /usr/local/bin/uv \
    && uv --version \
    && python -m camoufox fetch

COPY wandr_core_deps/ /opt/wandr_core_deps/

RUN mkdir -p "${UV_CACHE_DIR}" \
    && cd /opt/wandr_core_deps \
    && uv --no-config export --locked --format requirements.txt \
        --no-emit-project \
        --output-file /tmp/wandr-core-public-requirements.txt \
    && python -m venv "${UV_PROJECT_ENVIRONMENT}" \
    && uv --no-config pip install \
        --python "${UV_PROJECT_ENVIRONMENT}/bin/python" \
        --requirements /tmp/wandr-core-public-requirements.txt \
    && rm -f /tmp/wandr-core-public-requirements.txt \
    && chmod -R a+rwX "${UV_CACHE_DIR}" "${UV_PROJECT_ENVIRONMENT}"
