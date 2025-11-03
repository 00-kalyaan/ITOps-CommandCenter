
# src/cli/seed_assets.py
import argparse
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from src.app.models import Asset  # uses the same model as the app

DB_PATH = Path("./data/itops.db")
DB_PATH.parent.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--prefix", type=str, default="demo-pc")
    args = p.parse_args()

    with Session(engine) as s:
        for i in range(args.count):
            a = Asset(
                hostname=f"{args.prefix}-{i+1:02d}",
                ip=f"192.168.1.{100+i}",
                tags="demo"
            )
            s.add(a)
        s.commit()
    print(f"[INFO] Inserted {args.count} assets ✅ at {DB_PATH}")

if __name__ == "__main__":
    main()
