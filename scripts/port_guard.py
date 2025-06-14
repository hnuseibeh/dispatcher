
"""Utility to check service registry for port collisions."""
import sqlite3, sys, time, pathlib

DB = pathlib.Path(__file__).resolve().parents[1] / "sql" / "zaki.db"

def port_available(port:int)->bool:
    conn = sqlite3.connect(DB)
    row = conn.execute("SELECT 1 FROM registry_services WHERE port=?", (port,)).fetchone()
    conn.close()
    return row is None

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("Usage: port_guard.py <port>")
        sys.exit(1)
    p = int(sys.argv[1])
    if port_available(p):
        print(f"Port {p} is free ✔")
        sys.exit(0)
    print(f"Port {p} already registered! ✖")
    sys.exit(2)
