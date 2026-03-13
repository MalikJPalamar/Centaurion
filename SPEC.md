# Centaurion - AI-Driven Cognitive Operating System

## Project Specification

### 1. Project Overview

**Project Name:** Centaurion  
**Type:** Full-stack Web Application (Dashboard)  
**Core Functionality:** AI-driven command center for business operations, market intelligence, and CI/CD automation  
**Target Users:** Business operators, data analysts, DevOps engineers, AI/ML practitioners

---

### 2. UI/UX Specification

#### Layout Structure

**Page Sections:**
- **Navigation Sidebar** (fixed left, 280px width)
  - Logo & branding
  - Main navigation links
  - System status indicators
  - User profile section
  
- **Top Header Bar** (fixed, 64px height)
  - Page title / breadcrumbs
  - Search bar
  - Notifications bell
  - Quick actions
  
- **Main Content Area** (scrollable)
  - Dashboard grid
  - Module cards
  - Data visualizations
  
- **Command Palette** (overlay, triggered by Cmd+K)
  - Quick navigation
  - Command execution

**Responsive Breakpoints:**
- Desktop: 1440px+ (full sidebar)
- Laptop: 1024px-1439px (collapsed sidebar icons)
- Tablet: 768px-1023px (hamburger menu)
- Mobile: <768px (bottom nav)

#### Visual Design

**Color Palette:**
```css
--bg-primary: #0a0a0f;        /* Deep obsidian */
--bg-secondary: #12121a;       /* Card backgrounds */
--bg-tertiary: #1a1a24;       /* Elevated surfaces */
--bg-hover: #22222e;          /* Hover states */

--accent-gold: #c9a227;       /* Primary accent - centurion gold */
--accent-gold-light: #e8c547; /* Gold highlight */
--accent-gold-dark: #8b7015;  /* Gold shadow */

--accent-crimson: #8b2635;    /* Danger/alert */
--accent-emerald: #1a5f4a;    /* Success */
--accent-azure: #1e4d7b;      /* Info/links */

--text-primary: #f5f5f7;      /* Main text */
--text-secondary: #a0a0b0;     /* Muted text */
--text-tertiary: #606070;     /* Disabled text */

--border-subtle: #2a2a36;      /* Subtle borders */
--border-glow: rgba(201, 162, 39, 0.3); /* Gold glow */
```

**Typography:**
- **Display Font:** "Cinzel" (Google Fonts) - headings, logo
- **Heading Font:** "Sora" (Google Fonts) - section titles
- **Body Font:** "IBM Plex Sans" (Google Fonts) - body text, UI
- **Mono Font:** "JetBrains Mono" - code, metrics, data

**Font Sizes:**
- Display: 48px / 3rem
- H1: 32px / 2rem
- H2: 24px / 1.5rem
- H3: 20px / 1.25rem
- Body: 16px / 1rem
- Small: 14px / 0.875rem
- Caption: 12px / 0.75rem

**Spacing System:**
- Base unit: 4px
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

**Visual Effects:**
- Card shadows: `0 4px 24px rgba(0, 0, 0, 0.4)`
- Gold glow on hover: `0 0 20px rgba(201, 162, 39, 0.2)`
- Glassmorphism on modals: `backdrop-filter: blur(12px)`
- Subtle grain texture overlay on backgrounds
- Border gradients on active elements

#### Components

**Navigation Item:**
- States: default, hover, active, disabled
- Icon + label layout
- Gold accent bar on active
- Smooth 200ms transitions

**Dashboard Card:**
- Rounded corners: 16px
- Subtle border: 1px solid var(--border-subtle)
- Hover: slight lift + gold glow
- Header with icon + title
- Content area with padding

**Metric Card:**
- Large number display (JetBrains Mono)
- Label below
- Trend indicator (up/down arrow with percentage)
- Subtle background gradient

