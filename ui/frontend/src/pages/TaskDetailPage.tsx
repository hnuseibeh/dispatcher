import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  CircularProgress,
  Alert,
  Box,
  Paper,
  Grid,
  Divider,
} from '@mui/material';
import { Task } from '../types';
import { getTaskById } from '../services/api';
import LogViewer from '../components/LogViewer'; // Import LogViewer

const TaskDetailPage: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const [task, setTask] = useState<Task | null | undefined>(undefined); // undefined for not found, null for loading
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTask = async () => {
      if (!taskId) {
        setError('Task ID is missing.');
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setError(null);
        const fetchedTask = await getTaskById(taskId);
        setTask(fetchedTask);
      } catch (err) {
        setError('Failed to fetch task details. Please try again later.');
        console.error(err);
        setTask(null); // Explicitly set to null on error to differentiate from not found
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  if (loading || task === null) { // task === null means still loading initially or error occurred
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error && task === null) { // Show error only if task is also null (meaning error during fetch)
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (task === undefined) { // Task explicitly not found by API
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="warning">Task with ID "{taskId}" not found.</Alert>
      </Container>
    );
  }

  // Defensive check for task, though covered by above states
  if (!task) {
     return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="info">No task data available.</Alert>
      </Container>
    );
  }


  return (
    <Container maxWidth="lg" sx={{ my: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Task Details: {task.title}
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>Basic Information</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}><Typography><strong>ID:</strong> {task.id}</Typography></Grid>
          <Grid item xs={12} sm={6}><Typography><strong>Status:</strong> {task.status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</Typography></Grid>
          <Grid item xs={12} sm={6}><Typography><strong>Agent:</strong> {task.agent || 'N/A'}</Typography></Grid>
          <Grid item xs={12} sm={6}><Typography><strong>Created At:</strong> {new Date(task.created_at).toLocaleString()}</Typography></Grid>
          <Grid item xs={12} sm={6}><Typography><strong>Completed At:</strong> {task.completed_at ? new Date(task.completed_at).toLocaleString() : 'N/A'}</Typography></Grid>
        </Grid>
      </Paper>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px', display: 'flex', flexDirection: 'column' }}>
            {/* LogViewer will take full height of this Paper */}
            {taskId && <LogViewer taskId={taskId} />}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px' }}> {/* Matched height for consistency */}
            <Typography variant="h6" gutterBottom>Plan (PLAN.md)</Typography>
            <Divider sx={{ mb: 1 }}/>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', maxHeight: 330, overflowY: 'auto' }}>
              Placeholder for PLAN.md content...
              {/* Real plan content would be loaded here */}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px' }}> {/* Matched height for consistency */}
            <Typography variant="h6" gutterBottom>Report (REPORT.md)</Typography>
            <Divider sx={{ mb: 1 }}/>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', maxHeight: 330, overflowY: 'auto' }}>
              Placeholder for REPORT.md content...
              {/* Real report content would be loaded here */}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default TaskDetailPage;
