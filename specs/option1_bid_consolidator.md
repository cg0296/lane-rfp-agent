# Option 1: Bid Consolidator Tool — Development Specification

**Version:** 1.0
**Date:** 2026-03-30
**Scope:** Consolidation-only tool. No email sending. No carrier communication. Manual file handoff in, automated comparison out.

---

## Overview

The Bid Consolidator is a lightweight desktop or web application that solves one specific problem: the broker receives 5–15 carrier response spreadsheets per RFP and currently opens them all manually to find the lowest rate on each lane. This tool eliminates that manual comparison step entirely.

The user drops in the original client lane file and all carrier response files. The tool reads every file, identifies the lane rows, matches them across carriers, finds the lowest rate per lane, tags the winning carrier, applies a configurable markup, and produces two output files: a client-ready spreadsheet and an internal carrier comparison report.

The user never touches a formula. The tool does not send emails, does not contact carriers, and does not require a database. It is a file-in, file-out processing engine with a review screen between input and export.

---

## User Workflow

1. Start a new RFP job. Give it a name (e.g., "Acme Foods March 2026").
2. Upload the original client lane file. This is the master list of lanes the client sent.
3. Upload one or more carrier response files. Each file is a spreadsheet the broker received back from a carrier. There is no required format — carriers use their own templates.
4. The tool parses every file and displays a column-mapping confirmation screen. For each file, the tool shows its best guess at which column is pickup city, pickup state, delivery city, delivery state, and rate. The user confirms or corrects the mapping.
5. The tool builds the consolidated comparison matrix and displays it on screen: one row per lane, one column per carrier, with the lowest rate highlighted per row.
6. The user reviews the matrix. They can flag or exclude specific lanes or carrier quotes if something looks wrong.
7. The user confirms the markup percentage (default 15%, editable).
8. Export. The tool generates two files:
   - `[JobName]_client_quote.xlsx` — the client-facing spreadsheet with final marked-up rates.
   - `[JobName]_carrier_comparison.xlsx` — the internal report showing all carrier rates side by side.

Total interaction time target: under 5 minutes per RFP once the user is familiar with the tool.

---

## Core Features

### F1 — Multi-file Upload
- Accept Excel (.xlsx, .xls) and CSV (.csv) files.
- Support uploading a folder in one action (drag-and-drop entire folder of carrier responses).
- No limit on number of files per job (practical range: 1–20 carrier files).
- Files are held in memory or a temp directory for the session; nothing is persisted to a database.

### F2 — Column Auto-Detection
- On ingest, attempt to identify the following columns by scanning header row text using fuzzy matching:
  - Pickup City
  - Pickup State (or combined City/State)
  - Delivery City
  - Delivery State (or combined City/State)
  - Number of Skids (may be labeled: skids, pallets, pallet count, units)
  - Weight (lbs, weight, total weight)
  - Rate (rate, all-in rate, total rate, quoted rate, price, cost)
- If a combined City/State column is detected (e.g., "Chicago, IL"), split it into city and state components automatically.
- Present the mapping to the user for confirmation before proceeding. Mappings are per-file — each carrier file may map differently.
- Save confirmed mappings for reuse if the same carrier filename pattern appears again (optional, Phase 4).

### F3 — Lane Harmonization
- Define a canonical lane key: `(pickup_city_normalized, pickup_state, delivery_city_normalized, delivery_state)`.
- Normalize city names: strip leading/trailing whitespace, title-case, resolve common abbreviations (e.g., "ST LOUIS" -> "St. Louis").
- State normalization: accept full state names and abbreviations, normalize to 2-letter uppercase.
- Match carrier lanes back to the master client lane list using the canonical key. Carrier rows that do not match any client lane are flagged as unrecognized (not silently dropped).
- Build a unified lane table: one row per unique lane from the master file, columns for each carrier's quoted rate.

### F4 — Lowest Rate Identification
- For each lane row, identify the minimum rate across all carrier columns (excluding blank/null cells).
- If only one carrier quoted a lane, that carrier's rate is the winner by default.
- If no carrier quoted a lane, the lane is flagged as "No Quotes" and excluded from the client output (unless the user overrides).
- Highlight the winning cell in the comparison matrix (green background in Excel output; visual indicator in UI).

### F5 — Carrier Tagging
- Each lane row records: `winning_carrier`, `winning_rate`, `quote_count` (how many carriers quoted this lane).
- In the comparison report, the winning cell for each lane is marked.

