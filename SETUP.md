# Lane RFP Agent - Setup & Testing Guide

## Quick Start (Development)

### 1. Backend Setup

```bash
cd backend

# Create .env file from example
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-...

# Install dependencies
pip install -r requirements.txt

# Run server (will start on http://localhost:8000)
python -m uvicorn app.main:app --reload
```

Server will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs` (Swagger UI)

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server (will start on http://localhost:5173)
npm run dev
```

### 3. Test Email Parsing (Backend Only)

Using curl or Postman:

```bash
curl -X POST "http://localhost:8000/api/parse-email" \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Hello Jillian & Michelle,\n\nCould you please quote me for the following –\n\n16x 53'\nLos Angeles to Greenville, SC\nTeam Drivers and Solo\nLoading- mid to end April\nInsurance $250k per truck\n\nAll trucks need e-track throughout\nCommodity is Production Equipment (lighting, audio, video etc)",
    "client_name": "ABC Logistics"
  }'
```

Expected response:
```json
{
  "success": true,
  "data": {
    "origin_city": "Los Angeles",
    "origin_state": "CA",
    "destination_city": "Greenville",
    "destination_state": "SC",
    "equipment_type": "53' Trailer",
    "quantity": 16,
    "loading_date_start": "2026-04-15",
    "loading_date_end": "2026-04-30",
    "special_requirements": ["e-track throughout", "Insurance $250k per truck", "Production Equipment"],
    "confidence": 0.95
  }
}
```

### 4. Get Carriers

```bash
curl "http://localhost:8000/api/carriers"
```

Expected response:
```json
[
  {
    "id": 1,
    "name": "Carrier A",
    "email": "quotes@carriera.com",
    "phone": "123-456-7890",
    "created_at": null
  },
  ...
]
```

### 5. Generate Quote Sheet

```bash
curl -X POST "http://localhost:8000/api/generate-quote-sheet" \
  -H "Content-Type: application/json" \
  -d '{
    "quote_data": {
      "origin_city": "Los Angeles",
      "origin_state": "CA",
      "destination_city": "Greenville",
      "destination_state": "SC",
      "equipment_type": "53\" Trailer",
      "quantity": 16,
      "special_requirements": ["e-track throughout"],
      "confidence": 0.95
    },
    "carriers": [
      {"id": 1, "name": "Carrier A", "email": "quotes@carriera.com", "phone": "123-456-7890", "created_at": null},
      {"id": 2, "name": "Carrier B", "email": "rates@carrierb.com", "phone": "234-567-8901", "created_at": null}
    ],
    "client_name": "ABC Logistics"
  }'
```

Expected response:
```json
{
  "success": true,
  "file_url": "/downloads/quote_ABC_Logistics_20260331_150230.xlsx",
  "filename": "quote_ABC_Logistics_20260331_150230.xlsx"
}
```

Download the file:
```
http://localhost:8000/downloads/quote_ABC_Logistics_20260331_150230.xlsx
```

## API Endpoints

### Email Parsing
- `POST /api/parse-email` - Parse client email to extract quote details

### Quote Generation
- `POST /api/generate-quote-sheet` - Generate Excel quote sheet
- `GET /api/downloads/{filename}` - Download generated quote

### Carriers
- `GET /api/carriers` - List all carriers
- `POST /api/carriers` - Add new carrier
- `DELETE /api/carriers/{id}` - Delete carrier

### Health Check
- `GET /health` - Check if server is running
- `GET /` - API info

## Environment Variables

```env
# Backend
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/lane_rfp_agent
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

## Project Structure

```
FreightAgent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── email_parser.py      # Claude API integration
│   │   ├── main.py                   # FastAPI server
│   │   ├── config.py                 # Settings
│   │   ├── models.py                 # Pydantic models
│   │   └── excel_generator.py        # Excel generation
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/               # React components (TODO)
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
└── MVP_SPEC.md                       # Full specifications
```

## Next Steps

1. ✅ Backend API server running
2. ⏳ React components for email input and quote review
3. ⏳ Frontend-backend integration
4. ⏳ End-to-end testing with sample data
5. ⏳ Demo to Nita

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
Add your API key to `.env`:
```
ANTHROPIC_API_KEY=sk-your-key-here
```

### "Connection refused on port 8000"
Make sure backend is running:
```bash
cd backend && python -m uvicorn app.main:app --reload
```

### CORS errors
Check that `CORS_ORIGINS` includes your frontend URL in `.env`

### "File not found" when downloading
Make sure the `downloads/` directory exists in the backend folder
