import platform
import subprocess
import re
from typing import Optional


def ping_host(ip: str) -> Optional[float]:
    """
    Cross-platform ping function.
    Returns average latency in milliseconds, or None if host unreachable.
    """
    try:
        system = platform.system().lower()
        if system.startswith("win"):
            # Windows ping: -n count, -w timeout(ms)
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None

            match = re.search(r"time[=<]\s?(\d+)\s*ms", result.stdout)
            if match:
                return float(match.group(1))
            return None

        else:
            # Linux / macOS ping: -c count, -W timeout(seconds)
            cmd = ["ping", "-c", "1", "-W", "1", ip]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None

            match = re.search(r"time[=<]\s?(\d+\.?\d*)\s*ms", result.stdout)
            if match:
                return float(match.group(1))
            return None

    except Exception:
        return None
