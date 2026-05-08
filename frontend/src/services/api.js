import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
};

export const coursesAPI = {
  getAll: () => api.get('/courses/'),
  create: (course) => api.post('/courses/', course),
  update: (id, course) => api.put(`/courses/${id}/`, course),
  delete: (id) => api.delete(`/courses/${id}/`),
};

export const tasksAPI = {
  getAll: () => api.get('/tasks/'),
  create: (task) => api.post('/tasks/', task),
  update: (id, task) => api.put(`/tasks/${id}/`, task),
};

export const aiAPI = {
  generateStudyPlan: (data) => api.post('/ai/study-plan/', data),
  generateSummary: (text) => api.post('/ai/summary/', { text }),
  generateQuiz: (topic) => api.post('/ai/quiz/', { topic }),
};

export default api;