**Status Badge:**
- Pill shape
- Color-coded: success (emerald), warning (gold), error (crimson), info (azure)
- Small dot indicator

**Button Variants:**
- Primary: Gold background, dark text
- Secondary: Transparent, gold border
- Ghost: No border, text only
- Danger: Crimson background

**Data Table:**
- Striped rows (alternating bg)
- Sortable column headers
- Row hover highlight
- Pagination controls

---

### 3. Functionality Specification

#### Core Features

**1. Dashboard (Home)**
- System status overview (4 key metrics)
- Recent activity feed
- Quick action buttons
- AI operations summary
- Market intelligence snapshot

**2. AI Operations Module**
- List of active AI tasks
- Task creation form
- Real-time status updates
- Task history/logs

**3. Market Intelligence Module**
- Market data dashboard
- Report generation interface
- Data visualization charts
- Export capabilities

**4. CI/CD Automation Module**
- Pipeline status overview
- Recent deployments
- Health monitoring status
- Trigger manual runs

**5. Settings**
- API key configuration
- Theme preferences
- Notification settings
- User profile

#### API Endpoints (FastAPI Backend)

```
GET    /api/health              - Health check
GET    /api/dashboard/stats     - Dashboard statistics
GET    /api/ai-operations      - List AI operations
POST   /api/ai-operations      - Create new operation
GET    /api/ai-operations/{id}  - Get operation details
GET    /api/market/intelligence - Get market data
POST   /api/market/generate     - Generate report
GET    /api/cicd/pipelines      - List pipelines
POST   /api/cicd/trigger       - Trigger pipeline
GET    /api/cicd/health        - Health status
GET    /api/settings            - Get settings
PUT    /api/settings            - Update settings
```

#### User Interactions

- Sidebar navigation between modules
- Click cards to view details
- Form submissions for creating operations
- Real-time status polling (every 5 seconds)
- Keyboard shortcuts (Cmd+K for palette)
- Toast notifications for actions

#### Data Handling

- Mock data for initial implementation
- LocalStorage for settings persistence
- Simulated API responses with delays

---

### 4. Technical Stack

**Frontend:**
- React 18 with TypeScript
- Vite for build tooling
- React Router for navigation
- Framer Motion for animations
- Recharts for data visualization
- Lucide React for icons
- CSS Modules + CSS Variables

**Backend:**
- FastAPI (Python)
- Pydantic for validation
- Uvicorn for ASGI server
- CORS enabled
- Mock data layer

**Deployment:**
- Render.com (web service)
- Docker support
- Environment variables for config

---

### 5. Acceptance Criteria

**Visual Checkpoints:**
- [ ] Dark theme with gold accents renders correctly
- [ ] Cinzel font displays for logo/headings
- [ ] Sidebar navigation is functional
- [ ] Dashboard cards display with proper styling
- [ ] Hover effects work on interactive elements
- [ ] Responsive layout works at all breakpoints

**Functional Checkpoints:**
- [ ] All navigation routes work
- [ ] Dashboard displays mock statistics
- [ ] AI Operations page shows list
- [ ] Market Intelligence page displays data
- [ ] CI/CD page shows pipeline status
- [ ] Settings page saves to localStorage
- [ ] Backend API endpoints return valid responses
- [ ] Health check passes

**Performance:**
- [ ] Initial load under 3 seconds
- [ ] Smooth animations (60fps)
- [ ] No console errors

---

### 6. File Structure

```
Centaurion/
├── SPEC.md
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── api/
│   │   ├── routes.py       # API endpoints
│   │   └── mock_data.py    # Mock data layer
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css       # Global styles
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   ├── Dashboard/
│   │   │   ├── AIOperations/
│   │   │   ├── MarketIntelligence/
│   │   │   ├── Cicd/
│   │   │   └── Settings/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types/
│   └── public/
├── docker-compose.yml
├── Dockerfile
├── render.yaml
└── README.md
```
