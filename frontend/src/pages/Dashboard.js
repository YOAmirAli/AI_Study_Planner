import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import { coursesAPI, tasksAPI } from '../services/api';
import TaskList from '../components/TaskList';
import ProgressChart from '../components/ProgressChart';
import UpcomingDeadlines from '../components/UpcomingDeadlines';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [tasksRes, coursesRes] = await Promise.all([
        tasksAPI.getAll(),
        coursesAPI.getAll(),
      ]);
      setTasks(tasksRes.data);
      setCourses(coursesRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Student Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Upcoming Tasks</Typography>
            <TaskList tasks={tasks.filter(t => t.status !== 'completed')} />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Progress Overview</Typography>
            <ProgressChart tasks={tasks} />
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Upcoming Deadlines</Typography>
            <UpcomingDeadlines tasks={tasks} />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;