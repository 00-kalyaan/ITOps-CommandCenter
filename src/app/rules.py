
# src/app/rules.py
from datetime import datetime
from sqlmodel import Session, select
from .models import Metric, Ticket

THRESHOLDS = {
    "cpu": 85.0,    # %
    "ram": 90.0,    # %
    "disk": 90.0,   # %
    "ping_ms": 200  # ms; None = unreachable
}

def _ensure_ticket(s: Session, asset_id: int, summary: str, severity: str = "HIGH") -> Ticket:
    # If a similar open ticket exists, refresh it; else create new
    open_like = s.exec(
        select(Ticket).where(
            Ticket.asset_id == asset_id,
            Ticket.status != "RESOLVED",
            Ticket.summary == summary,
        )
    ).first()
    if open_like:
        open_like.updated_at = datetime.utcnow()
        s.add(open_like)
        return open_like

    t = Ticket(asset_id=asset_id, severity=severity, status="OPEN", summary=summary)
    s.add(t)
    return t

def evaluate_latest_metric(s: Session, metric: Metric) -> None:
    """Check a newly inserted Metric against thresholds and open/resolve tickets."""
    issues = []

    if metric.cpu is not None and metric.cpu >= THRESHOLDS["cpu"]:
        issues.append(f"High CPU {metric.cpu:.0f}%")
    if metric.ram is not None and metric.ram >= THRESHOLDS["ram"]:
        issues.append(f"High RAM {metric.ram:.0f}%")
    if metric.disk is not None and metric.disk >= THRESHOLDS["disk"]:
        issues.append(f"Low Disk headroom {metric.disk:.0f}% used")

    if metric.ping_ms is None:
        issues.append("Host unreachable (ping failed)")
    elif metric.ping_ms >= THRESHOLDS["ping_ms"]:
        issues.append(f"High latency {metric.ping_ms:.0f}ms")

    if issues:
        summary = " / ".join(issues)
        severity = "CRIT" if "unreachable" in summary else "HIGH"
        _ensure_ticket(s, metric.asset_id, summary, severity=severity)
        s.commit()
        return

    # No issues → resolve any open tickets for this asset
    open_ts = s.exec(
        select(Ticket).where(Ticket.asset_id == metric.asset_id, Ticket.status != "RESOLVED")
    ).all()
    for t in open_ts:
        t.status = "RESOLVED"
        t.updated_at = datetime.utcnow()
        s.add(t)
    s.commit()
