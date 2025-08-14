FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY SafeStep/ /app/

# Create instance directory for SQLite database
RUN mkdir -p /app/instance

# Set port
ENV PORT=8080

# Use array syntax for CMD to avoid shell issues
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080", "--workers", "3", "--threads", "8", "--timeout", "120"]
