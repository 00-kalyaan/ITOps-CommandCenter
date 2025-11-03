from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from .models import Asset, Metric
from .collectors.sys_metrics import collect_local_metrics
from .collectors.net_probe import ping_host
from .rules import evaluate_latest_metric

scheduler = BackgroundScheduler()


def job_collect_metrics(engine):
    # This function collects metrics for all assets and applies threshold rules
    with Session(engine) as s:
        assets = s.exec(select(Asset)).all()
        for asset in assets:
            # Collect system metrics (CPU, RAM, Disk)
            m = collect_local_metrics(asset)
            # Measure latency / ping
            m.ping_ms = ping_host(asset.ip)
            # Save metric and evaluate against rules
            s.add(m)
            s.commit()
            evaluate_latest_metric(s, m)
        s.commit()


def start_scheduler(engine):
    """Start APScheduler background job"""
    if scheduler.running:
        return
    scheduler.add_job(job_collect_metrics, "interval", minutes=1, args=[engine], id="collect")
    scheduler.start()
