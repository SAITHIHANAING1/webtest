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
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy SafeStep directory to app root (flatten structure)
COPY SafeStep/ .

# Create instance directory for SQLite database with proper permissions
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Create a writable data directory for SQLite
RUN mkdir -p /app/data && chmod 777 /app/data

# Set port
ENV PORT=8080

# Use wsgi.py for production
CMD ["python", "wsgi.py"]
