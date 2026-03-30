# Lane RFP Agent — Project Plan & Status

## Project Overview

AI-powered tool for freight brokers to optimize the lane bid consolidation process. The core problem: brokers manually compare 100-500 shipping lanes across multiple carrier response spreadsheets to find the lowest rate per lane (4-6 hours per project, ~5x weekly).

## Current Status

**Phase:** Discovery & Proof of Concept
**Timeline:** Sample data incoming in 2 days
**Next Step:** Build working demo with Option 1

---

## Solution Options

### Option 1: Bid Consolidator (MVP)
**Scope:** Spreadsheet consolidation tool only
**User workflow:**
1. Upload multiple carrier response spreadsheets
2. Tool harmonizes formats and matches lanes
3. Compares rates across carriers per lane
4. Picks lowest rate, applies 15% markup
5. Exports final client-ready spreadsheet

**Effort:** 3-5 days
**Deliverable:** Python CLI + optional web UI for file upload

**Features:**
- Automatic column detection and mapping
- Lane harmonization (handle missing lanes, duplicates)
- Rate comparison matrix
- Carrier winner tagging
- Configurable markup percentage
- Final spreadsheet generation
- Carrier comparison report

**Tech Stack:**
- Python (pandas, openpyxl)
- Optional: Flask/FastAPI for web UI
- Excel/CSV processing

---

### Option 2: Bid Automation Suite
**Scope:** Option 1 + carrier outreach & response collection
**User workflow:**
1. Create project with carrier list
2. Upload client spreadsheet
3. One-click distribution (email/SMS to carriers)
4. Tool monitors inbox for responses
5. Auto-downloads and parses returned files
6. Response tracking dashboard
7. Auto-consolidates as rates come in
8. Manual "stop waiting" trigger
9. Final spreadsheet exported

**Effort:** 2-3 weeks
**Deliverable:** Full web application

**New Features:**
- Carrier contact management
- Automated email/SMS distribution
- Email attachment parsing & auto-download
- Inbox monitoring (via Microsoft Graph API)
- Response tracking dashboard
- Non-responsive carrier reminders
- Real-time consolidation as responses arrive

**Tech Stack:**
- Backend: Python/Node.js + job queue (Celery/Bull)
- Frontend: React/Vue
- Email: Microsoft Graph API (Outlook)
- SMS: Twilio
- Database: PostgreSQL

---

### Option 3: Full RFP Agent
**Scope:** Option 1 + Option 2 + AI analysis, history, portal, & carrier scoring
**User workflow:**
1. (All of Option 2)
2. Client submits spreadsheet via branded portal
3. Real-time status updates for client
4. AI rate analysis (outlier detection, market comparison)
5. Carrier performance scoring
6. Historical rate trending
7. Final spreadsheet + insights delivered through portal

**Effort:** 4-6 weeks
**Deliverable:** Enterprise SaaS application

**New Features:**
- Client portal (multi-tenant)
- AI rate analysis (Claude API)
- Historical rate database
- Market rate comparisons
- Carrier performance scoring
- Trend analysis & forecasting
- Negotiation recommendations
- Admin dashboard

**Tech Stack:**
- Backend: Python/Node.js + job queue
- Frontend: Next.js (multi-tenant)
- Database: PostgreSQL
- AI: Claude API
- Auth: OAuth 2.0
- Hosting: AWS/Vercel

---

## Technical Implementation Details

### Core Technologies & Libraries

**Option 1 — Bid Consolidator:**
- **Data Processing:** Python 3.10+, pandas, openpyxl
- **File Handling:** Excel (.xlsx, .csv), fuzzy matching for lane comparison
- **Output:** openpyxl for formatted Excel generation
- **Deployment:** Python CLI or Flask/FastAPI microservice

**Recommended libraries:**
- `pandas` — data frame operations, rate comparison, aggregation
- `openpyxl` — read/write Excel with formatting
- `fuzzywuzzy` — fuzzy string matching for lane names across different formats
- `click` or `typer` — CLI interface
- `pydantic` — data validation

**Option 2 — Bid Automation Suite:**
- All of Option 1 +
- **Email Integration:** Microsoft Graph API (via Outlook MCP)
- **Task Queue:** Celery (Redis backend) for monitoring inbox
- **Backend:** FastAPI or Django
- **Frontend:** React or Vue
- **Database:** PostgreSQL
- **Job Scheduling:** APScheduler or Celery Beat

**Option 3 — Full RFP Agent:**
- All of Option 1 & 2 +
- **AI Analysis:** Claude API (Anthropic SDK)
- **Frontend Framework:** Next.js (multi-tenant)
- **Hosting:** Vercel (frontend) + AWS (backend)
- **Authentication:** Auth0 or Firebase
- **Analytics:** PostHog or Mixpanel

### Reference Implementations

**Excel Consolidation:**
- [Excel Compare Tool (GitHub)](https://github.com/rjshanahan/Excel_Compare_Tool)
- [Compare Excel Files (GitHub)](https://github.com/sannypatel/compare-excel-files)
- [Python Pandas Excel Automation (GitHub)](https://github.com/shardul-bhakta/python-pandas-excel-automation)

**Pandas & OpenPyXL Guides:**
- [Real Python — openpyxl Guide](https://realpython.com/openpyxl-excel-spreadsheets-python/)
- [DataCamp — openpyxl Tutorial](https://www.datacamp.com/tutorial/openpyxl)
- [pandas.read_excel Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)

---

## Implementation Roadmap

### Phase 1: Option 1 (Proof of Concept)
**Duration:** 1 week
**Goal:** Working demo with real client data
**Deliverables:**
- Functional consolidation engine
- Sample output spreadsheet
- Documentation

### Phase 2: Option 1 (Production)
**Duration:** 1-2 weeks
**Goal:** Polished tool ready for regular use
**Deliverables:**
- Web UI for file upload
- Error handling & edge cases
- User guide

### Phase 3: Option 2
**Duration:** 2-3 weeks
**Goal:** Fully automated outreach & collection
**Deliverables:**
- Carrier management system
- Email/SMS distribution
- Response tracking dashboard
- Integration with Option 1

### Phase 4: Option 3
**Duration:** 3-4 weeks
**Goal:** Enterprise-grade SaaS
**Deliverables:**
- Client portal
- AI analysis engine
- Carrier scoring system
- Historical reporting

---

## Key Decisions

- **Start with Option 1:** Solves 80% of the pain with 20% of the effort
- **AI integration:** Claude API for rate analysis and anomaly detection
- **Communication:** Email primary (Microsoft Graph), SMS secondary (Twilio)
- **Multi-tenant ready:** Portal should support multiple brokers from day one

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Carrier spreadsheet formats vary wildly | Build flexible column mapping + user-defined rules |
| Email parsing fragility | Fallback to manual upload, clear user guidance |
| Historical data collection | Start collecting from day one, even if not used until later |
| Scope creep to Option 3 | Deliver Option 1 first, get feedback before expanding |

---

## Success Metrics

- **Option 1:** Reduces consolidation time from 4-6 hours → 15 minutes
- **Option 2:** Reduces total bid cycle time by 50%
- **Option 3:** Enables brokers to handle 2x more bids per week

---

## Dependencies

- Client sample data (ETA: 2 days)
- Microsoft Graph API access (✓ configured)
- Twilio account (for Option 2+)
- Claude API key (for Option 3)
