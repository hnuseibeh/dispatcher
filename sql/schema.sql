
-- schema.sql
PRAGMA foreign_keys = ON;

/* Core task tables */
CREATE TABLE IF NOT EXISTS agent_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending','approved','in_progress','done','failed')) NOT NULL DEFAULT 'pending',
    created_unix INTEGER NOT NULL,
    assigned_agent TEXT,
    completed_unix INTEGER
);

/* Service registry */
CREATE TABLE IF NOT EXISTS registry_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL UNIQUE,
    description TEXT,
    host TEXT DEFAULT 'localhost',
    port INTEGER NOT NULL UNIQUE,
    registered_unix INTEGER NOT NULL
);
