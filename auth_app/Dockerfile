FROM python:3.10

RUN useradd --create-home userapi
WORKDIR /usr/src/auth_app

COPY ./poetry.lock .
COPY ./pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip  \
    && pip install poetry

COPY . /usr/src/auth_app
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
