import psutil
from .typing import AssetLike # or just pass asset fields
from ..models import Metric


def collect_local_metrics(asset) -> Metric:
cpu = psutil.cpu_percent(interval=0.5)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent
return Metric(asset_id=asset.id, cpu=cpu, ram=ram, disk=disk)
