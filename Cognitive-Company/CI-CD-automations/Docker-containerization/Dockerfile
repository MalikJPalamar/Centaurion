# Centaurion Base Docker Image

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4

# Copy the build context (this directory) into /app
COPY . .

EXPOSE 8000

# Default command
CMD ["python", "main.py"]
