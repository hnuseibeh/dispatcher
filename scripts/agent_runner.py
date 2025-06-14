
"""Minimal agent execution loop for Zaki‑OS MVP."""
import os, json, time, pathlib, sqlite3, shutil

BASE = pathlib.Path(__file__).resolve().parents[1]
DB   = BASE / "sql" / "zaki.db"
INBOX= BASE / "prompts"

def init_db():
    schema = (BASE / "sql" / "schema.sql").read_text()
    conn = sqlite3.connect(DB)
    for stmt in filter(None, schema.split(';')):
        conn.execute(stmt)
    conn.commit()
    conn.close()

def get_next_task():
    conn = sqlite3.connect(DB)
    row = conn.execute("SELECT id,title,prompt FROM agent_tasks WHERE status='approved' ORDER BY created_unix LIMIT 1").fetchone()
    conn.close()
    return row

def mark_status(task_id, status):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE agent_tasks SET status=?, completed_unix=? WHERE id=?", (status, int(time.time()), task_id))
    conn.commit(); conn.close()

def main():
    if not DB.exists():
        init_db()
    task = get_next_task()
    if not task:
        print("No work, exiting."); return
    task_id, title, prompt = task
    plan_path = BASE / "docs" / "plans" / f"PLAN_{task_id}.md"
    plan_path.write_text(f"# PLAN for Task {task_id}\n\nPrompt:\n````\n{prompt}\n````\n")
    input(f"PLAN created at {plan_path}. Press Enter once approved…")
    # Simulate work
    time.sleep(2)
    report_path = BASE / "docs" / "reports" / f"REPORT_{task_id}.md"
    report_path.write_text(f"# REPORT for Task {task_id}\n\nCompleted at unix {int(time.time())}")
    mark_status(task_id, "done")
    print(f"Task {task_id} complete.")

if __name__ == "__main__":
    main()
