FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
