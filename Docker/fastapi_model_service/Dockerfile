FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY ../../pyproject.toml ../../poetry.lock ./
COPY ../../.env ./app/.env
COPY ../../src/app ./app

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

CMD ["uvicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "80"]