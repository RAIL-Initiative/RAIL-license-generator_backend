FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    # Required for poetry
    pandoc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra if you want latex support

WORKDIR /app/

# Install Poetry
RUN pip install poetry && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
ENV PYTHONPATH=/app
