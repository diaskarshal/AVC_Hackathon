# AVC Hackathon

Track: BuildFlow  

ERP for automating resource planning on industrial construction and repair projects in  Kazakhstan's petroleum sector.

---

## Tech stack

**Backend:** FastAPI, PostgreSQL 15, SQLAlchemy 2.0, JWT, Pandas, Scikit-learn

**Frontend:** React 19 + TypeScript, Tailwind CSS, Recharts, Axios

**Infrastructure:** Docker

---

## Get started

### Requirements

- Docker & Docker Compose
- API keys for: Gemini (aistudio.google.com) and Groq (console.groq.com)

### Steps

1. Clone repo:
```bash
git clone https://github.com/diaskarshal/AVC_Hackathon.git
cd AVC_Hackathon
```

2. Create `.env` according to `.env.example`:

3. Start container:
```bash
sudo docker-compose up --build
```

4. Seed DB:
```bash
sudo docker-compose exec backend python -m app.utils.seed_data
```

- Frontend: http://localhost:3000
- API: http://localhost:8001
- API docs: http://localhost:8001/docs