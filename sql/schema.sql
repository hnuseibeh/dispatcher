-- sql/schema.sql

CREATE TABLE IF NOT EXISTS agent_tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending','approved','in_progress','done','failed','pending_approval')) NOT NULL DEFAULT 'pending',
    created_unix INTEGER NOT NULL,
    assigned_agent TEXT,
    completed_unix INTEGER,
    parent_task_id INTEGER REFERENCES agent_tasks(id) ON DELETE SET NULL,
    dependency_ids TEXT, -- For comma-separated IDs or similar
    retry_count INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS task_logs (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES agent_tasks(id) ON DELETE CASCADE,
    timestamp INTEGER NOT NULL,
    level TEXT CHECK(level IN ('INFO', 'WARNING', 'ERROR', 'DEBUG')) NOT NULL DEFAULT 'INFO',
    message TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_task_logs_task_id ON task_logs(task_id);
CREATE INDEX IF NOT EXISTS idx_task_logs_timestamp ON task_logs(timestamp);

CREATE TABLE IF NOT EXISTS registry_services (
    id SERIAL PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    description TEXT,
    host TEXT DEFAULT 'localhost',
    port INTEGER NOT NULL UNIQUE,
    registered_unix INTEGER NOT NULL
);
