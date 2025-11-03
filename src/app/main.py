from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, create_engine, select

from .models import Asset, Metric, Ticket, ActionLog
from .scheduler import start_scheduler

# --- DB setup ---
DB_PATH = Path("./data/itops.db")
DB_PATH.parent.mkdir(exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

# --- App / Templates ---
app = FastAPI(title="ITOps Command Center")
templates = Jinja2Templates(directory="src/app/templates")


@app.on_event("startup")
def _startup():
    start_scheduler(engine)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with Session(engine) as s:
        assets = s.exec(select(Asset)).all()
        tickets_open = s.exec(
            select(Ticket).where(Ticket.status != "RESOLVED")
        ).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "assets": assets, "tickets": tickets_open},
    )


@app.get("/tickets", response_class=HTMLResponse)
def tickets(request: Request):
    with Session(engine) as s:
        open_t = s.exec(
            select(Ticket).where(Ticket.status != "RESOLVED").order_by(Ticket.created_at.desc())
        ).all()
        resolved_t = s.exec(
            select(Ticket).where(Ticket.status == "RESOLVED").order_by(Ticket.updated_at.desc()).limit(20)
        ).all()
    return templates.TemplateResponse(
        "tickets.html", {"request": request, "open_t": open_t, "resolved_t": resolved_t}
    )


# Optional: redirect /tickets resolve endpoint (only if you added tickets.html button)
@app.post("/tickets/{ticket_id}/resolve")
def resolve_ticket(ticket_id: int):
    with Session(engine) as s:
        t = s.get(Ticket, ticket_id)
        if t:
            t.status = "RESOLVED"
            s.add(t)
            s.commit()
    return RedirectResponse("/tickets", status_code=303)
