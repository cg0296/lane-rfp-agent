# Lane RFP Agent — MVP Specification

## Problem Statement

Freight brokers receive unstructured client emails requesting quotes (origin, destination, equipment type, qty, dates, special requirements). They manually create Excel spreadsheets from these emails, then send them to carriers.

**Current workflow (manual):**
1. Receive email from client
2. Open Excel, create columns manually
3. Type in pickup/delivery cities, equipment details, dates
4. Add rows for each lane/shipment
5. Format and send to carriers

**MVP solution:**
Automate step 1-5. User pastes email → AI extracts details → generates Excel → ready to send.

---

## MVP User Flow

### Step 1: Paste Client Email
User lands on app, sees a form:
- **Text area:** "Paste client email here"
- **Button:** "Parse Email"

### Step 2: AI Extracts Details
Backend calls Claude API with the email. Claude extracts:
- **Origin cities/states** (e.g., Los Angeles, CA)
- **Destination cities/states** (e.g., Greenville, SC)
- **Equipment type** (e.g., 53' trailer, flatbed, etc.)
- **Quantity** (e.g., 16 trucks)
- **Dates** (loading/delivery window)
- **Special requirements** (e-track, insurance requirements, commodity type, etc.)

### Step 3: Review & Add Carriers
User sees parsed data in a form:
```
Origin: Los Angeles, CA
Destination: Greenville, SC
Equipment: 53' Trailer
Quantity: 16 trucks
Loading: Mid to end April
Insurance: $250k per truck
Special Reqs: E-track throughout, Production Equipment
```

User can edit any field.

Below that, a **Carrier Management** section:
- Table of carriers (Name, Email)
- Add carrier button
- Remove carrier button

Example carriers (pre-populated or user adds):
```
| Name         | Email               |
|--------------|---------------------|
| Carrier A    | quotes@carriera.com |
| Carrier B    | rates@carrierb.com  |
| Carrier C    | dispatch@carrierc.com|
```

### Step 4: Generate & Download
- **Button:** "Generate Quote Sheet"
- System creates Excel file with:
  - One row per truck/lane (16 rows for 16 trucks)
  - Columns: Origin, Destination, Equipment, Special Reqs, Carrier Rate (blank for them to fill)
  - Metadata at top: Date created, client info, notes
- **Button:** "Download Excel"
- **Button:** "Send to Carriers" (optional - pre-fills email template with carrier list)

---

## Sample Data (for testing/demo)

### Sample Client Email
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
ABC Logistics
```

### Parsed Output (JSON)
```json
{
  "origin_city": "Los Angeles",
  "origin_state": "CA",
  "destination_city": "Greenville",
  "destination_state": "SC",
  "equipment_type": "53' Trailer",
  "driver_type": "Team Drivers and Solo",
  "quantity": 16,
  "loading_date_start": "2026-04-15",
  "loading_date_end": "2026-04-30",
  "special_requirements": [
    "E-track throughout",
    "Insurance $250k per truck",
    "Commodity: Production Equipment (lighting, audio, video)"
  ],
  "confidence": 0.95
}
```

### Generated Excel (16 rows, one per truck)
```
Lane RFP - ABC Logistics - 2026-03-30

Origin: Los Angeles, CA
Destination: Greenville, SC
Equipment: 53' Trailer
Quantity: 16 trucks
Loading: Mid to end April
Insurance: $250k per truck
Special Requirements: E-track throughout, Production Equipment

| Lane # | Origin         | Destination       | Equipment | Driver Type       | Qty | Special Reqs           | Carrier Rate |
|--------|----------------|-------------------|-----------|-------------------|-----|------------------------|--------------|
| 1      | Los Angeles CA | Greenville SC     | 53' Trail | Team Drivers      | 1   | E-track, Production Eq | ___________  |
| 2      | Los Angeles CA | Greenville SC     | 53' Trail | Team Drivers      | 1   | E-track, Production Eq | ___________  |
| 3      | Los Angeles CA | Greenville SC     | 53' Trail | Solo              | 1   | E-track, Production Eq | ___________  |
| ...    | ...            | ...               | ...       | ...               | ... | ...                    | ...          |
| 16     | Los Angeles CA | Greenville SC     | 53' Trail | Solo              | 1   | E-track, Production Eq | ___________  |
```

---

## Tech Stack for MVP

| Component | Technology |
|-----------|------------|
| Frontend | React + Tailwind + Shadcn/UI |
| Backend | FastAPI (Python) |
| AI Parsing | Claude API (claude-3-5-sonnet) |
| Excel Generation | openpyxl |
| Hosting | Vercel (frontend) + Railway/AWS (backend) |

---

## API Endpoints (MVP)

### Parse Email
```
POST /api/parse-email

Request:
{
  "email_text": "Hello Jillian...",
  "client_name": "ABC Logistics" (optional)
}

Response:
{
  "origin_city": "Los Angeles",
  "origin_state": "CA",
  "destination_city": "Greenville",
  "destination_state": "SC",
  "equipment_type": "53' Trailer",
  "driver_type": "Team Drivers and Solo",
  "quantity": 16,
  "loading_date_start": "2026-04-15",
  "loading_date_end": "2026-04-30",
  "special_requirements": [...],
  "confidence": 0.95
}
```

### Generate Quote Sheet
```
POST /api/generate-quote-sheet

Request:
{
  "origin_city": "Los Angeles",
  "origin_state": "CA",
  "destination_city": "Greenville",
  "destination_state": "SC",
  "equipment_type": "53' Trailer",
  "quantity": 16,
  "loading_date_start": "2026-04-15",
  "loading_date_end": "2026-04-30",
  "special_requirements": [...],
  "carriers": [
    {"name": "Carrier A", "email": "quotes@carriera.com"},
    {"name": "Carrier B", "email": "rates@carrierb.com"}
  ]
}

Response:
{
  "file_url": "/downloads/quote-sheet-abc-logistics-2026-03-30.xlsx",
  "filename": "quote-sheet-abc-logistics-2026-03-30.xlsx"
}
```

---

## Frontend Pages (MVP)

### 1. Home / Quote Creator
- **Left side:** Email input textarea
- **Center:** Parsed fields (editable)
- **Right side:** Carrier list (add/remove)
- **Bottom:** "Generate Quote Sheet" button

### 2. Download
- Show preview of Excel
- Download button
- "Create Another" button

---

## Claude API Prompt (for Email Parsing)

```
Extract the following information from this freight quote request email:

- Origin city and state
- Destination city and state
- Equipment type (trailer size, type, flatbed, etc.)
- Driver type (solo, team, owner-op, etc.)
- Quantity of trucks/loads
- Loading date (start and end if range given)
- Delivery date (if specified)
- Any special requirements (insurance requirements, e-track, commodity type, equipment specs, etc.)

Return as JSON. Be conservative - if you're not sure about a detail, omit it or mark confidence low.

Email:
{email_text}
```

---

## Implementation Plan

### Phase 1: Core Engine (2 days)
- [ ] FastAPI backend setup
- [ ] Claude API integration for email parsing
- [ ] Excel generation with openpyxl
- [ ] Test with sample emails

### Phase 2: Frontend UI (2 days)
- [ ] React setup + Tailwind
- [ ] Email input form
- [ ] Parsed fields display + editing
- [ ] Carrier management table
- [ ] Download functionality

### Phase 3: Polish & Deployment (1 day)
- [ ] Error handling
- [ ] Input validation
- [ ] Deploy to Vercel + Railway
- [ ] Test end-to-end

**Total: ~5 days for MVP**

---

## Success Metrics

- User pastes email → system extracts details with 95%+ accuracy
- Generated Excel matches user's manual format
- Can handle 10+ different email formats
- Generation time < 5 seconds
- Users can edit parsed details before generating Excel

---

## Future Enhancements (Phase 2+)

- Save quote templates for recurring clients
- Multi-lane quotes (different origin/dest combos in one email)
- Email integration (auto-send to carriers)
- Rate consolidation (Part 2 of original project)
- Rate history & carrier performance scoring
