-- Updated agent_tasks table with subtask relationships
ALTER TABLE agent_tasks ADD COLUMN parent_task_id TEXT;
ALTER TABLE agent_tasks ADD COLUMN dependency_ids TEXT; -- Comma-separated list