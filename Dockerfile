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

# Copy entire project
COPY . .

# Create instance directory for SQLite database
RUN mkdir -p instance

# Set port
ENV PORT=8080

# Use simple Python startup script
CMD ["python", "start.py"]
