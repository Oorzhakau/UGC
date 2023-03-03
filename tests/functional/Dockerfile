FROM python:3.10

RUN useradd --create-home userapi
WORKDIR /usr/src/

COPY ./poetry.lock .
COPY ./pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip  \
    && pip install poetry

COPY . /usr/src/

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/ugc_app/"