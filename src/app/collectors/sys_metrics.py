import psutil
from ..models import Metric


def collect_local_metrics(asset) -> Metric:
    """Collect local system performance metrics"""
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    # Create Metric object (linked to this asset)
    return Metric(
        asset_id=asset.id,
        cpu=cpu,
        ram=ram,
        disk=disk
    )
