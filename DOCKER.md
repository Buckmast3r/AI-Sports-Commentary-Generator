# Docker Usage Guide

This guide shows how to use Docker to run the AI Sports Commentary Generator.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Get Docker Compose](https://docs.docker.com/compose/install/))

## Quick Start with Docker Compose

### 1. Setup Configuration
```bash
# Copy example config
cp config.example.json config.json

# Edit if needed
nano config.json
```

### 2. Build and Run
```bash
# Build the image and start services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This will:
- Start Ollama service
- Pull llama2 model
- Build the generator image
- Run the generator once

### 3. Check Output
```bash
# Videos will be in the output directory
ls -lh output/

# View logs
docker-compose logs generator
```

### 4. Run Again
```bash
# Generate another video
docker-compose run --rm generator python main.py

# With custom avatar
docker-compose run --rm generator python main.py --avatar /app/my_avatar.jpg

# Upload to YouTube
docker-compose run --rm generator python main.py --upload
```

### 5. Cleanup
```bash
# Stop services
docker-compose down

# Remove volumes (including Ollama data)
docker-compose down -v
```

## Using Standalone Docker

### Build the Image
```bash
docker build -t sports-commentary-generator .
```

### Run with External Ollama
If you have Ollama running on your host:

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/config.json:/app/config.json:ro \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  sports-commentary-generator \
  python main.py
```

### Run with Docker Network
Connect to Ollama in another container:

```bash
# Create network
docker network create sports-net

# Run Ollama
docker run -d \
  --name ollama \
  --network sports-net \
  -v ollama_data:/root/.ollama \
  ollama/ollama:latest

# Pull model
docker exec ollama ollama pull llama2

# Run generator
docker run --rm \
  --network sports-net \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/config.json:/app/config.json:ro \
  -e OLLAMA_HOST=http://ollama:11434 \
  sports-commentary-generator \
  python main.py
```

## Scheduled Runs with Docker

### Using Cron
Add to host's crontab:

```bash
# Generate daily at 9 AM
0 9 * * * cd /path/to/project && docker-compose run --rm generator python main.py --upload >> cron.log 2>&1
```

### Using Docker with restart policy
Create a service that runs periodically:

```yaml
# In docker-compose.yml
generator:
  # ... other config ...
  command: >
    bash -c "while true; do 
      python main.py --upload; 
      sleep 86400;  # 24 hours
    done"
  restart: always
```

## YouTube Authentication in Docker

For YouTube uploads, you need to handle OAuth:

### Option 1: Pre-authenticate
```bash
# Run once on host to authenticate
python main.py --upload

# Copy token to project
# Now Docker can use it
docker-compose run --rm \
  -v $(pwd)/token.pickle:/app/token.pickle \
  generator python main.py --upload
```

### Option 2: Interactive Authentication
```bash
# Run with port forwarding for OAuth callback
docker-compose run --rm \
  -p 8080:8080 \
  generator python main.py --upload
```

## Troubleshooting

### Ollama Connection Failed
```bash
# Check if Ollama is running
docker-compose ps

# View Ollama logs
docker-compose logs ollama

# Test connection
docker-compose run --rm generator \
  curl http://ollama:11434/api/tags
```

### Permission Issues with Output
```bash
# Fix permissions on output directory
sudo chown -R $USER:$USER output/

# Or run with user
docker-compose run --rm --user $(id -u):$(id -g) generator python main.py
```

### Out of Memory
```bash
# Increase Docker memory limit
# In Docker Desktop: Settings → Resources → Memory

# Or limit container memory
docker-compose run --rm -m 4g generator python main.py
```

## Production Deployment

### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml sports-commentary
```

### Using Kubernetes
See example Kubernetes manifests in `k8s/` directory (if available).

## Custom Dockerfile

### Add Custom Dependencies
```dockerfile
# Add to Dockerfile
RUN pip install custom-package

# Rebuild
docker-compose build --no-cache
```

### Use Different Python Version
```dockerfile
# Change base image
FROM python:3.10-slim
```

## Environment Variables

Available environment variables:

- `OLLAMA_HOST`: Ollama server URL (default: http://ollama:11434)
- `PYTHONUNBUFFERED`: Set to 1 for real-time logs

Example:
```bash
docker-compose run --rm \
  -e OLLAMA_HOST=http://custom-ollama:11434 \
  generator python main.py
```

## Volume Mounts

Persistent data locations:

- `./output:/app/output` - Generated videos
- `./temp:/app/temp` - Temporary files
- `./config.json:/app/config.json` - Configuration
- `ollama_data` - Ollama models (named volume)

## Tips

1. **Cache Models**: Use named volume for Ollama to avoid re-downloading
2. **Separate Concerns**: Run Ollama separately for better resource management
3. **Monitor Logs**: Use `docker-compose logs -f` to watch progress
4. **Cleanup**: Regularly clean up old videos and temp files
5. **Backup**: Backup `ollama_data` volume if you customize models

## Resources

- Docker Hub: https://hub.docker.com/
- Ollama Docker: https://hub.docker.com/r/ollama/ollama
- Docker Compose Docs: https://docs.docker.com/compose/
