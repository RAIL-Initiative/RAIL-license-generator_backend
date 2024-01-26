FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra -y

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
