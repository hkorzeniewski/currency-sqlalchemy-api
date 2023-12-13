FROM python:3.12.0 as requirements
WORKDIR /tmp

ARG POETRY_VERSION=1.6.1
ENV PATH /root/.local/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python -

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes



FROM python:3.12.0 as server
WORKDIR /code
COPY --from=requirements /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["bash", "-c", "alembic upgrade head && gunicorn -c settings/gunicorn.conf.py app.main:app"]
