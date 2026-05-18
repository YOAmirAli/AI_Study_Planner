import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Courses from './pages/Courses'
import Tasks from './pages/Tasks'
import Schedule from './pages/Schedule'
import AIFeatures from './pages/AIFeatures'
import Groups from './pages/Groups'
import Resources from './pages/Resources'
import Quizzes from './pages/Quizzes'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-900">
        <div className="relative">
          <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-indigo-600"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-8 w-8 bg-indigo-600 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to="/" />} />
      
      <Route element={user ? <MainLayout /> : <Navigate to="/login" />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/ai-features" element={<AIFeatures />} />
        <Route path="/groups" element={<Groups />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/quizzes" element={<Quizzes />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
    </Routes>
  )
}

export default App