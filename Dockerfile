FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
COPY SafeStep/ /app
ENV PORT=8080
CMD exec gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120
