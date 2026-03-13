# Centaurion Deployment Guide

## Project Structure
The project now includes both frontend and backend:

```
Centaurion/
├── SPEC.md              # Detailed specification
├── backend/             # FastAPI backend
│   ├── main.py         # Application entry point
│   ├── requirements.txt
│   └── api/
│       ├── routes.py   # API endpoints
│       └── mock_data.py
├── frontend/           # React frontend
│   ├── src/
│   │   ├── pages/      # Dashboard, AIOperations, etc.
│   │   ├── App.tsx     # Main app component
│   │   └── index.css   # Global styles
│   └── package.json
├── Dockerfile          # Backend container
└── render.yaml        # Render.com config
```

---

## Deploy to Render.com

### Prerequisites
1. GitHub account
2. Render.com account connected to GitHub

### Steps

1. **Push to GitHub**
   ```bash
   cd Centaurion
   git add .
   git commit -m "Add frontend and backend"
   git push origin main
   ```

2. **Deploy Backend**
   - Go to Render.com Dashboard
   - Create new "Web Service"
   - Connect to GitHub repo
   - Settings:
     - Environment: Python
     - Build Command: `cd backend && pip install -r requirements.txt`
     - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Create

3. **Deploy Frontend**
   - Create new "Static Site" on Render
   - Connect to GitHub repo
   - Settings:
     - Build Command: `cd frontend && npm install && npm run build`
     - Publish Directory: `frontend/dist`
     - Environment Variables:
       - `VITE_API_URL`: Your backend URL (e.g., https://centaurion-backend.onrender.com)
   - Create

---

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
# API available at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| PORT | Server port (default: 8000) | No |
| OPENAI_API_KEY | OpenAI API key | Optional |
| ANTHROPIC_API_KEY | Anthropic API key | Optional |
| MARKET_DATA_API_KEY | Market data provider key | Optional |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/dashboard/stats | Dashboard statistics |
| GET | /api/ai-operations | List AI operations |
| POST | /api/ai-operations | Create operation |
| GET | /api/market/intelligence | Market data |
| POST | /api/market/generate | Generate report |
| GET | /api/cicd/pipelines | List pipelines |
| POST | /api/cicd/trigger | Trigger pipeline |
| GET | /api/cicd/health | Health status |
| GET | /api/settings | Get settings |
| PUT | /api/settings | Update settings |

---

## Design System

The frontend uses a premium Centaurion theme:

- **Colors**: Obsidian dark (#0a0a0f), Centurion Gold (#c9a227)
- **Fonts**: Cinzel (display), Sora (headings), IBM Plex Sans (body), JetBrains Mono (data)
- **Components**: Cards, tables, badges, buttons, forms
- **Animations**: Subtle hover effects, smooth transitions
