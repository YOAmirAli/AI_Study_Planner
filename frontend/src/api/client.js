import axios from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
      toast.error('Session expired. Please login again.')
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
}

// User API (for profile management)
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  changePassword: (data) => api.put('/users/password', data),
  deleteAccount: () => api.delete('/users/account'),
}

// Course API
export const courseAPI = {
  getAll: () => api.get('/courses'),
  getById: (id) => api.get(`/courses/${id}`),
  create: (data) => api.post('/courses', data),
  update: (id, data) => api.put(`/courses/${id}`, data),
  delete: (id) => api.delete(`/courses/${id}`),
}

// Task API
export const taskAPI = {
  getAll: (params) => api.get('/tasks', { params }),
  getById: (id) => api.get(`/tasks/${id}`),
  create: (data) => api.post('/tasks', data),
  update: (id, data) => api.put(`/tasks/${id}`, data),
  delete: (id) => api.delete(`/tasks/${id}`),
  complete: (id, data) => api.patch(`/tasks/${id}/complete`, data),
  getUpcoming: (days) => api.get('/tasks/upcoming', { params: { days } }),
  getOverdue: () => api.get('/tasks/overdue'),
}

// Schedule API
export const scheduleAPI = {
  getWeekly: (weekStart) => api.get('/schedules', { params: { week_start: weekStart } }),
  generate: (data) => api.post('/schedules/generate', data),
  create: (data) => api.post('/schedules', data),
  update: (id, data) => api.put(`/schedules/${id}`, data),
  delete: (id) => api.delete(`/schedules/${id}`),
}

// AI API
export const aiAPI = {
  summarize: (formData) => api.post('/ai/summarize', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  generateQuiz: (formData) => api.post('/ai/generate-quiz', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  generateFlashcards: (formData) => api.post('/ai/create-flashcards', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  recommendMaterials: (data) => api.post('/ai/recommend-materials', data),
  taskTutor: (data) => api.post('/ai/task-tutor', data),
  suggestTasks: (data) => api.post('/ai/suggest-tasks', data),
}

// Group API
export const groupAPI = {
  getAll: () => api.get('/groups'),
  getById: (id) => api.get(`/groups/${id}`),
  create: (data) => api.post('/groups', data),
  update: (id, data) => api.put(`/groups/${id}`, data),
  delete: (id) => api.delete(`/groups/${id}`),
  join: (id) => api.post(`/groups/${id}/join`),
  joinByCode: (data) => api.post('/groups/join', data),
  leave: (id) => api.post(`/groups/${id}/leave`),
  getMessages: (groupId, params) => api.get(`/groups/${groupId}/messages`, { params }),
  sendMessage: (groupId, data) => api.post(`/groups/${groupId}/messages`, data),
  deleteMessage: (groupId, messageId) => api.delete(`/groups/${groupId}/messages/${messageId}`),
  getResources: (groupId) => api.get(`/groups/${groupId}/resources`),
  shareResource: (groupId, data) => api.post(`/groups/${groupId}/resources`, data),
  deleteResource: (groupId, resourceId) => api.delete(`/groups/${groupId}/resources/${resourceId}`),
  getLeaderboard: (groupId) => api.get(`/groups/${groupId}/leaderboard`),
  getActivity: (groupId) => api.get(`/groups/${groupId}/activity`),
  markMessagesRead: (groupId) => api.post(`/groups/${groupId}/messages/mark-read`),
  getUnreadCount: (groupId) => api.get(`/groups/${groupId}/messages/unread-count`),
}

// Resource API
export const resourceAPI = {
  getAll: (params) => api.get('/resources', { params }),
  getById: (id) => api.get(`/resources/${id}`),
  create: (data) => api.post('/resources', data),
  update: (id, data) => api.put(`/resources/${id}`, data),
  delete: (id) => api.delete(`/resources/${id}`),
  toggleFavorite: (id) => api.post(`/resources/${id}/favorite`),
}

// Quiz API
export const quizAPI = {
  getAll: (params) => api.get('/quizzes', { params }),
  getById: (id) => api.get(`/quizzes/${id}`),
  generate: (data) => api.post('/quizzes/generate', data),
  start: (id) => api.post(`/quizzes/${id}/start`),
  submit: (id, data) => api.post(`/quizzes/${id}/submit`, data),
  delete: (id) => api.delete(`/quizzes/${id}`),
  getPendingCount: () => api.get('/quizzes/pending-count'),
}

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/progress/dashboard'),
  getAnalytics: () => api.get('/progress/analytics'),
  logSession: (data) => api.post('/progress/session', data),
  getSessions: (limit) => api.get('/progress/sessions', { params: { limit } }),
  getPrediction: (expectedHours) => api.get('/progress/prediction', { params: { expected_hours: expectedHours } }),
  getWeeklySummary: () => api.get('/progress/weekly-summary'),
}

// Notification API
export const notificationAPI = {
  getAll: (params) => api.get('/notifications', { params }),
  markRead: (id) => api.patch(`/notifications/${id}/read`),
  markAllRead: () => api.patch('/notifications/mark-all-read'),
  delete: (id) => api.delete(`/notifications/${id}`),
  clearAllRead: () => api.delete('/notifications/clear-all'),
}

// Default export
export default api
