# Lane RFP Workflows

## Option 1: Bid Consolidator

```
MANUAL PROCESS                          CONSOLIDATED PROCESS
─────────────────                       ──────────────────

Client sends                            Client sends
spreadsheet                             spreadsheet
    │                                       │
    ▼                                       ▼
Broker manually                         Broker exports
emails carriers                         to folder
    │                                       │
    ▼                                       ▼
Carriers respond                        Carriers respond
(5-10 different                         (5-10 different
spreadsheets)                           spreadsheets)
    │                                       │
    ▼                                       ▼
Broker manually                         Broker uploads
compares rates                          to Consolidator
line by line                                │
(4-6 hours)                             ▼
    │                                   Tool parses
    ▼                                   all files
Broker builds                               │
final spreadsheet                       ▼
with lowest rates                       Tool compares
    │                                   rates per lane
    ▼                                       │
Client receives                         ▼
quote                                   Tool picks
                                        lowest + markup
                                            │
                                            ▼
                                        Final spreadsheet
                                        generated
                                            │
                                            ▼
                                        Client receives
                                        quote

Time savings: 4-6 hours → 15 minutes
```

---

## Option 2: Bid Automation Suite

```
CLIENT                      BROKER                      CARRIERS
──────                      ──────                      ─────────

Submit                      Create project
RFP                         with carrier list
    │                           │
    ▼                           ▼
                            Upload client
                            spreadsheet
                                │
                                ▼
                            Review & confirm
                                │
                                ▼
                            ONE-CLICK SEND
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
    [Email]             [Email]               [Email]
  Carrier A             Carrier B             Carrier C
        │                       │                       │
        ▼                       ▼                       ▼
  [Tool monitors inbox — receives responses as they come in]
        │                       │                       │
        ▼                       ▼                       ▼
   Downloads              Downloads              Downloads
   & parses               & parses               & parses
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                        Response tracking
                        dashboard shows:
                        - Who responded
                        - Who hasn't
                        - When they responded
                                │
                                ▼
                        Broker clicks
                        "Stop waiting"
                                │
                                ▼
                        Consolidation engine
                        runs automatically
                                │
                                ▼
                        Final spreadsheet
                        ready
                                │
                                ▼
Receives                    Broker reviews
quote                       & sends
                                │
                                ▼
                            Client receives
                            quote

Time savings: 6 hours → 30 minutes (including manual review)
```

---

## Option 3: Full RFP Agent

```
CLIENT PORTAL                   BROKER DASHBOARD              CARRIERS
─────────────                   ────────────────              ────────

Login to
portal
    │
    ▼
Submit RFP
spreadsheet
    │
    ▼
Status: Pending
(real-time update)
    │
    │
    ├─────────────────────────────────────────────┐
    │                                             │
    ▼                                             ▼
Real-time status                        Broker sees
shows:                                  new RFP
- Carriers contacted                    │
- Responses received                    ▼
- Analysis running                      Agent auto-selects
                                        carriers from
                                        scoring system
                                            │
                                            ▼
                                        ONE-CLICK SEND
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
                [Email]             [Email]               [Email]
              Carrier A             Carrier B             Carrier C
                    │                       │                       │
                    ▼                       ▼                       ▼
              [Auto-collection continues — agent monitors inbox]
                    │                       │                       │
                    └───────────────────────┼───────────────────────┘
                                            │
                                            ▼
                                    Agent runs
                                    AI analysis:
                                    - Flag outliers
                                    - Compare to
                                      historical rates
                                    - Scoring
                                            │
                                            ▼
                                    Agent consolidates
                                    with AI insights
                                            │
    ┌───────────────────────────────────────┼───────────────────────────────────────┐
    │                                       │                                       │
    ▼                                       ▼                                       ▼
Status updated:                     Broker sees:                            Dashboard shows:
- Rates received                    - Consolidated                         - Carrier leaderboard
- AI analysis complete              spreadsheet                            - Rate trends
- Recommendations                   - AI recommendations                   - Historical comparison
shown                               - Carrier scoring
    │                               - Rate outliers
    ▼                                   │
View insights:                          ▼
- Market rates                      Broker reviews &
- Recommendations                   approves
- Rate trends                           │
                                        ▼
                                    Final spreadsheet
                                    + insights exported
                                        │
    ▼                                   ▼
Download final                      Client receives
quote with                          quote
insights                                │
                                        ▼
                                    Portal shows:
                                    - Quote details
                                    - Market comparison
                                    - Recommendations

Time savings: 6 hours → 15 minutes
Value-add: Market insights, carrier scoring, historical trending
```

---

## Key Workflow Differences

| Aspect | Option 1 | Option 2 | Option 3 |
|--------|----------|----------|----------|
| **Carrier outreach** | Manual email | Automated | Automated + smart routing |
| **Response collection** | Manual download | Automated | Automated |
| **Consolidation** | Manual process → Tool | Automated | Automated |
| **Analysis** | None | None | AI-powered insights |
| **Client experience** | Email quote | Email quote | Portal + insights |
| **Historical data** | Not tracked | Optional | Central DB + trending |
| **Carrier scoring** | None | Basic | Comprehensive |

---

## Data Flow

### Option 1
```
Carrier files → Consolidator → Final spreadsheet
```

### Option 2
```
Client RFP → Agent distributes → Inbox monitoring → Auto-parsing → Consolidator → Final spreadsheet
```

### Option 3
```
Client Portal → Agent distributes → Inbox monitoring → Auto-parsing → AI Analysis → Consolidator →
Portal delivery + historical DB + carrier scoring dashboard
```
