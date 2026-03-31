# Lane RFP Agent MVP - Ready for Testing

## Overview

This MVP automates the creation of freight quote sheets from unstructured client emails.

**Workflow:**
1. User pastes a client's email request
2. Claude AI parses the email to extract quote details
3. User reviews the parsed data and selects carriers
4. System generates a professional Excel quote sheet
5. User downloads the Excel file

## What's Included

### Backend (FastAPI + Claude API)
✅ Email parsing with Claude API
✅ Quote sheet generation with openpyxl
✅ Carrier management (add/remove/list)
✅ REST API endpoints
✅ CORS enabled for frontend

### Frontend (React + Vite + Tailwind)
✅ Email input with sample loader
✅ Parsed data review & editing
✅ Carrier selection and management
✅ Direct Excel download
✅ Two-step workflow UI

## Quick Start (5 minutes)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anthropic API key (get at https://console.anthropic.com)

### Step 1: Backend Setup

```bash
cd backend

# Copy .env.example to .env and add your Anthropic API key
cp .env.example .env
# Edit .env and set: ANTHROPIC_API_KEY=sk-your-key-here

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload
```

Server runs on: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

### Step 2: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs on: `http://localhost:5173`

### Step 3: Test It!

1. Open `http://localhost:5173` in your browser
2. Click "Load Sample" to load a test email
3. Click "Parse Email"
4. Review the parsed data (should extract origin, destination, equipment, quantity, etc.)
5. Select carriers (default: Carrier A, B, C)
6. Click "Generate & Download Excel"
7. Open the downloaded Excel file in Excel or Google Sheets

## Sample Email (Built-In)

```
Hello Jillian & Michelle,

Could you please quote me for the following –

16x 53'
Los Angeles to Greenville, SC
Team Drivers and Solo
Loading- mid to end April
Insurance $250k per truck

All trucks need e-track throughout
Commodity is Production Equipment (lighting, audio, video etc)

Thanks,
John Smith
```

**Expected Parse Result:**
- Origin: Los Angeles, CA
- Destination: Greenville, SC
- Equipment: 53' Trailer
- Quantity: 16
- Special Requirements: e-track throughout, Insurance $250k per truck, Production Equipment

## Project Structure

```
backend/
├── app/
│   ├── agents/
│   │   └── email_parser.py    # Claude API integration
│   ├── main.py                 # FastAPI app & routes
│   ├── config.py               # Settings
│   ├── models.py               # Pydantic models
│   └── excel_generator.py      # Excel file generation
├── requirements.txt
├── .env.example
└── run.sh                       # Startup script

frontend/
├── src/
│   ├── components/
│   │   ├── EmailParser.jsx     # Email input & parsing
│   │   └── QuoteGenerator.jsx  # Data review & generation
│   ├── App.jsx                  # Main app component
│   └── main.jsx                 # Entry point
└── package.json
```

## API Endpoints

All endpoints are in the built-in Swagger docs at `http://localhost:8000/docs`

### Email Parsing
```
POST /api/parse-email
Request: { "email_text": "...", "client_name": "..." }
Response: { "success": true, "data": {...} }
```

### Quote Generation
```
POST /api/generate-quote-sheet
Request: { "quote_data": {...}, "carriers": [...], "client_name": "..." }
Response: { "success": true, "file_url": "/downloads/...", "filename": "..." }
```

### Downloads
```
GET /api/downloads/{filename}
Returns: Excel file download
```

### Carriers
```
GET /api/carriers                          # List all
POST /api/carriers                         # Add new
DELETE /api/carriers/{id}                  # Remove
```

## Features

### Email Parsing
- Claude AI extracts key information from unstructured emails
- Detects: origin city/state, destination city/state, equipment type, quantity, dates, special requirements
- Confidence score indicates how certain the parse is
- Handles various email formats

### Quote Sheet Generation
- Creates professional Excel files
- One row per unit (qty 16 = 16 rows)
- Carrier columns for rates (ready to fill in)
- Metadata header with client info, loading dates, special requirements
- Professional formatting with borders, colors, column widths

### Carrier Management
- Pre-loaded with 3 sample carriers
- Add/remove carriers on the fly
- Reused across quotes

## Customization

### Change Carriers
Edit the carrier list in `backend/app/main.py`:
```python
DEFAULT_CARRIERS = [
    {"id": 1, "name": "Your Carrier A", "email": "email@carrier.com", "phone": "123-456-7890"},
    # ...
]
```

### Adjust Excel Format
Edit `backend/app/excel_generator.py`:
- Colors: Modify the `PatternFill` objects
- Column widths: Adjust `column_dimensions`
- Fonts: Change `Font` objects

### Change Port
Edit `.env`:
```
PORT=8001  # Instead of 8000
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
# Make sure .env file exists and has your key:
ANTHROPIC_API_KEY=sk-proj-...
```

### "Connection refused on port 8000"
Backend isn't running. In the `backend` folder:
```bash
python -m uvicorn app.main:app --reload
```

### "Connection refused on port 5173"
Frontend isn't running. In the `frontend` folder:
```bash
npm run dev
```

### CORS errors
Make sure `CORS_ORIGINS` in `.env` includes your frontend:
```
CORS_ORIGINS=["http://localhost:5173"]
```

### Excel download doesn't start
- Check that the backend generated the file (check `downloads/` folder)
- Check browser console for errors
- Make sure file URL matches the actual file path

## Next Steps (Phase 2)

- [ ] Database setup (PostgreSQL) for persistence
- [ ] User authentication
- [ ] Quote history
- [ ] Carrier response collection (email/SMS)
- [ ] Rate consolidation & comparison
- [ ] Markup configuration per quote
- [ ] Email integration for auto-sending
- [ ] Client portal

## Demo Notes

**What to Show Nita:**
1. Load sample email
2. Show how it parses automatically (takes ~2 seconds)
3. Show how she can edit any field
4. Show carrier selection
5. Generate Excel
6. Open Excel and show the formatted sheet ready for carrier rates

**Key Selling Points:**
- Eliminates manual spreadsheet creation
- Consistent formatting
- Error-free parsing with Claude AI
- Takes 10 seconds instead of 20-30 minutes per quote
- Easy to customize carriers and format

## Support

For issues or questions, check:
- `SETUP.md` - Detailed setup and API testing guide
- `MVP_SPEC.md` - Full specifications
- `backend/app/main.py` - API implementation
- Backend docs: `http://localhost:8000/docs`

## License

MIT