### F6 — Markup Application
- Apply markup as: `client_rate = winning_rate * (1 + markup_percentage / 100)`.
- Default markup: 15%.
- Markup is set once per job and applies to all lanes uniformly.
- Round client rate to 2 decimal places.
- The markup percentage is visible and editable on the review screen before export.

### F7 — Client-Ready Output
- Output columns: Pickup City, Pickup State, Delivery City, Delivery State, Skids, Weight, Rate.
- Rate column contains the marked-up rate.
- Formatted as a clean Excel file — no internal columns, no carrier names, no markup formula exposed.
- Column headers match the original client file headers where possible.

### F8 — Carrier Comparison Report
- One row per lane.
- Columns: lane key fields, then one column per carrier with their quoted rate, then: Lowest Rate, Winning Carrier, Marked-Up Rate, Quote Count.
- Winning rate cell highlighted in green.
- Unquoted lanes show a blank cell (not zero, not "N/A" — blank, to avoid confusion).
- Flagged/excluded lanes noted with a status column.

---

## Technical Architecture

### Recommended Tech Stack

**Backend / Processing Engine: Python**

Python is the correct choice here. The processing logic (file parsing, fuzzy matching, normalization, Excel output) maps directly onto mature, well-tested Python libraries. There is no reason to use Node for a data processing tool.

| Concern | Library |
|---|---|
| Excel read | `openpyxl`, `xlrd` (for .xls) |
| CSV read | `pandas` (via `pd.read_csv`) |
| DataFrame operations | `pandas` |
| Fuzzy column name matching | `rapidfuzz` |
| City/state normalization | custom lookup dict + regex |
| Excel output with formatting | `openpyxl` (direct cell formatting) |
| UI (Option A — desktop) | `Tkinter` or `PySimpleGUI` |
| UI (Option B — local web) | `Flask` + plain HTML/JS, no frontend framework needed |

**Recommended UI approach: Flask local web app.**

Reasons: drag-and-drop file upload is trivial in a browser, the comparison matrix renders naturally as an HTML table, and a Flask app runs locally without any install complexity beyond `pip install flask`. The user opens `http://localhost:5000` in their browser. Nothing is deployed to the cloud. No login, no accounts.

Avoid React/Vue for this — overkill for a single-user local tool with no real-time requirements.

### File Processing Pipeline

```
[Upload Files]
     |
     v
[Detect file type: xlsx / xls / csv]
     |
     v
[Read header row -> fuzzy match to canonical column names]
     |
     v
[Present mapping confirmation UI per file]
     |
     v
[User confirms mappings]
     |
     v
[Read data rows into pandas DataFrame per file]
     |
     v
[Normalize lane keys: city trim/case, state abbreviation]
     |
     v
[Match each carrier DataFrame against master lane list]
     |
     v
[Build consolidated matrix DataFrame]
     |
     v
[Compute: min rate, winning carrier, markup, flags]
     |
     v
[Display review matrix in UI]
     |
     v
[User approves + sets markup %]
     |
     v
[Generate client_quote.xlsx + carrier_comparison.xlsx]
     |
     v
[Download / save to disk]
```

### Data Model

**Lane (canonical record)**
```
lane_id:           int (row index from master file)
pickup_city:       str (normalized)
pickup_state:      str (2-letter)
delivery_city:     str (normalized)
delivery_state:    str (2-letter)
skids:             int or None
weight:            float or None
lane_key:          str (composite: "Chicago IL -> Dallas TX")
```

**CarrierQuote**
```
lane_key:          str (FK to Lane)
carrier_name:      str (derived from filename, editable)
rate:              float or None
source_file:       str (original filename)
source_row:        int (row number in source file, for traceability)
```

**ConsolidatedRow (output record)**
```
lane_key:          str
...all Lane fields...
rates:             dict[carrier_name -> float|None]
lowest_rate:       float or None
winning_carrier:   str or None
quote_count:       int
marked_up_rate:    float or None
status:            enum: OK | NO_QUOTES | FLAGGED | DUPLICATE
```

### Error Handling

| Error Condition | Behavior |
|---|---|
| File is empty or unreadable | Show error per file, skip file, continue with others |
| Header row not found (no recognizable columns) | Flag file as unrecognized, prompt user to manually map or skip |
| Carrier lane does not match any master lane | Log as unmatched row, show count in summary, do not include in output |
| Rate cell contains non-numeric value | Treat as blank (unquoted), log the cell reference |
| Rate cell is zero | Treat as a valid quote of $0.00, flag visually as unusual (zero-rate warning) |
| Duplicate lane in master file | Log warning, use first occurrence, show duplicate count in summary |
| Duplicate lane in carrier file | Use the lower of the two rates, log the occurrence |
| All carriers skipped for a lane | Mark lane as NO_QUOTES, exclude from client output, include in comparison report |

