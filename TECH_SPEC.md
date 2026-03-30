# Lane RFP Agent — Web App Tech Spec

## Database Schema

```sql
-- Users & Projects
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  name VARCHAR(255),
  client_name VARCHAR(255),
  markup_percentage DECIMAL(5,2) DEFAULT 15.00,
  status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Carriers
CREATE TABLE carriers (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  status VARCHAR(50) DEFAULT 'pending', -- pending, sent, responded
  responded_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(project_id, name)
);

-- Files & Uploads
CREATE TABLE uploads (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  carrier_id INTEGER REFERENCES carriers(id), -- NULL for client file
  filename VARCHAR(255),
  file_path VARCHAR(500),
  upload_type VARCHAR(50), -- 'client_rfp', 'carrier_response'
  status VARCHAR(50) DEFAULT 'processing', -- processing, parsed, error
  error_message TEXT,
  parsed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Lanes (individual shipping lanes)
CREATE TABLE lanes (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  lane_number INTEGER, -- position in original spreadsheet
  pickup_city VARCHAR(100),
  pickup_state VARCHAR(2),
  delivery_city VARCHAR(100),
  delivery_state VARCHAR(2),
  skids INTEGER,
  weight DECIMAL(10,2),
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(project_id, pickup_city, pickup_state, delivery_city, delivery_state)
);

-- Rates (carrier quotes per lane)
CREATE TABLE rates (
  id SERIAL PRIMARY KEY,
  lane_id INTEGER NOT NULL REFERENCES lanes(id),
  carrier_id INTEGER NOT NULL REFERENCES carriers(id),
  quoted_rate DECIMAL(10,2),
  is_winner BOOLEAN DEFAULT FALSE,
  final_rate DECIMAL(10,2), -- quoted_rate * (1 + markup%)
  upload_id INTEGER REFERENCES uploads(id),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(lane_id, carrier_id)
);

-- Consolidation Results
CREATE TABLE consolidations (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  status VARCHAR(50) DEFAULT 'in_progress', -- in_progress, completed
  total_lanes INTEGER,
  lanes_with_rates INTEGER,
  consolidated_at TIMESTAMP,
  file_path VARCHAR(500), -- path to final Excel file
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints

### Authentication
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Projects
```
GET    /api/projects                    # List user's projects
POST   /api/projects                    # Create new project
GET    /api/projects/{id}               # Get project details
PUT    /api/projects/{id}               # Update project
DELETE /api/projects/{id}               # Delete project
GET    /api/projects/{id}/status        # Get project status
```

### Uploads
```
POST   /api/projects/{id}/upload        # Upload file (multipart/form-data)
GET    /api/projects/{id}/uploads       # List all uploads for project
GET    /api/uploads/{id}                # Get upload details
DELETE /api/uploads/{id}                # Delete upload
```

### Carriers
```
GET    /api/projects/{id}/carriers      # List carriers for project
POST   /api/projects/{id}/carriers      # Add carrier
PUT    /api/carriers/{id}               # Update carrier
DELETE /api/carriers/{id}               # Delete carrier
GET    /api/carriers/{id}/status        # Get response status
```

### Lanes
```
GET    /api/projects/{id}/lanes         # List lanes for project (paginated)
GET    /api/lanes/{id}                  # Get lane details with all rates
GET    /api/lanes/{id}/rates            # Get all rates for a lane
```

### Rates & Consolidation
```
GET    /api/projects/{id}/rates         # Get all rates for project
GET    /api/projects/{id}/comparison    # Get comparison matrix (all lanes × all carriers)
POST   /api/projects/{id}/consolidate   # Trigger consolidation
GET    /api/consolidations/{id}         # Get consolidation results
POST   /api/consolidations/{id}/download # Download final Excel file
```

### Admin Dashboard
```
GET    /api/admin/stats                 # Overall system stats
GET    /api/admin/projects              # All projects
GET    /api/admin/users                 # All users
```

---

## File Upload & Parsing Flow

### Request
```
POST /api/projects/{id}/upload
Content-Type: multipart/form-data

