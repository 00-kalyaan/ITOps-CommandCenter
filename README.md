# ITOps Command Center Dashboard


A portfolio‑ready Service Desk/NOC console for Tier‑1/2 support. Monitor endpoints, open tickets automatically, and run one‑click fixes.


## Features
- Live metrics: CPU, RAM, Disk, Latency
- Auto tickets on threshold breach
- One‑click actions: PowerShell/Bash
- Alerts: Email/Webhook
- SQLite data layer + FastAPI


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app.main:app --reload --port 8000
