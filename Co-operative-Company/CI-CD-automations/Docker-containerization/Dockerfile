# Centaurion Base Docker Image

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    playwright

# Copy application files
COPY . .

# Default command
CMD ["python", "main.py"]
