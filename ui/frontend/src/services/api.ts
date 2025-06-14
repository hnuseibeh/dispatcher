import { Task, Agent, LogEntry } from '../types'; // Moved Agent here, Added LogEntry

const sampleTasks: Task[] = [
  {
    id: '1',
    title: 'Develop UI for task dashboard',
    status: 'in_progress',
    agent: 'Agent Smith',
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
    completed_at: null,
  },
  {
    id: '2',
    title: 'Setup backend API for tasks',
    status: 'pending',
    agent: null,
    created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
    completed_at: null,
  },
  {
    id: '3',
    title: 'Write documentation for API',
    status: 'completed',
    agent: 'Agent Brown',
    created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 7 days ago
    completed_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
  },
  {
    id: '4',
    title: 'Deploy application to staging',
    status: 'pending_approval',
    agent: 'Agent Smith',
    created_at: new Date(Date.now() - 0.5 * 24 * 60 * 60 * 1000).toISOString(), // 12 hours ago
    completed_at: null,
  }
];

export const getTasks = (): Promise<Task[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([...sampleTasks]); // Return a copy to prevent modification of the original array
    }, 1000); // Simulate 1 second delay
  });
};

export const getTaskById = (taskId: string): Promise<Task | undefined> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const task = sampleTasks.find((t) => t.id === taskId);
      resolve(task);
    }, 500); // Simulate 0.5 seconds delay
  });
};

// In the future, we might add functions to create, update, delete tasks, e.g.:
// export const createTask = (taskData: Omit<Task, 'id' | 'created_at' | 'completed_at'>): Promise<Task> => { ... }
// export const updateTask = (taskId: string, updates: Partial<Task>): Promise<Task> => { ... }

const sampleAgents: Agent[] = [
  {
    id: 'agent-001',
    name: 'Agent Smith',
    status: 'busy',
    current_task_id: '1',
  },
  {
    id: 'agent-002',
    name: 'Agent Jones',
    status: 'idle',
    current_task_id: null,
  },
  {
    id: 'agent-003',
    name: 'Agent Brown',
    status: 'offline',
    current_task_id: null,
  },
];

export const getAgents = (): Promise<Agent[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([...sampleAgents]);
    }, 800); // Simulate 0.8 seconds delay
  });
};

// --- Mock Log Service ---
interface MockLogBuffer {
  [taskId: string]: LogEntry[];
}
const mockLogStore: MockLogBuffer = {};
let logIdCounter = 0;

const generateInitialLogs = (taskId: string): LogEntry[] => {
  const now = Date.now();
  return [
    { id: `log-${logIdCounter++}`, taskId, timestamp: new Date(now - 5000).toISOString(), message: `Task ${taskId} initiated.`, level: 'INFO' },
    { id: `log-${logIdCounter++}`, taskId, timestamp: new Date(now - 4000).toISOString(), message: 'Fetching prerequisites...', level: 'DEBUG' },
    { id: `log-${logIdCounter++}`, taskId, timestamp: new Date(now - 3000).toISOString(), message: 'Prerequisites found. Starting execution.', level: 'INFO' },
  ];
};

export const getTaskLogs = (taskId: string, since?: string): Promise<LogEntry[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (!mockLogStore[taskId]) {
        mockLogStore[taskId] = generateInitialLogs(taskId);
      }

      // Simulate new log generation
      const newLog: LogEntry = {
        id: `log-${logIdCounter++}`,
        taskId,
        timestamp: new Date().toISOString(),
        message: `Executing step ${mockLogStore[taskId].length + 1}...`,
        level: Math.random() < 0.1 ? 'WARNING' : (Math.random() < 0.05 ? 'ERROR' : 'INFO'),
      };
      if (Math.random() < 0.2) {
        newLog.message = `Detailed debug information for step ${mockLogStore[taskId].length + 1}: parameter_x = ${Math.random().toFixed(3)}`;
        newLog.level = 'DEBUG';
      }
      mockLogStore[taskId].push(newLog);

      if (since) {
        const sinceTimestamp = new Date(since).getTime();
        const newLogs = mockLogStore[taskId].filter(log => new Date(log.timestamp).getTime() > sinceTimestamp);
        resolve(newLogs);
      } else {
        resolve([...mockLogStore[taskId]]);
      }
    }, 750); // Simulate network delay for log fetching
  });
};
