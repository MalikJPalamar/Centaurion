# Centaurion Base Docker Image

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4

# Create app directory structure
RUN mkdir -p /app/Cognitive-Company

# Copy main entry point
COPY main.py /app/

# Copy Framework
COPY ../../../Framework /app/Framework

# Copy Cognitive-Company structure
COPY ../../* /app/Cognitive-Company/

# Default command
CMD ["python", "main.py"]
