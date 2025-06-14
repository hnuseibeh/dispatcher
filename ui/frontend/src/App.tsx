import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link as RouterLink } from 'react-router-dom';
import { Box, Drawer, AppBar, Toolbar, List, ListItemButton, ListItemIcon, ListItemText, Typography, CssBaseline } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import PeopleIcon from '@mui/icons-material/People'; // Import PeopleIcon
import TaskDashboardPage from './pages/TaskDashboardPage';
import TaskSubmissionPage from './pages/TaskSubmissionPage';
import TaskDetailPage from './pages/TaskDetailPage';
import AgentRegistryPage from './pages/AgentRegistryPage'; // Import AgentRegistryPage

const drawerWidth = 240;

function App() {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar
          position="fixed"
          sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
        >
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              Task Management App
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
          variant="permanent"
          anchor="left"
        >
          <Toolbar />
          <List>
            <ListItemButton component={RouterLink} to="/">
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Task Dashboard" />
            </ListItemButton>
            <ListItemButton component={RouterLink} to="/submit-task"> {/* New Nav Item */}
              <ListItemIcon>
                <AddCircleOutlineIcon />
              </ListItemIcon>
              <ListItemText primary="Submit New Task" />
            </ListItemButton>
            <ListItemButton component={RouterLink} to="/agents"> {/* New Nav Item for Agents */}
              <ListItemIcon>
                <PeopleIcon />
              </ListItemIcon>
              <ListItemText primary="Agent Registry" />
            </ListItemButton>
          </List>
        </Drawer>
        <Box
          component="main"
          sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
        >
          <Toolbar /> {/* Spacer for AppBar */}
          <Routes>
            <Route path="/" element={<TaskDashboardPage />} />
            <Route path="/submit-task" element={<TaskSubmissionPage />} />
            <Route path="/task/:taskId" element={<TaskDetailPage />} />
            <Route path="/agents" element={<AgentRegistryPage />} /> {/* New Route for Agents */}
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
