from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, create_engine, select
from pathlib import Path
from .models import Asset, Metric, Ticket
from .scheduler import start_scheduler


DB_PATH = Path("./data/itops.db")
DB_PATH.parent.mkdir(exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


app = FastAPI(title="ITOps Command Center")
templates = Jinja2Templates(directory="src/app/templates")


@app.on_event("startup")
def _startup():
start_scheduler(engine)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
with Session(engine) as s:
assets = s.exec(select(Asset)).all()
tickets_open = s.exec(select(Ticket).where(Ticket.status != "RESOLVED")).all()
return templates.TemplateResponse("dashboard.html", {"request": request, "assets": assets, "tickets": tickets_open})
