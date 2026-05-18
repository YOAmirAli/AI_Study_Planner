import React, { useState, useEffect } from 'react'
import { TrendingUp, Clock, Target, Award, BookOpen, Activity } from 'lucide-react'
import { analyticsAPI } from '../api/client'
import toast from 'react-hot-toast'
import { format, parseISO } from 'date-fns'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await analyticsAPI.getAnalytics()
      // API returns the analytics object directly as response.data
      setAnalyticsData(response.data)
    } catch (error) {
      toast.error('Failed to load analytics data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  if (!analyticsData) {
    return (
      <div className="text-center py-12">
        <Activity className="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 mb-2">No analytics available</h3>
        <p className="text-gray-500">Complete tasks and quizzes to generate data.</p>
      </div>
    )
  }

  // Format weekly trend data for the chart
  const weeklyTrendData = analyticsData.weekly_trend
    ?.slice()
    .reverse()
    .map(week => ({
      name: format(parseISO(week.week_start), 'MMM dd'),
      hours: week.hours
    })) || []

  // Format course hours for the chart
  const courseHoursData = analyticsData.hours_by_course || []

  // Format quiz performance by course
  const quizByCourseData = analyticsData.quiz_by_course || []

  const stats = [
    {
      title: 'Study Hours (This Week)',
      value: `${analyticsData.study_hours_this_week}h`,
      icon: Clock,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Task Completion Rate',
      value: `${analyticsData.completion_rate}%`,
      icon: Target,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Average Quiz Score',
      value: `${analyticsData.avg_quiz_score}%`,
      icon: Award,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Avg Hours / Day',
      value: `${analyticsData.avg_hours_per_day}h`,
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="text-gray-600 mt-1">Track your study progress and performance</p>
      </div>

      {/* Top Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div key={index} className="card p-6">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-xl ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div>
                <p className="text-sm text-gray-500 font-medium">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Trend Chart */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Study Hours Trend (Last 8 Weeks)</h2>
          <div className="h-[300px]">
            {weeklyTrendData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={weeklyTrendData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '0.5rem', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="hours" 
                    name="Hours Studied"
                    stroke="#4f46e5" 
                    strokeWidth={3}
                    dot={{ r: 4, fill: '#4f46e5', strokeWidth: 0 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500">
                Not enough data to display trend
              </div>
            )}
          </div>
        </div>

        {/* Study Hours by Course */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Study Hours by Course</h2>
          <div className="h-[300px]">
            {courseHoursData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={courseHoursData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e5e7eb" />
                  <XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                  <YAxis dataKey="course_name" type="category" width={100} axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '0.5rem', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                    cursor={{ fill: '#f3f4f6' }}
                  />
                  <Bar dataKey="hours" name="Hours" radius={[0, 4, 4, 0]}>
                    {courseHoursData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color || '#4f46e5'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500">
                No course data available
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quiz Performance by Course */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Average Quiz Score by Course</h2>
          <div className="h-[300px]">
            {quizByCourseData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={quizByCourseData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                  <XAxis dataKey="course_name" axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} domain={[0, 100]} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '0.5rem', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                    cursor={{ fill: '#f3f4f6' }}
                  />
                  <Bar dataKey="avg_score" name="Avg Score %" radius={[4, 4, 0, 0]} maxBarSize={60}>
                    {quizByCourseData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color || '#8b5cf6'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500">
                No quiz data available
              </div>
            )}
          </div>
        </div>

        {/* Recent Quizzes */}
        <div className="card p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Recent Quizzes</h2>
          <div className="space-y-4">
            {analyticsData.recent_quiz_scores && analyticsData.recent_quiz_scores.length > 0 ? (
              analyticsData.recent_quiz_scores.slice(0, 5).map((quiz, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                  <div>
                    <h4 className="font-semibold text-gray-800">{quiz.title}</h4>
                    <p className="text-sm text-gray-500">
                      {format(parseISO(quiz.completed_at), 'MMM dd, yyyy')} • {quiz.total_questions} Questions
                    </p>
                  </div>
                  <div className={`px-3 py-1 rounded-full font-bold ${
                    quiz.percentage >= 80 ? 'bg-green-100 text-green-700' :
                    quiz.percentage >= 60 ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {quiz.percentage}%
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                No recent quizzes taken
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics