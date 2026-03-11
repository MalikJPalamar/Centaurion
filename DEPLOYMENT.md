# Centaurion Deployment Guide

## Quick Deploy (Docker)

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

1. **Clone the repo**
```bash
git clone https://github.com/MalikJPalamar/Centaurion.git
cd Centaurion
```

2. **Configure environment**
```bash
# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

3. **Deploy**
```bash
cd Cognitive-Company/CI-CD-automations/Docker-containerization
docker-compose up -d
```

4. **Check status**
```bash
docker-compose ps
docker-compose logs -f
```

---

## Deploy without Docker (Manual)

### Prerequisites
- Python 3.11+
- Node.js (for some tools)

### Steps

1. **Clone and install**
```bash
git clone https://github.com/MalikJPalamar/Centaurion.git
cd Centaurion
pip install -r requirements.txt
```

2. **Configure**
```bash
cp .env.example .env
# Edit with your settings
```

3. **Run**
```bash
python main.py
```

---

## Deploy to Cloud

### Option 1: Render.com
1. Connect GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python main.py`

### Option 2: Railway
1. Connect GitHub repo
2. Auto-detects Dockerfile

### Option 3: DigitalOcean App Platform
1. Connect GitHub repo
2. Choose Docker container

---

## Current Services

| Service | Port | Purpose |
|---------|------|---------|
| Centaurion | 8000 | Main AI framework |
| Prometheus | 9090 | Monitoring |

---

## Next Steps After Deploy

1. Add your API keys to .env
2. Configure market intelligence sources
3. Set up cron jobs for social listening
4. Enable health monitoring

---

*For more details, see CI-CD-automations/README.md*
