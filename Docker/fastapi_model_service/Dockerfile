FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.9

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# RUN poetry config virtualenvs.create false && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY ./app /code/app
COPY ./.env /code/

CMD ["uvicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "80"]