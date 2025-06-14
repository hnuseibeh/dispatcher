export interface Task {
  id: string; // Or number, to be aligned with backend
  title: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'pending_approval';
  agent: string | null;
  created_at: string; // ISO date string
  completed_at: string | null; // ISO date string
}

export interface Agent {
  id: string;
  name: string;
  status: 'idle' | 'busy' | 'offline';
  current_task_id: string | null;
}

export interface LogEntry {
  id: string;
  taskId?: string; // Added to associate log with a task, optional if globally unique IDs
  timestamp: string; // ISO date string
  message: string;
  level?: 'INFO' | 'WARNING' | 'ERROR' | 'DEBUG'; // Defaults to 'INFO'
}
