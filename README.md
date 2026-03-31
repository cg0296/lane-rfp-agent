# Lane RFP Agent MVP

AI-powered tool that converts freight quote request emails into professional Excel sheets in seconds.

## 🎯 What This Does

**Before:** Manually create Excel quote sheets from client emails (20-30 minutes per quote)
**After:** AI parses email → user reviews → downloads Excel (10 seconds)

## ⚡ Quick Start (5 minutes)

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

Open `http://localhost:5173` and start using.

## 📋 Documentation

- **[README_MVP.md](README_MVP.md)** - Feature overview and quick start
- **[SETUP.md](SETUP.md)** - Detailed setup with API examples
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Demo flow and production deployment
- **[MVP_COMPLETE.md](MVP_COMPLETE.md)** - What was built, metrics, next steps

## 🏗️ Project Structure

```
Lane-RFP-Agent/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── main.py       # API routes
│   │   ├── agents/       # Claude AI integration
│   │   ├── excel_generator.py
│   │   ├── models.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # React + Vite app
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   ├── package.json
│   └── tailwind.config.js
├── .planning/            # Planning docs and research
├── CLAUDE.md             # Code guidelines
└── README.md
```

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Python 3.11 |
| **AI** | Anthropic Claude API |
| **Excel** | openpyxl |
| **Frontend** | React 18, Vite, Tailwind |
| **Database** | PostgreSQL (Phase 2) |

## 📊 What's Included

✅ Email parsing with Claude AI
✅ Excel quote sheet generation
✅ Carrier management (add/remove)
✅ Professional UI with Tailwind CSS
✅ Full REST API with Swagger docs
✅ Sample email for testing
✅ Comprehensive documentation

## 🚀 Next Steps (Phase 2+)

- Database persistence
- Email integration (auto-send to carriers)
- Rate consolidation & comparison
- Client portal
- Carrier performance tracking

See [MVP_COMPLETE.md](MVP_COMPLETE.md) for full roadmap.

## 🤝 Contributing

For questions or contributions:
1. Check the documentation
2. See backend docs at `http://localhost:8000/docs` (when running)
3. Review code comments

## 📝 License

MIT
