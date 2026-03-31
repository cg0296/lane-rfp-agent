# Repository Structure Guide

This document explains how the Lane RFP Agent repository is organized.

## Quick Overview

```
lane-rfp-agent/
├── README.md              ← Start here! Quick start and overview
├── SETUP.md               ← Detailed setup instructions
├── DEPLOYMENT.md          ← Demo flow and production deployment
├── MVP_COMPLETE.md        ← Summary of what was built
├── README_MVP.md          ← Feature overview
├── CLAUDE.md              ← Code guidelines
│
├── backend/               ← FastAPI server
│   ├── app/
│   │   ├── main.py        (API routes and endpoints)
│   │   ├── config.py      (settings and configuration)
│   │   ├── models.py      (Pydantic data models)
│   │   ├── excel_generator.py
│   │   └── agents/
│   │       └── email_parser.py  (Claude API integration)
│   ├── requirements.txt    (Python dependencies)
│   └── .env.example        (environment template)
│
├── frontend/              ← React app
│   ├── src/
│   │   ├── App.jsx         (main component)
│   │   ├── main.jsx        (entry point)
│   │   └── components/
│   │       ├── EmailParser.jsx
│   │       └── QuoteGenerator.jsx
│   ├── index.html
│   ├── package.json        (Node dependencies)
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── postcss.config.js
│
├── outlook-mcp/           ← Microsoft 365 integration (external tool)
│
└── .planning/             ← Planning & research archive
    ├── README.md          (explains this folder)
    ├── MVP_SPEC.md        (MVP specifications)
    ├── TECH_SPEC.md       (full architecture)
    ├── WORKFLOWS.md       (workflow diagrams)
    ├── PROJECT_*.md       (initial planning)
    ├── specs/             (detailed specs for 3 options)
    ├── Emails/            (client correspondence)
    └── *.pdf              (proposals and PDFs)
```

## What's Where

### 📖 Documentation (Read These First)

| File | Purpose |
|------|---------|
| **README.md** | Project overview, quick start, tech stack |
| **README_MVP.md** | Features, sample email, troubleshooting |
| **SETUP.md** | Detailed setup with API examples |
| **DEPLOYMENT.md** | Demo flow, production deployment |
| **MVP_COMPLETE.md** | What was built, metrics, roadmap |
| **CLAUDE.md** | Code guidelines for development |

### 💻 Active Code

| Folder | Contains |
|--------|----------|
| **backend/** | FastAPI REST API, Claude AI integration, Excel generation |
| **frontend/** | React UI, Vite build, Tailwind styling |

### 📚 Reference & Archive

| Folder | Contains |
|--------|----------|
| **.planning/** | Research, specifications, proposals (read-only reference) |

### 🔌 External

| Folder | Purpose |
|--------|---------|
| **outlook-mcp/** | Microsoft 365 MCP server (not used in MVP, for Phase 2+) |

## File Navigation Guide

### "I want to..."

**...run the app locally**
→ Read `README.md` (Quick Start section)

**...understand what was built**
→ Read `MVP_COMPLETE.md`

**...set up development environment**
→ Read `SETUP.md`

**...prepare for demo to client**
→ Read `DEPLOYMENT.md`

**...understand the architecture**
→ Read `backend/app/main.py` and `TECH_SPEC.md` (in .planning/)

**...modify the UI**
→ Edit `frontend/src/components/`

**...modify the backend API**
→ Edit `backend/app/main.py`

**...add email parsing logic**
→ Edit `backend/app/agents/email_parser.py`

**...change Excel formatting**
→ Edit `backend/app/excel_generator.py`

**...understand the original specifications**
→ Read `.planning/MVP_SPEC.md`

**...see the full technical design**
→ Read `.planning/TECH_SPEC.md`

## Key Decisions

### Why .planning/ is hidden
- Those are research and planning artifacts
- The active codebase is in `backend/` and `frontend/`
- Reference materials are there for context, not for development
- `.gitignore` hides this folder from most operations

### Why separate backend and frontend
- Independent development and deployment
- Backend runs on port 8000 (FastAPI)
- Frontend runs on port 5173 (Vite dev server)
- Can deploy separately or together

### Why SETUP, DEPLOYMENT, MVP_COMPLETE, etc.
- Different audiences need different docs
- SETUP = developers getting started
- DEPLOYMENT = demo and production ops
- MVP_COMPLETE = stakeholders and team leads
- README_MVP = feature overview for users

## Development Workflow

### First Time Setup
1. Read `README.md`
2. Read `SETUP.md` for detailed instructions
3. Run backend: `cd backend && python -m uvicorn app.main:app --reload`
4. Run frontend: `cd frontend && npm run dev`
5. Open http://localhost:5173

### Making Changes
1. Edit code in `backend/` or `frontend/`
2. Changes reload automatically (hot reload enabled)
3. Test in browser
4. Commit to git when ready

### Adding Features
1. Refer to `TECH_SPEC.md` for architecture
2. Add backend endpoint in `backend/app/main.py`
3. Add React component in `frontend/src/components/`
4. Connect them via API calls
5. Test and commit

### Deploying
1. Read `DEPLOYMENT.md`
2. Choose deployment target (Vercel, Railway, etc.)
3. Set environment variables
4. Deploy

## Common Questions

**Q: Where are the tests?**
A: Not in MVP. Add in Phase 2 with database setup.

**Q: Where's the database?**
A: Not needed for MVP. Uses in-memory storage. PostgreSQL schema in `.planning/TECH_SPEC.md` for Phase 2.

**Q: Why is there an outlook-mcp folder?**
A: For future integration (Phase 2+). Currently unused.

**Q: Can I delete .planning?**
A: Don't. It contains original specifications needed for Phase 2 development.

**Q: Where do I add new carriers?**
A: In the UI, or in `backend/app/main.py` DEFAULT_CARRIERS list for testing.

**Q: How do I change the Excel format?**
A: Edit `backend/app/excel_generator.py` - colors, fonts, columns, etc.

## Next Steps

- **Phase 1 (MVP)** ← You are here ✓
- **Phase 2** - Database, email integration, rate consolidation
- **Phase 3** - Client portal, carrier response collection
- **Phase 4** - AI analysis, historical tracking, predictions

See `MVP_COMPLETE.md` for full roadmap.

---

**Last Updated:** March 31, 2026
**Status:** Production-ready MVP
