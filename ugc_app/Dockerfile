FROM python:3.10

WORKDIR /usr/src/ugc_app

COPY requirements.txt /usr/src/ugc_app

RUN pip3 install --upgrade pip && \
    pip3 install -r /usr/src/ugc_app/requirements.txt --no-cache-dir

COPY . /usr/src/ugc_app

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

