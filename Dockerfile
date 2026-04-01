FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PORT=8000 \
    WEB_CONCURRENCY=2 \
    TIMEOUT=120

WORKDIR /app

COPY requirements-web.txt /app/requirements-web.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements-web.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "gunicorn webapp.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --workers ${WEB_CONCURRENCY} --timeout ${TIMEOUT}"]