{
  "file": <File>,
  "carrier_id": 5,  // NULL if this is the client RFP
  "file_type": "carrier_response"
}
```

### Response
```json
{
  "id": 42,
  "project_id": 1,
  "carrier_id": 5,
  "filename": "carrier_rates.xlsx",
  "status": "processing",
  "uploaded_at": "2026-03-30T15:30:00Z"
}
```

### Backend Processing
1. Save file to temp directory
2. Read with pandas: `pd.read_excel(file_path)`
3. Detect columns (fuzzy match: pickup, delivery, skids, weight, rate)
4. Validate data (numeric rates, valid cities, etc)
5. Match lanes to project lanes (fuzzy city matching)
6. Insert rates into DB
7. Update upload status to 'parsed'
8. Trigger consolidation check (if all carriers have responded)

---

## Consolidation Algorithm

```python
# Pseudo-code
def consolidate_project(project_id):
    lanes = get_all_lanes(project_id)

    for lane in lanes:
        rates = get_rates_for_lane(lane.id)

        if not rates:
            continue

        # Find lowest rate
        winning_rate = min(rates, key=lambda r: r.quoted_rate)

        # Calculate final rate with markup
        markup = project.markup_percentage / 100
        final_rate = winning_rate.quoted_rate * (1 + markup)

        # Mark as winner
        update_rate(winning_rate.id, is_winner=True, final_rate=final_rate)

    # Generate Excel file with results
    result_file = generate_final_spreadsheet(project_id)

    # Update consolidation record
    update_consolidation(project_id, status='completed', file_path=result_file)
```

---

## Dashboard Data Views

### Project Overview
```json
{
  "project_id": 1,
  "client_name": "ABC Logistics",
  "status": "in_progress",
  "stats": {
    "total_lanes": 250,
    "lanes_with_quotes": 240,
    "carriers_responded": 5,
    "carriers_pending": 3,
    "completion_percentage": 96
  },
  "carriers": [
    {
      "id": 5,
      "name": "Carrier A",
      "status": "responded",
      "responded_at": "2026-03-30T14:15:00Z",
      "rates_provided": 248
    }
  ],
  "consolidation_status": "ready_to_consolidate"
}
```

### Lanes & Rates Grid
```json
{
  "lanes": [
    {
      "id": 1,
      "pickup": "Chicago, IL",
      "delivery": "Atlanta, GA",
      "skids": 20,
      "weight": 15000,
      "rates": [
        {"carrier": "Carrier A", "rate": 1200, "is_winner": true, "final": 1380},
        {"carrier": "Carrier B", "rate": 1350, "is_winner": false},
        {"carrier": "Carrier C", "rate": 1100, "is_winner": false}
      ]
    }
  ]
}
```

### Consolidation Results
```json
{
  "id": 1,
  "project_id": 1,
  "status": "completed",
  "stats": {
    "total_lanes": 250,
    "total_revenue": 312500,
    "average_margin": 15,
    "consolidation_time_seconds": 8
  },
  "download_url": "/api/consolidations/1/download"
}
```

---

## Frontend Pages

### 1. Projects List
- Create new project button
- Table with: Client name, status, # of lanes, # of carriers, last updated
- Quick actions: View, Edit, Delete

### 2. Project Dashboard
- **Left panel:** Project info, carriers (with response status), markup %
- **Center panel:** Key stats (lanes, responses, completion %)
- **Right panel:** Action buttons (Upload file, View rates, Consolidate, Download)

### 3. Upload Area
- Drag-and-drop zone
- File queue with progress
- File type selector (Client RFP vs Carrier Response)
- Carrier dropdown (for carrier responses)

### 4. Rates Dashboard
- Searchable table of all lanes
- Columns: Pickup, Delivery, Skids, Weight, + rate column per carrier
- Highlight lowest rate per lane (green)
- Sortable, filterable

### 5. Consolidation Results
- Summary stats (total revenue, avg markup, processing time)
- Preview table of final results (pickup, delivery, winner carrier, final rate)
- Download button for final Excel file

---

## n8n/Zapier Automation

### Workflow: Auto-Upload from Google Drive

**Trigger:** New file in specific Google Drive folder
**Actions:**
1. Download file from Drive
2. Determine project ID from filename (e.g., `PROJECT-123-carrier-a.xlsx`)
3. Determine carrier from filename
4. Call `POST /api/projects/{id}/upload` with file
5. Wait for parsing to complete
6. If all carriers responded → call `POST /api/projects/{id}/consolidate`
7. Download final file
8. Email final spreadsheet to user

**Alternative:** Watch OneDrive folder instead

---

## Tech Stack Summary

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + Tailwind CSS + Shadcn/UI |
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | PostgreSQL 14+ |
| **File Processing** | pandas, openpyxl, fuzzywuzzy |
| **Authentication** | JWT tokens |
| **Automation** | n8n or Zapier |
| **Hosting** | Vercel (frontend) + AWS/Railway (backend) |
| **Storage** | AWS S3 or local file system |

---

## Implementation Phases

### Phase 1: MVP (1 week)
- Database setup
- File upload & parsing
- Basic dashboard
- Consolidation engine
- Download results

### Phase 2: Polish (3-4 days)
- UI refinement
- Error handling & validation
- Rate comparison matrix
- Carrier status tracking

### Phase 3: Automation (3-4 days)
- n8n/Zapier integration
- Email notifications
- Batch upload support

### Phase 4: Extra Features (optional)
- User authentication
- Multi-user projects
- Rate history tracking
- AI analysis layer (Option 3)