---

## UI/UX

### Upload Screen
- Large drag-and-drop zone for carrier response files.
- Separate control to designate the master client lane file (the original RFP spreadsheet).
- File list shows uploaded files with name, size, detected format, and a "remove" button.
- "Carrier name" field next to each file — pre-populated from filename (e.g., "ABF_response.xlsx" -> "ABF"), editable.
- "Process Files" button to advance to column mapping.

### Column Mapping Screen
- Displayed after initial parse, before data is processed.
- One section per uploaded file.
- Shows: detected header row, proposed column assignments.
- Each assignment is a dropdown — the user can correct any mis-detected column.
- A "preview" pane shows the first 3 data rows so the user can visually confirm.
- "Confirm All Mappings" button to proceed.

### Review Matrix Screen
- HTML table: rows = lanes, columns = carriers + computed columns.
- Winning rate cell highlighted in green per row.
- Lanes with NO_QUOTES highlighted in yellow.
- Flagged/excluded lanes highlighted in red.
- Checkbox per row to exclude a lane from the client output.
- Markup percentage field at top — live-updates the "Marked-Up Rate" column as the user types.
- Summary bar: total lanes, lanes with quotes, lanes without quotes, number of carriers.
- "Export" button at the bottom.

### Export
- Two download links appear: client quote file and carrier comparison file.
- Files are named with the job name and today's date automatically.
- If running as a local Flask app, files are saved to a user-specified output folder (configurable in settings) and the browser triggers a download.

### Settings (minimal)
- Default markup percentage (persisted to a local config file).
- Default output folder path.
- No user accounts, no cloud sync, no telemetry.

---

## Edge Cases

### Carrier Does Not Quote Every Lane
Handled by the matching step. If a carrier file has no row for a given master lane, the carrier's column for that lane is left blank. The tool never infers or interpolates missing rates. The `quote_count` field reflects how many carriers actually provided a number.

### Different Column Names Across Carrier Files
This is the core problem the column-mapping screen solves. Each file is mapped independently. The fuzzy matcher handles common variants:
- "Origin City" / "Ship From City" / "Pickup" / "O City" all map to Pickup City.
- "Destination" / "Consignee City" / "Del City" / "D City" all map to Delivery City.
- "All-In Rate" / "Quoted Rate" / "Total Cost" / "Price" / "Rate (USD)" all map to Rate.

The fuzzy match uses token-sort ratio (via `rapidfuzz`) with a confidence threshold of 70. Below threshold, the column is flagged as unmapped and the user must assign it manually.

### Duplicate Lanes
Two scenarios:

1. Duplicate in the master client file: same pickup/delivery combination appears more than once (e.g., different skid/weight classes). These are treated as distinct lanes if skid count or weight differs by more than a tolerance (configurable, default: skids differ by >= 2 or weight differs by >= 500 lbs). If they are truly identical, the first row is kept and a warning is shown.

2. Duplicate in a carrier response file: same lane appears twice with different rates. Use the lower rate and log the occurrence in the comparison report with a note.

### Multiple Rate Columns (LTL vs FTL)
Some carriers return files with both an LTL rate and an FTL rate column. The column-mapping screen will detect this — both columns will appear as candidates for "Rate." The user selects which rate type to use for this job. The unselected column is stored but not used in consolidation.

A future enhancement (Phase 4) could support running the consolidation twice — once for LTL rates and once for FTL — but this is out of scope for Phase 1.

### Currency and Number Formatting Issues
Rate cells may contain:
- `$1,250.00` — strip `$` and `,`, parse as float.
- `1250` — parse directly.
- `1,250` — strip `,`, parse as float.
- `1250.5` — parse directly.
- `$1.2K` — log as unparseable, treat as blank.
- `TBD`, `-`, `N/A`, empty string — treat as blank (unquoted).

Parsing uses a cleaning function applied to every rate cell before type conversion. Parsing failures are logged with file, row, and column reference so the user can investigate.

---

## Development Phases

### Phase 1 — Core Processing Engine
**Estimated effort: 4 days**

