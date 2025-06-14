# Start of ui/dispatcher/app.py
import os
import time
import pathlib
import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Optional
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
# Removed Form from fastapi imports as it's not used in the new version
from pydantic import BaseModel
# Removed StaticFiles as it's not in the provided new version
# Removed uuid as it's not in the provided new version

BASE = pathlib.Path(__file__).resolve().parents[2]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zaki_user:zaki_password@localhost:5432/zaki_os_db")

app = FastAPI(title="Zaki‑OS Dispatcher")
# app.mount("/static", ...) removed as it's not in the provided new version

# Pydantic Models
class TaskStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"
        pending_approval = "pending_approval" # Added

class TaskBase(BaseModel):
    title: str
    prompt: str
    assigned_agent: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class SubTaskCreate(TaskBase): # TaskBase should already be defined
    pass

class Task(TaskBase):
    id: int
    status: TaskStatus
    created_unix: int
    completed_unix: Optional[int] = None
    parent_task_id: Optional[int] = None
    dependency_ids: Optional[str] = None
    retry_count: int

    class Config:
        orm_mode = True

class SubTaskStatusInfo(BaseModel):
    id: int
    status: TaskStatus
    title: str

class LogLevel(str, Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"

class LogEntry(BaseModel):
    id: int
    task_id: int
    timestamp: int
    level: LogLevel
    message: str
    class Config:
        orm_mode = True

class AgentStatus(str, Enum):
    idle = "idle"
    busy = "busy"
    offline = "offline"

class Agent(BaseModel):
    id: int
    name: str
    status: AgentStatus
    description: Optional[str] = None
    host: Optional[str] = None
    port: int
    registered_unix: int
    class Config:
        orm_mode = True

def init_db():
    schema_path = BASE / "sql" / "schema.sql"
    if not schema_path.exists():
        print(f"Schema file not found at {schema_path}. Skipping DB initialization.")
        return

    schema_content = schema_path.read_text()
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cursor:
            # Split statements carefully, handling potential empty strings from split
            statements = [s.strip() for s in schema_content.split(';') if s.strip()]
            for stmt in statements:
                # Filter out PRAGMA statements for PostgreSQL
                if "PRAGMA" not in stmt.upper():
                    cursor.execute(stmt)
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM registry_services")
            count_result = cursor.fetchone()
            count = count_result[0] if count_result else 0

            if count == 0:
                sample_agents_data = [
                    ('AgentSmith_1', 'Matrix Sentinel Program', 'localhost', 10001, int(time.time())),
                    ('OracleBot_7', 'Information & Prophecy Service', 'localhost', 10002, int(time.time())),
                    ('MaintenanceBot_3', 'System Cleaner and Optimizer', 'localhost', 10003, int(time.time()))
                ]
                # Use executemany for PostgreSQL, or loop if issues persist with parameter style
                insert_query = "INSERT INTO registry_services (service_name, description, host, port, registered_unix) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(insert_query, sample_agents_data)
                conn.commit()
        print("Database initialization attempted from schema.sql using PostgreSQL.")
    except psycopg2.Error as e:
        print(f"Error during DB initialization with PostgreSQL: {e}")
        if conn: conn.rollback()
    except FileNotFoundError: # Should be caught by schema_path.exists() earlier
        print(f"Schema file not found at {schema_path} during init_db.")
    except Exception as e:
        print(f"An unexpected error occurred during DB initialization: {e}")
    finally:
        if conn: conn.close()

@app.on_event("startup")
def startup_event():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print("Database connection successful.")
            init_db() # Call init_db after successful connection
            break
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying... ({retries-1} retries left)")
            retries -= 1
            time.sleep(5)
    if retries == 0:
        print("Failed to connect to database after multiple retries. Application might not work as expected.")

def get_db():
    # No PRAGMA foreign_keys = ON for PostgreSQL; it's handled by default or per constraint
    db = psycopg2.connect(DATABASE_URL)
    try:
        yield db
    finally:
        db.close()

@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate, db: psycopg2.extensions.connection = Depends(get_db)):
    created_time = int(time.time())
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "INSERT INTO agent_tasks(title, prompt, status, created_unix, assigned_agent) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (task_data.title, task_data.prompt, TaskStatus.pending.value, created_time, task_data.assigned_agent)
            )
            task_id_tuple = cursor.fetchone()
            if not task_id_tuple: raise HTTPException(status_code=500, detail="Failed to create task: no ID returned.")
            task_id = task_id_tuple['id']
            # db.commit() # Commit will be done after logs

            mock_logs = [
                (task_id, int(time.time()), LogLevel.info.value, "Task creation process started."),
                (task_id, int(time.time()) + 1, LogLevel.debug.value, f"Task details: {{title: '{task_data.title}'}}"),
                (task_id, int(time.time()) + 2, LogLevel.info.value, "Task successfully submitted to queue."),
            ]
            # Use executemany for PostgreSQL for inserting logs
            insert_log_query = "INSERT INTO task_logs (task_id, timestamp, level, message) VALUES (%s, %s, %s, %s)"
            cursor.executemany(insert_log_query, mock_logs)
            db.commit() # Commit both task and its logs together

            cursor.execute("SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix FROM agent_tasks WHERE id = %s", (task_id,))
            created_task_row = cursor.fetchone()
            if not created_task_row: raise HTTPException(status_code=500, detail="Failed to retrieve task after creation.")
            # Pydantic model will validate the row
            return Task(**dict(created_task_row))
    except psycopg2.Error as e:
        if db: db.rollback() # Rollback in case of DB error
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if db: db.rollback() # Rollback for other errors too
        raise HTTPException(status_code=500, detail=f"Unexpected error during task creation: {str(e)}")

