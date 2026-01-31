# ===============================
# Base image
# ===============================
FROM python:3.7

# ===============================
# Environment
# ===============================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app \
    C_FORCE_ROOT=1

WORKDIR /app

# ===============================
# System dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Install Poetry
# ===============================
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# ===============================
# Copy dependency files
# ===============================
COPY app/pyproject.toml app/poetry.lock* /app/

# ===============================
# Install dependencies
# ===============================
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then \
        poetry install --no-root; \
    else \
        poetry install --no-root --no-dev; \
    fi

# ===============================
# Optional: JupyterLab
# ===============================
ARG INSTALL_JUPYTER=false
RUN if [ "$INSTALL_JUPYTER" = "true" ]; then \
        pip install --no-cache-dir jupyterlab; \
    fi

# ===============================
# Copy application and entrypoint
# ===============================
COPY app /app
COPY app/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh

# ===============================
# Entrypoint
# ===============================
CMD ["/worker-start.s]()
