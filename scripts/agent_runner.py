# scripts/agent_runner.py
import os
import psycopg2
from psycopg2.extras import DictCursor
import time
import pathlib
import re # For filename sanitization
from core.rag.kernel import RAGKernel
import logging

# Initialize logger for the module. Configuration will be done in main or if __name__ == "__main__"
logger = logging.getLogger(__name__)

BASE = pathlib.Path(__file__).resolve().parents[1]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zaki_user:zaki_password@localhost:5432/zaki_os_db")

def get_next_task():
    conn = None
    # Logger is fetched here to ensure it uses the config from main() or __main__ block if they've run
    logger_get_task = logging.getLogger(__name__)
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            logger_get_task.debug("get_next_task: Looking for tasks with status 'approved'.")
            cursor.execute("SELECT id, title, prompt FROM agent_tasks WHERE status='approved' ORDER BY created_unix LIMIT 1")
            row = cursor.fetchone()
        return row
    except psycopg2.Error as e:
        logger_get_task.error(f"Database error in get_next_task: {e}", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def mark_status(task_id: int, status_value: str):
    conn = None
    logger_mark_status = logging.getLogger(__name__)
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cursor:
            # For "done", completed_unix is updated. For other statuses, it might not be.
            # The original subtask implies only 'done' updates completed_unix.
            # For 'pending_approval' or 'in_progress', completed_unix should remain NULL or unchanged.
            if status_value == "done":
                update_query = "UPDATE agent_tasks SET status=%s, completed_unix=%s WHERE id=%s"
                params = (status_value, int(time.time()), task_id)
            else:
                update_query = "UPDATE agent_tasks SET status=%s WHERE id=%s"
                params = (status_value, task_id)
            cursor.execute(update_query, params)
        conn.commit()
    except psycopg2.Error as e:
        logger_mark_status.error(f"Database error in mark_status for task {task_id} to status {status_value}: {e}", exc_info=True)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def sanitize_filename(name_base: str, task_id: int, extension: str = ".md", max_length: int = 100) -> str:
    name_base = re.sub(r'[^\w\s-]', '', name_base)
    name_base = re.sub(r'\s+', '_', name_base)
    max_name_base_len = max_length - len(str(task_id)) - len(extension) -1
    if len(name_base) > max_name_base_len:
        name_base = name_base[:max_name_base_len]
    return f"{name_base}_{task_id}{extension}"

def main():
    # This basicConfig is for the main agent runner logic.
    # The __main__ block has its own for bootstrap/DB check.
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(),
                        format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')
    # Re-fetch logger instance after basicConfig
    logger_main = logging.getLogger(__name__)
    logger_main.info("Agent Runner - Main process started.")

    rag_kernel = None
    try:
        logger_main.info("Initializing RAG Kernel...")
        rag_kernel = RAGKernel()
        rag_kernel.initialize_and_embed_lessons()
        logger_main.info("RAG Kernel initialization and lesson embedding process completed.")
    except Exception as e:
        logger_main.error(f"Failed to initialize RAG Kernel or embed lessons: {e}", exc_info=True)

    logger_main.info("Checking for tasks with status 'approved' to generate plan...")
    task_data = get_next_task()

    if not task_data:
        logger_main.info("No 'approved' tasks found for plan generation, exiting.")
        return

    task_id = task_data['id']
    title = task_data['title']
    prompt = task_data['prompt']
    logger_main.info(f"Processing task ID: {task_id}, Title: '{title}' for plan generation.")

    # Mark task as 'in_progress' while generating the plan
    mark_status(task_id, "in_progress")

    retrieved_lessons_str = "No lessons retrieved. (RAG system might be unavailable or no relevant lessons found)."
    if rag_kernel and rag_kernel.vector_store and rag_kernel.documents_loaded:
        try:
            logger_main.info(f"Querying RAG for lessons relevant to prompt (first 100 chars): '{prompt[:100]}...'")
            relevant_lessons = rag_kernel.get_relevant_lessons(prompt, n_results=3)
            if relevant_lessons:
                logger_main.info(f"Retrieved {len(relevant_lessons)} relevant lessons.")
                retrieved_lessons_summary = []
                for i, lesson in enumerate(relevant_lessons):
                    source = lesson.get('metadata', {}).get('source', 'Unknown source')
                    distance = lesson.get('distance')
                    distance_str = f"{distance:.4f}" if distance is not None else "N/A"
                    content_snippet = lesson.get('document_content', '')[:150].replace('\n', ' ') + "..."
                    retrieved_lessons_summary.append(f"- Source: {source} (Distance: {distance_str})\n  Snippet: {content_snippet}")
                retrieved_lessons_str = "\n".join(retrieved_lessons_summary)
            else:
                logger_main.info("No relevant lessons found by RAG for this prompt.")
                retrieved_lessons_str = "No relevant lessons found by RAG for this prompt."
        except Exception as e:
            logger_main.error(f"Error querying RAG system: {e}", exc_info=True)
            retrieved_lessons_str = f"Error querying RAG system: {str(e)}"
    elif not rag_kernel or not rag_kernel.vector_store:
        logger_main.warning("RAG Kernel or its vector store is not available.")
    elif not rag_kernel.documents_loaded:
        logger_main.warning("RAG documents were not loaded properly.")

    plans_dir = BASE / "docs" / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)

    # Use sanitize_filename for plan_filename
    plan_filename = sanitize_filename(f"PLAN_{title}", task_id)
    plan_path = plans_dir / plan_filename

    plan_content = f"# PLAN for Task {task_id}: {title}\n\n## Original Prompt:\n```\n{prompt}\n```\n\n## Relevant Lessons from RAG System:\n{retrieved_lessons_str}\n\n## Proposed Plan Steps:\n1. [TODO: Define actual plan steps based on prompt and RAG insights]\n2. [TODO: Further breakdown]\n"
    plan_path.write_text(plan_content)
    logger_main.info(f"PLAN created at '{plan_path}'.")

    # Update task status to 'pending_approval'
    mark_status(task_id, "pending_approval")
    logger_main.info(f"Task {task_id} ('{title}') status updated to 'pending_approval'. Agent will stop here. Waiting for approval via API call to resume processing.")

    # Work simulation, report generation, and marking 'done' are removed from here.
    # This script will now exit after setting status to 'pending_approval'.
    # A future version of the agent or a different agent instance will pick up 'approved' tasks to execute them.

if __name__ == "__main__":
    log_level_main_check = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level_main_check,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s - %(message)s')
    logger_bootstrap_check = logging.getLogger(__name__ + "._bootstrap_check")

    db_connected = False
    retries = 5
    logger_bootstrap_check.info("Agent Runner bootstrap: Initiating database connection check...")
    while retries > 0 and not db_connected:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            logger_bootstrap_check.info("Database connection successful. Agent runner can proceed.")
            db_connected = True
        except psycopg2.OperationalError as e:
            logger_bootstrap_check.warning(f"Database connection failed: {e}. Retrying in 5 seconds... ({retries} retries left)")
            retries -= 1
            if retries > 0:
                time.sleep(5)

    if db_connected:
        main()
    else:
        logger_bootstrap_check.critical("Failed to connect to database after multiple retries. Agent runner cannot start.")