@app.post("/api/tasks/{parent_task_id}/subtasks", response_model=Task, status_code=201)
async def dispatch_subtask(
    parent_task_id: int,
    subtask_data: SubTaskCreate,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    created_time = int(time.time())
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            # Check if parent task exists
            cursor.execute("SELECT id, status FROM agent_tasks WHERE id = %s", (parent_task_id,))
            parent_task = cursor.fetchone()
            if not parent_task:
                raise HTTPException(status_code=404, detail=f"Parent task with ID {parent_task_id} not found.")

            # Insert the subtask
            cursor.execute(
                "INSERT INTO agent_tasks(title, prompt, status, created_unix, assigned_agent, parent_task_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (subtask_data.title, subtask_data.prompt, TaskStatus.pending.value, created_time, subtask_data.assigned_agent, parent_task_id)
            )
            subtask_id_tuple = cursor.fetchone()
            if not subtask_id_tuple:
                raise HTTPException(status_code=500, detail="Failed to create subtask: no ID returned.")
            subtask_id = subtask_id_tuple['id']
            db.commit() # Commit the subtask creation

            # Fetch and return the created subtask
            # Ensure all fields required by the Task Pydantic model are selected
            cursor.execute(
                "SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix, parent_task_id, dependency_ids, retry_count FROM agent_tasks WHERE id = %s",
                (subtask_id,)
            )
            created_subtask_row = cursor.fetchone()
            if not created_subtask_row:
                # This should ideally not happen if RETURNING id worked and commit was successful
                raise HTTPException(status_code=500, detail="Failed to retrieve subtask after creation.")
            return Task(**dict(created_subtask_row))
    except psycopg2.Error as e:
        if db: db.rollback()
        # It's good practice to log the actual database error on the server side
        # logger.error(f"Database error dispatching subtask: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException: # Re-raise HTTPException to ensure FastAPI handles it correctly
        raise
    except Exception as e:
        if db: db.rollback()
        # logger.error(f"Unexpected error dispatching subtask: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error dispatching subtask: {str(e)}")

@app.get("/api/tasks", response_model=List[Task])
async def list_tasks(db: psycopg2.extensions.connection = Depends(get_db)):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix FROM agent_tasks ORDER BY created_unix DESC")
            tasks_rows = cursor.fetchall()
            return [Task(**dict(row)) for row in tasks_rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error listing tasks: {str(e)}")

@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: psycopg2.extensions.connection = Depends(get_db)):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix FROM agent_tasks WHERE id = %s", (task_id,))
            task_row = cursor.fetchone()
            if task_row is None: raise HTTPException(status_code=404, detail="Task not found")
            return Task(**dict(task_row))
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error getting task: {str(e)}")

@app.get("/api/tasks/{task_id}/logs", response_model=List[LogEntry])
async def get_task_logs(task_id: int, db: psycopg2.extensions.connection = Depends(get_db)): # Renamed from get_task_logs_endpoint for consistency
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id FROM agent_tasks WHERE id = %s", (task_id,))
            if cursor.fetchone() is None: raise HTTPException(status_code=404, detail="Task not found, so logs cannot be retrieved")

            cursor.execute("SELECT id, task_id, timestamp, level, message FROM task_logs WHERE task_id = %s ORDER BY timestamp ASC", (task_id,))
            log_rows = cursor.fetchall()
            return [LogEntry(**dict(row)) for row in log_rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error getting logs: {str(e)}")

@app.get("/api/tasks/{parent_task_id}/subtasks_status", response_model=List[SubTaskStatusInfo])
async def get_subtasks_status(
    parent_task_id: int,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            # Check if parent task exists
            cursor.execute("SELECT id FROM agent_tasks WHERE id = %s", (parent_task_id,))
            parent_task = cursor.fetchone()
            if not parent_task:
                raise HTTPException(status_code=404, detail=f"Parent task with ID {parent_task_id} not found.")

            # Fetch status and title for subtasks of the parent task
            cursor.execute(
                "SELECT id, status, title FROM agent_tasks WHERE parent_task_id = %s ORDER BY id ASC",
                (parent_task_id,)
            )
            subtasks_rows = cursor.fetchall()
            # Pydantic will validate each dict against SubTaskStatusInfo
            return [dict(row) for row in subtasks_rows]
    except psycopg2.Error as e:
        # logger.error(f"Database error getting subtasks status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException: # Re-raise HTTPException to allow FastAPI to handle it
        raise
    except Exception as e:
        # logger.error(f"Unexpected error getting subtasks status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error fetching subtasks status: {str(e)}")

@app.post("/api/tasks/{task_id}/approve", response_model=Task)
async def approve_task_plan(
    task_id: int,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            # Using FOR UPDATE to lock the row if the DB supports it and it's truly needed.
            # PostgreSQL supports FOR UPDATE. This prevents race conditions if multiple entities try to approve.
            cursor.execute(
                "SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix, parent_task_id, dependency_ids, retry_count FROM agent_tasks WHERE id = %s FOR UPDATE",
                (task_id,)
            )
            task_row = cursor.fetchone()
            if not task_row:
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")

            current_task_dict = dict(task_row) # Convert row to dict to access status
            current_task_status_str = current_task_dict.get("status")

            # Check if the task is actually in 'pending_approval' status
            if current_task_status_str != TaskStatus.pending_approval.value:
                raise HTTPException(
                    status_code=400, # Bad Request
                    detail=f"Task {task_id} cannot be approved. It is not in 'pending_approval' state. Current status: '{current_task_status_str}'"
                )

            # Update the status to 'approved'
            cursor.execute(
                "UPDATE agent_tasks SET status = %s WHERE id = %s",
                (TaskStatus.approved.value, task_id)
            )

            # Fetch the updated task row to return it
            cursor.execute(
                "SELECT id, title, prompt, status, created_unix, assigned_agent, completed_unix, parent_task_id, dependency_ids, retry_count FROM agent_tasks WHERE id = %s",
                (task_id,)
            )
            updated_task_row_dict = cursor.fetchone()
            db.commit() # Commit the transaction

            if not updated_task_row_dict:
                # This should not happen if the update was successful and the task exists
                raise HTTPException(status_code=500, detail="Failed to retrieve task after approval.")
            return Task(**dict(updated_task_row_dict)) # Ensure it's a dict for Pydantic

    except psycopg2.Error as e:
        if db: db.rollback()
        # logger.error(f"Database error approving task {task_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as http_exc: # Re-raise HTTPException
        if db: db.rollback() # Rollback if transaction was started
        raise http_exc
    except Exception as e:
        if db: db.rollback()
        # logger.error(f"Unexpected error approving task {task_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error approving task: {str(e)}")

@app.get("/api/agents", response_model=List[Agent])
async def list_agents(db: psycopg2.extensions.connection = Depends(get_db)):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id, service_name, description, host, port, registered_unix FROM registry_services ORDER BY registered_unix DESC")
            services_rows = cursor.fetchall()
            agents_list = []
            for service_row_map_dict in map(dict, services_rows):
                service_row_map_dict['name'] = service_row_map_dict.pop('service_name')
                service_row_map_dict['status'] = AgentStatus.idle.value
                agents_list.append(Agent(**service_row_map_dict))
            return agents_list
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error listing agents: {str(e)}")

# End of ui/dispatcher/app.py
