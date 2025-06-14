import React, { useEffect, useState, useRef, useCallback } from 'react';
import { Paper, Typography, Box, IconButton, Tooltip } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import { LogEntry } from '../types';
import { getTaskLogs } from '../services/api';

interface LogViewerProps {
  taskId: string;
}

const LogViewer: React.FC<LogViewerProps> = ({ taskId }) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [lastFetchedTimestamp, setLastFetchedTimestamp] = useState<string | undefined>();
  const [isPolling, setIsPolling] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const userScrolledUpRef = useRef<boolean>(false);

  const handleScroll = () => {
    if (scrollRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
      // Consider user scrolled up if not near the bottom (e.g., within 20px)
      userScrolledUpRef.current = scrollHeight - scrollTop - clientHeight > 20;
    }
  };

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current && !userScrolledUpRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  const fetchLogs = useCallback(async (isInitialFetch = false) => {
    if (!taskId) return;
    try {
      const newLogs = await getTaskLogs(taskId, isInitialFetch ? undefined : lastFetchedTimestamp);
      if (newLogs.length > 0) {
        setLogs((prevLogs) => [...prevLogs, ...newLogs]);
        setLastFetchedTimestamp(newLogs[newLogs.length - 1].timestamp);
      }
      setError(null);
    } catch (err) {
      console.error('Failed to fetch logs:', err);
      setError('Failed to fetch logs.');
      // Consider stopping polling on error or implementing retry logic
    }
  }, [taskId, lastFetchedTimestamp]);

  useEffect(() => {
    setLogs([]); // Clear logs when taskId changes
    setLastFetchedTimestamp(undefined);
    userScrolledUpRef.current = false;
    fetchLogs(true); // Initial fetch
  }, [taskId, fetchLogs]);

  useEffect(() => {
    if (isPolling) {
      const intervalId = setInterval(() => fetchLogs(), 3000); // Poll every 3 seconds
      return () => clearInterval(intervalId);
    }
  }, [isPolling, fetchLogs]);

  useEffect(() => {
    scrollToBottom();
  }, [logs, scrollToBottom]);


  const formatTimestamp = (isoString: string) => {
    return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', fractionalSecondDigits: 3 });
  };

  return (
    <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="h6" component="div">
          Live Logs
        </Typography>
        <Tooltip title={isPolling ? "Pause Polling" : "Resume Polling"}>
          <IconButton onClick={() => setIsPolling(!isPolling)} size="small">
            {isPolling ? <PauseIcon /> : <PlayArrowIcon />}
          </IconButton>
        </Tooltip>
      </Box>
      {error && <Typography color="error" variant="caption">{error}</Typography>}
      <Paper
        variant="outlined"
        sx={{
          flexGrow: 1,
          overflowY: 'auto',
          p: 1.5,
          fontFamily: 'monospace',
          fontSize: '0.875rem',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-all',
          backgroundColor: '#f5f5f5', // Light grey background for the log area
        }}
        ref={scrollRef}
        onScroll={handleScroll}
      >
        {logs.length === 0 && !error && <Typography variant="body2">No logs yet...</Typography>}
        {logs.map((log) => (
          <Box key={log.id} sx={{ mb: 0.5 }}>
            <Typography
              variant="caption"
              sx={{
                color: log.level === 'ERROR' ? 'red' : log.level === 'WARNING' ? 'orange' : 'inherit',
                fontWeight: log.level === 'ERROR' || log.level === 'WARNING' ? 'bold' : 'normal'
              }}
            >
              [{formatTimestamp(log.timestamp)}] [{log.level || 'INFO'}] {log.message}
            </Typography>
          </Box>
        ))}
      </Paper>
    </Paper>
  );
};

export default LogViewer;
