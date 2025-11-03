from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from .models import Asset, Metric
from .collectors.sys_metrics import collect_local_metrics
from .collectors.net_probe import ping_host


scheduler = BackgroundScheduler()


def job_collect_metrics(engine):
with Session(engine) as s:
for asset in s.exec(select(Asset)).all():
m = collect_local_metrics(asset) # for demo, treat all as local
m.ping_ms = ping_host(asset.ip)
s.add(m)
s.commit()


_defers = {}


def start_scheduler(engine):
if scheduler.running:
return
scheduler.add_job(job_collect_metrics, "interval", minutes=1, args=[engine], id="collect")
scheduler.start()
