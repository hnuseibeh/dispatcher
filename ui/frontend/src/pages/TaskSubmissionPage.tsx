import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Box,
  SelectChangeEvent,
} from '@mui/material';

// Mock agent list - in a real app, this might come from an API or config
const availableAgents = ['Agent Smith', 'Agent Jones', 'Agent Brown', 'Unassigned'];

interface TaskFormData {
  title: string;
  prompt: string;
  agent: string;
}

const TaskSubmissionPage: React.FC = () => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    prompt: '',
    agent: 'Unassigned', // Default to Unassigned
  });

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<string>
  ) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name!]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log('Task Submission Data:', formData);
    // Here you would typically call an API to submit the task
    // For now, we just log and could potentially reset the form
    alert(`Task "${formData.title}" submitted! Check console for data.`);
    setFormData({ title: '', prompt: '', agent: 'Unassigned' }); // Reset form
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Submit New Task
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Task Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            fullWidth
            required
            margin="normal"
          />
          <TextField
            label="Task Prompt / Description"
            name="prompt"
            value={formData.prompt}
            onChange={handleChange}
            fullWidth
            required
            multiline
            rows={4}
            margin="normal"
          />
          <FormControl fullWidth margin="normal" required>
            <InputLabel id="agent-select-label">Assign to Agent</InputLabel>
            <Select
              labelId="agent-select-label"
              id="agent-select"
              name="agent"
              value={formData.agent}
              label="Assign to Agent"
              onChange={handleChange}
            >
              {availableAgents.map((agentName) => (
                <MenuItem key={agentName} value={agentName}>
                  {agentName}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Box sx={{ mt: 3 }}>
            <Button type="submit" variant="contained" color="primary" size="large">
              Submit Task
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
};

export default TaskSubmissionPage;
