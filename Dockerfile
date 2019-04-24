FROM python:3

RUN pip install pipenv

RUN groupadd -r celery && useradd --no-log-init -r -g celery celery

WORKDIR /app

ENV CELERY_LOGLEVEL info

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

USER celery:celery

ENTRYPOINT celery -A tasks worker --loglevel=$CELERY_LOGLEVEL
