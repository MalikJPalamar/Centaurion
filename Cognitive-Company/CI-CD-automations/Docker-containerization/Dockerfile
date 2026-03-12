# Centaurion Base Docker Image

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4

# Copy all files from repo root
COPY . .

# Default command
CMD ["python", "Cognitive-Company/CI-CD-automations/Docker-containerization/main.py"]
