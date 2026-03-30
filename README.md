# Lane RFP Agent

AI-powered tool for freight brokers to consolidate carrier bid responses and optimize lane pricing.

## The Problem

Freight brokers send spreadsheets with 100-500 shipping lanes to multiple carriers. Each carrier fills in their rates and sends it back. The broker then **manually compares all responses** to find the lowest rate per lane — a process that takes 4-6 hours per project, repeated ~5x per week.

## What We're Building

### Option 1 — Bid Consolidator
Upload all carrier response spreadsheets → get back one consolidated sheet with the best rate per lane, carrier tagged, markup applied. Done in seconds.

### Option 2 — Bid Automation
One-click carrier outreach via email/text, automated response collection, and auto-consolidation as rates come in.

### Option 3 — Full RFP Agent
End-to-end agentic solution with AI rate analysis, historical tracking, carrier scoring, and a client portal.

## Tech Stack

- **Python** — core processing engine (pandas, openpyxl)
- **Claude AI** — agent orchestration and rate analysis
- **Microsoft Graph API** — email integration
- **Slack API** — notifications and carrier communication

## Project Structure

```
FreightAgent/
├── specs/              # Detailed specs for each option
├── outlook-mcp/        # Outlook email MCP server
├── Emails/             # Email correspondence
├── CLAUDE.md           # AI assistant instructions
├── PROJECT_STATUS.md   # Current project state
└── README.md
```

## Getting Started

Sample data incoming. More details soon.

## Contributing

Drop a message in the Discord thread if you want to pick up a piece.
