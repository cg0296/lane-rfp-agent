# Freight Agent — Project Status

## Overview
Building an agentic solution for **Nita Derbigny** (Assistant Transportation Manager, Beltmann Integrated Logistics) to automate the freight quoting process.

**Contact:** nita.derbigny@beltmann.com | 773-501-6569

---

## What We Know About the Process

1. Client sends a spreadsheet (Excel) with lanes to quote
   - Columns: Pickup location / Delivery location / # of skids / Weight of load
   - May have extra columns they don't need
2. Nita/team sends the spreadsheet to multiple carriers via email
3. Carriers fill in their rates on every lane and email the spreadsheet back
   - Carriers may call with questions, but rates must come via email
4. Team compares all carrier responses, picks the lowest rate per lane
5. Mark up 15% (always fixed) and fill the final spreadsheet with carrier name + marked-up rate
6. Send completed spreadsheet back to client

**Volume:** ~5 projects/week, each with 100-500 lanes. Always Excel.

---

## Remaining Questions
- How many carriers do they send each project to?
- Do all carriers get the same spreadsheet or is it segmented by lane/region?
- What's the typical turnaround time from sending to carriers to getting all rates back?
- Do they have a preferred carrier list or is it different per project?
- What does the final deliverable spreadsheet look like vs the one the client sent?

---

## Vision / Proposed Solution
Client spreadsheet comes in → team reviews/cleans extra columns → hits a button → system emails the spreadsheet to preferred carriers automatically → carriers fill in rates and email back → system ingests all returned spreadsheets, compares rates per lane, picks lowest, applies 15% markup, fills final spreadsheet → team reviews and sends back to client.

---

## Last Correspondence

### Nita → Curt | Mon Mar 30, 2026 10:08 AM
> Alright, so in short, I need to know if there is a way to make the following much simpler when it comes to getting all data on excel:
> Our clients will send us a spreadsheet of all the lanes needed to quote.
> Pick up location / del location / # of skids / weight of load / - then we provide the carrier and their rate.
> (we'd usually go with our lowest option and fill the chart with the carrier and their rate BUT we mark up.)
> So if a carrier quotes $1500, we mark up 15% and that would be the rate on the spreadsheet.

### Curt → Nita | Mon Mar 30, 2026 2:07 PM
Sent follow-up questions about cleanup, carrier outreach, rate format, markup, volume, and anything else. Pitched high-level agent vision.

### Nita → Curt | Mon Mar 30, 2026 4:01 PM (LATEST)
> - Client sheets may have extra columns but they only look at pickup/delivery/skids/weight
> - Carriers get the spreadsheet via email, fill in rates, send it back
> - All via email. Calls only for questions, rates must come via email
> - 15% markup always
> - ~5 projects/week, 100-500 lanes each
> - Always Excel

---

## Status
**Nita answered follow-up questions. Ready to draft next reply — remaining questions about carrier list, turnaround time, and final deliverable format.**

---

## Infrastructure Setup
- Outlook MCP server connected (cgolden@golteris.com)
- Slack workspace created: golteris.slack.com
- Slack MCP server: configured (pending restart verification)
- Second email (curtg@bbinsight08.com): pending — IT admin consent needed for Azure app OR forwarding setup
