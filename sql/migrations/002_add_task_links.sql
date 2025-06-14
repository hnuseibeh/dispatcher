-- Add parent_task_id and status for subtasks
ALTER TABLE agent_tasks ADD COLUMN parent_task_id TEXT;
ALTER TABLE agent_tasks ADD COLUMN dependency_ids TEXT;
ALTER TABLE agent_tasks ADD COLUMN retry_count INTEGER DEFAULT 0;
