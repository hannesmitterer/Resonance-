FROM python:3.11-slim

LABEL maintainer="Hannes Mitterer <hannes@resonance.school>"
LABEL description="Resonance Streaming Pipeline for inter-repository communication"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy streaming pipeline code
COPY streaming/ ./streaming/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Expose WebSocket port
EXPOSE 8765

# Run the streaming pipeline
CMD ["python", "-m", "streaming.pipeline"]
