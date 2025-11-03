import platform
import subprocess
import re

def ping_host(ip: str):
    """
    Cross-platform ping function.
    Returns average latency in milliseconds, or None if host unreachable.
    """
    try:
        system = platform.system().lower()
        if system.startswith("win"):
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            m = re.search(r"time[=<]\s?(\d+)\s*ms", result.stdout)
            return float(m.group(1)) if m else None
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            m = re.search(r"time[=<]\s?(\d+\.?\d*)\s*ms", result.stdout)
            return float(m.group(1)) if m else None
    except Exception:
        return None
