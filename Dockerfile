# AI Sports Commentary Generator - Docker Image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Piper TTS
RUN wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz \
    && tar -xzf piper_amd64.tar.gz \
    && mv piper/piper /usr/local/bin/ \
    && rm -rf piper piper_amd64.tar.gz

# Download Piper voice model
RUN mkdir -p /root/.local/share/piper/models && \
    cd /root/.local/share/piper/models && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directories
RUN mkdir -p output temp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Expose no ports (this is a batch processing app)

# Default command
CMD ["python", "main.py", "--help"]
