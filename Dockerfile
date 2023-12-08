FROM python:3.10

ENV POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"  \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . ./

EXPOSE 8000

ENV PYTHONPATH=.

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
