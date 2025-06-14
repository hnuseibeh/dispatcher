
"""Minimal FastAPI dispatcher MVP."""
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3, time, pathlib, uuid

BASE = pathlib.Path(__file__).resolve().parents[2]
DB   = BASE / "sql" / "zaki.db"
app  = FastAPI(title="Zaki‑OS Dispatcher MVP")
app.mount("/static", StaticFiles(directory=str(BASE / "ui" / "dispatcher" / "static")), name="static")

def init_db():
    schema = (BASE / "sql" / "schema.sql").read_text()
    conn = sqlite3.connect(DB)
    for stmt in filter(None, schema.split(';')):
        conn.execute(stmt)
    conn.commit(); conn.close()

@app.on_event("startup")
def startup():
    if not DB.exists():
        init_db()

@app.post("/submit")
async def submit(prompt:str = Form(...), title:str = Form(...), agent:str = Form("unassigned")):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO agent_tasks(title,prompt,status,created_unix,assigned_agent) VALUES(?,?,?,?,?)",
        (title, prompt, "pending", int(time.time()), agent)
    )
    conn.commit(); conn.close()
    return RedirectResponse("/", status_code=303)

@app.get("/")
async def form():
    html = '''
    <html><body>
    <h1>Zaki‑OS Task Submit</h1>
    <form action="/submit" method="post">
    Title:<br><input type="text" name="title"><br>
    Prompt:<br><textarea name="prompt" cols="60" rows="10"></textarea><br>
    Assign to:<select name="agent"><option value="unassigned">--manual later--</option>
    <option value="Claude">Claude</option><option value="Cursor-GPT4">Cursor‑GPT4</option></select><br>
    <button type="submit">Submit</button>
    </form></body></html>
    '''
    return html
