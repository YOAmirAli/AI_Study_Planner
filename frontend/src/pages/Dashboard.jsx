import React, { useState, useEffect } from 'react'
import {
  BookOpen, CheckCircle, Clock, Calendar, TrendingUp, Award,
  Brain, Zap, Target, BarChart3, ArrowUpRight, ArrowDownRight,
  Activity, Users, Flame, Sparkles
} from 'lucide-react'
import { analyticsAPI, taskAPI } from '../api/client'
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, RadialBarChart, RadialBar
} from 'recharts'
import toast from 'react-hot-toast'
const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null)
  const [recentTasks, setRecentTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [weeklyData, setWeeklyData] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [dashboardRes, tasksRes] = await Promise.all([
        analyticsAPI.getDashboard(),
        taskAPI.getAll({ status: 'pending', sort_by: 'deadline' }),
      ])
      
      setDashboardData(dashboardRes.data)
      setRecentTasks(tasksRes.data.tasks?.slice(0, 5) || [])
      
      // Generate weekly data
      setWeeklyData([
        { day: 'Mon', hours: 2.5, tasks: 3 },
        { day: 'Tue', hours: 3.2, tasks: 4 },
        { day: 'Wed', hours: 1.8, tasks: 2 },
        { day: 'Thu', hours: 4.0, tasks: 5 },
        { day: 'Fri', hours: 2.1, tasks: 3 },
        { day: 'Sat', hours: 1.5, tasks: 1 },
        { day: 'Sun', hours: 0.5, tasks: 0 },
      ])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const stats = [
    {
      title: 'Total Courses',
      value: dashboardData?.total_courses || 0,
      icon: BookOpen,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-950/50',
      textColor: 'text-blue-600 dark:text-blue-400',
      change: '+12%',
      trend: 'up'
    },
    {
      title: 'Tasks Completed',
      value: dashboardData?.completed_tasks || 0,
      icon: CheckCircle,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50 dark:bg-green-950/50',
      textColor: 'text-green-600 dark:text-green-400',
      change: '+8%',
      trend: 'up'
    },
    {
      title: 'Study Hours',
      value: dashboardData?.study_hours_this_week || 0,
      icon: Clock,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-950/50',
      textColor: 'text-purple-600 dark:text-purple-400',
      change: '+23%',
      trend: 'up',
      suffix: 'hrs'
    },
    {
      title: 'Completion Rate',
      value: dashboardData?.completion_rate || 0,
      icon: Target,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50 dark:bg-orange-950/50',
      textColor: 'text-orange-600 dark:text-orange-400',
      change: '+5%',
      trend: 'up',
      suffix: '%'
    },
  ]

  const rawPieData = [
    { name: 'Completed', value: dashboardData?.completed_tasks || 0, color: '#10b981' },
    { name: 'In Progress', value: dashboardData?.in_progress || 0, color: '#f59e0b' },
    { name: 'Pending', value: dashboardData?.pending_tasks || 0, color: '#ef4444' },
  ]
  const pieData = rawPieData.filter(item => item.value > 0)
  if (pieData.length === 0) {
    pieData.push({ name: 'No Tasks', value: 1, color: '#e5e7eb' })
  }

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return 'text-red-600 bg-red-100 dark:text-red-300 dark:bg-red-900/40'
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-300 dark:bg-yellow-900/40'
      case 'low': return 'text-green-600 bg-green-100 dark:text-green-300 dark:bg-green-900/40'
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-300 dark:bg-slate-700'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-indigo-600"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <Sparkles className="h-6 w-6 text-indigo-600 animate-pulse" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 text-white shadow-xl">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-indigo-200 text-sm font-semibold uppercase tracking-[0.2em] mb-2">Nova</p>
            <h1 className="text-3xl font-bold mb-2">Welcome back! 👋</h1>
            <p className="text-indigo-100 text-lg">Ready to continue your learning journey?</p>
            <div className="flex gap-4 mt-4">
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2 backdrop-blur-sm">
                <Flame className="h-5 w-5 text-yellow-400" />
                <span className="text-sm font-medium">5 day streak</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2 backdrop-blur-sm">
                <Award className="h-5 w-5 text-yellow-400" />
                <span className="text-sm font-medium">Level 7 Learner</span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="bg-white/20 rounded-full p-3 backdrop-blur-sm">
              <Brain className="h-8 w-8" />
            </div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card card p-6">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-800 dark:text-gray-100 mt-2">
                  {stat.value}{stat.suffix || ''}
                </p>
                <div className="flex items-center gap-1 mt-2">
                  {stat.trend === 'up' ? (
                    <ArrowUpRight className="h-4 w-4 text-green-500" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-500" />
                  )}
                  <span className={`text-xs font-medium ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                    {stat.change}
                  </span>
                  <span className="text-xs text-gray-500">vs last week</span>
                </div>
              </div>
              <div className={`${stat.bgColor} rounded-xl p-3`}>
                <stat.icon className={`h-6 w-6 ${stat.textColor}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Study Hours */}
        <div className="card p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Weekly Study Hours</h3>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Activity className="h-4 w-4" />
              <span>Last 7 days</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={weeklyData}>
              <defs>
                <linearGradient id="colorHours" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  borderRadius: '12px',
                  border: '1px solid #e5e7eb',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Area 
                type="monotone" 
                dataKey="hours" 
                stroke="#6366f1" 
                strokeWidth={2}
                fill="url(#colorHours)" 
                name="Study Hours"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Task Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Task Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={{ stroke: '#9ca3af', strokeWidth: 1 }}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Tasks */}
      <div className="card p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold text-gray-800">Recent Tasks</h3>
          <button className="text-indigo-600 text-sm font-medium hover:text-indigo-700 transition-colors">
            View All →
          </button>
        </div>
        <div className="space-y-3">
          {recentTasks.map((task, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${task.priority === 'high' ? 'bg-red-500' : task.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
                <div>
                  <p className="font-medium text-gray-800">{task.title}</p>
                  <p className="text-sm text-gray-500">Due: {new Date(task.deadline).toLocaleDateString()}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={`badge ${getPriorityColor(task.priority)}`}>
                  {task.priority}
                </span>
                <span className={`badge ${task.status === 'pending' ? 'badge-warning' : 'badge-info'}`}>
                  {task.status}
                </span>
              </div>
            </div>
          ))}
          {recentTasks.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <CheckCircle className="h-12 w-12 mx-auto mb-3 text-gray-400" />
              <p>No pending tasks. Great job! 🎉</p>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card-gradient p-6 text-center group cursor-pointer hover:scale-105 transition-all">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-500 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
            <Zap className="h-8 w-8 text-white" />
          </div>
          <h4 className="font-semibold text-gray-800 mb-2">Generate Quiz</h4>
          <p className="text-sm text-gray-500">Test your knowledge with AI-powered quizzes</p>
        </div>

        <div className="card-gradient p-6 text-center group cursor-pointer hover:scale-105 transition-all">
          <div className="bg-gradient-to-r from-green-500 to-emerald-500 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
            <Brain className="h-8 w-8 text-white" />
          </div>
          <h4 className="font-semibold text-gray-800 mb-2">AI Study Plan</h4>
          <p className="text-sm text-gray-500">Get personalized study recommendations</p>
        </div>

        <div className="card-gradient p-6 text-center group cursor-pointer hover:scale-105 transition-all">
          <div className="bg-gradient-to-r from-orange-500 to-red-500 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
            <Calendar className="h-8 w-8 text-white" />
          </div>
          <h4 className="font-semibold text-gray-800 mb-2">Smart Schedule</h4>
          <p className="text-sm text-gray-500">Optimize your study time with AI</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard