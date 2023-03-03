#!/bin/bash
poetry config virtualenvs.create false &&
poetry install --no-interaction --no-ansi &&
poetry run python db/wait_for_postgres.py &&
poetry run python db/wait_for_redis.py &&
poetry run flask db upgrade &&
poetry run flask createsuperuser $AUTH_ADMIN_USERNAME $AUTH_ADMIN_PASSWORD $AUTH_ADMIN_EMAIL &&
poetry run gunicorn wsgi_app:app --workers 4 --bind 0.0.0.0:5000