Deliverables:
- `consolidator/parser.py` — reads xlsx/xls/csv into a pandas DataFrame, detects header row, returns raw column list.
- `consolidator/mapper.py` — fuzzy column matching logic using `rapidfuzz`, returns mapping dict.
- `consolidator/normalizer.py` — lane key normalization (city/state cleaning, state abbreviation lookup table).
- `consolidator/engine.py` — takes master lane DataFrame and list of (carrier_name, carrier_DataFrame, column_mapping) tuples; returns the ConsolidatedRow list.
- `consolidator/rate_parser.py` — currency/number cleaning function.
- Unit tests for normalizer and rate_parser covering known edge cases.
- CLI runner (`run_consolidation.py`) that accepts a folder of files and produces output CSVs — no UI, used to validate the engine independently.

Validation: run against a set of 3–5 real or synthetic carrier files. Manually verify the output matrix matches what you would have built by hand.

### Phase 2 — Flask UI
**Estimated effort: 3 days**

Deliverables:
- `app.py` — Flask application, routes for upload, mapping confirmation, review, export.
- `templates/upload.html` — drag-and-drop upload screen.
- `templates/mapping.html` — per-file column mapping confirmation.
- `templates/review.html` — consolidated matrix with green highlighting, markup field, exclusion checkboxes.
- Session state management (Flask session or in-memory job store keyed by session ID).
- No JavaScript framework — vanilla JS only (fetch for async calls, DOM manipulation for live markup update).

### Phase 3 — Output Generation
**Estimated effort: 2 days**

Deliverables:
- `consolidator/exporter.py` — produces both Excel output files using `openpyxl`.
- Client quote file: clean formatting, correct column headers, no internal fields.
- Carrier comparison file: all carrier columns, conditional formatting (green fill on winning cells, yellow on no-quote rows), summary tab.
- Download route in Flask that serves the generated files.
- File naming convention: `{job_name}_{YYYYMMDD}_client_quote.xlsx` and `{job_name}_{YYYYMMDD}_carrier_comparison.xlsx`.

### Phase 4 — Polish and Edge Cases
**Estimated effort: 2 days**

Deliverables:
- Settings screen: default markup %, default output folder, persisted to `config.json`.
- Column mapping memory: save confirmed mappings per carrier filename pattern to `mappings_cache.json`, auto-apply on next upload of same carrier.
- Improved zero-rate warning (visual indicator in matrix).
- Unmatched lane report: a third output tab in the comparison file listing carrier rows that did not match any master lane.
- Input validation messaging improvements (clearer error text per file).
- Basic logging to `consolidator.log` for troubleshooting.
- End-to-end test using a realistic synthetic dataset of 200 lanes and 8 carriers.

**Total estimated effort: 11 development days.**

---

## Deliverables

At the end of development the client receives:

1. **The application** — a Python project (`pip install -r requirements.txt`, then `python app.py`) that runs locally on Windows. No cloud, no subscription, no external dependencies beyond Python and the listed libraries.

2. **Two output files per RFP job:**
   - `[JobName]_[Date]_client_quote.xlsx` — clean, client-facing, shows only lane fields and marked-up rate.
   - `[JobName]_[Date]_carrier_comparison.xlsx` — internal report with all carrier rates, winner highlighting, and unquoted lane flags.

3. **A settings file** (`config.json`) for default markup % and output folder.

4. **User documentation** — one-page PDF covering: how to start the app, how to upload files, how to confirm column mappings, how to review and export. Not a full manual — a quick reference card.

5. **Source code** — full Python source, MIT licensed, no obfuscation. The broker can modify it or hand it to another developer.

---

## Out of Scope for Option 1

The following are explicitly not included and should be treated as scope creep if raised during development:

- Sending emails to carriers.
- Parsing carrier responses directly from email attachments (that is Option 2).
- Any cloud storage or multi-user access.
- Historical rate tracking or lane benchmarking.
- Integration with TMS or any freight platform.
- PDF output.
- Mobile access.

---

## Dependencies and Assumptions

- The broker's machine runs Windows 10 or 11 with Python 3.10+ installable.
- The master client lane file always has a header row and consistent lane columns (it is the broker's own standardized template).
- Carrier response files always have a header row somewhere in the first 10 rows.
- All rates are in USD. No multi-currency support is needed.
- The broker reviews the column mapping screen on every new carrier template. The tool assists but does not auto-proceed without user confirmation.
- "Rate" means the all-in rate per lane per shipment. The tool does not calculate per-mile or per-hundredweight rates.
