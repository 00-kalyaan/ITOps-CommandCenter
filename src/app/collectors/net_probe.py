import subprocess


def ping_host(ip: str) -> float | None:
try:
# cross-platform ping (Linux/macOS), for Windows adjust -n / -w
out = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, text=True)
if out.returncode != 0:
return None
# parse avg time (simple heuristic)
for line in out.stdout.splitlines():
if "time=" in line:
tok = line.split("time=")[-1]
return float(tok.split(" ")[0].replace("ms", ""))
except Exception:
return None
