import React, { useState, useEffect } from 'react'
import { Plus, Search, Filter, Calendar, Flag, Clock, CheckCircle, Circle, Edit2, Trash2, AlertCircle } from 'lucide-react'
import { taskAPI, courseAPI } from '../api/client'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

const Tasks = () => {
  const [tasks, setTasks] = useState([])
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    deadline: '',
    priority: 'medium',
    estimated_time: 60
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [tasksRes, coursesRes] = await Promise.all([
        taskAPI.getAll(),
        courseAPI.getAll()
      ])
      setTasks(tasksRes.data.tasks || [])
      setCourses(coursesRes.data.courses || [])
    } catch (error) {
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingTask) {
        await taskAPI.update(editingTask.task_id, formData)
        toast.success('Task updated successfully')
      } else {
        await taskAPI.create(formData)
        toast.success('Task created successfully')
      }
      setShowModal(false)
      setEditingTask(null)
      setFormData({ title: '', description: '', course_id: '', deadline: '', priority: 'medium', estimated_time: 60 })
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const handleComplete = async (taskId) => {
    try {
      await taskAPI.complete(taskId)
      toast.success('Task completed! 🎉')
      fetchData()
    } catch (error) {
      toast.error('Failed to complete task')
    }
  }

  const handleDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.delete(taskId)
        toast.success('Task deleted')
        fetchData()
      } catch (error) {
        toast.error('Failed to delete task')
      }
    }
  }

  const getPriorityIcon = (priority) => {
    switch(priority) {
      case 'high': return <Flag className="h-4 w-4 text-red-500" />
      case 'medium': return <Flag className="h-4 w-4 text-yellow-500" />
      case 'low': return <Flag className="h-4 w-4 text-green-500" />
      default: return <Flag className="h-4 w-4 text-gray-500" />
    }
  }

  const getPriorityClass = (priority) => {
    switch(priority) {
      case 'high': return 'badge-danger'
      case 'medium': return 'badge-warning'
      case 'low': return 'badge-success'
      default: return 'badge-info'
    }
  }

  const filteredTasks = tasks.filter(task => {
    const matchesFilter = filter === 'all' || task.status === filter
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          task.description?.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesFilter && matchesSearch
  })

  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.status === 'completed').length,
    pending: tasks.filter(t => t.status === 'pending').length,
    overdue: tasks.filter(t => t.status !== 'completed' && new Date(t.deadline) < new Date()).length
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
          <p className="text-gray-600 mt-1">Manage your assignments and study tasks</p>
        </div>
        <button
          onClick={() => {
            setEditingTask(null)
            setFormData({ title: '', description: '', course_id: '', deadline: '', priority: 'medium', estimated_time: 60 })
            setShowModal(true)
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-5 w-5" />
          Add Task
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-500">Total Tasks</p>
              <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-indigo-500" />
          </div>
        </div>
        <div className="card p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
            </div>
            <Circle className="h-8 w-8 text-green-500" />
          </div>
        </div>
        <div className="card p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-500">Pending</p>
              <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-500" />
          </div>
        </div>
        <div className="card p-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-500">Overdue</p>
              <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
            </div>
            <AlertCircle className="h-8 w-8 text-red-500" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex flex-wrap gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
            />
          </div>
          <div className="flex gap-2">
            {['all', 'pending', 'in_progress', 'completed'].map(status => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-4 py-2 rounded-xl capitalize transition-all ${
                  filter === status
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tasks List */}
      <div className="space-y-3">
        {filteredTasks.map((task) => (
          <div key={task.task_id} className="card p-4 hover:shadow-lg transition-all">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3 flex-1">
                <button onClick={() => handleComplete(task.task_id)} className="mt-1">
                  {task.status === 'completed' ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <Circle className="h-5 w-5 text-gray-400 hover:text-indigo-500" />
                  )}
                </button>
                <div className="flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h3 className={`font-semibold ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      {task.title}
                    </h3>
                    <span className={`badge ${getPriorityClass(task.priority)}`}>
                      {task.priority}
                    </span>
                    {task.status === 'completed' && (
                      <span className="badge badge-success">Completed</span>
                    )}
                  </div>
                  {task.description && (
                    <p className="text-sm text-gray-500 mt-1">{task.description}</p>
                  )}
                  <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    {task.deadline && (
                      <div className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        <span>Due: {format(new Date(task.deadline), 'MMM dd, yyyy')}</span>
                      </div>
                    )}
                    {task.estimated_time && (
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        <span>{task.estimated_time} min</span>
                      </div>
                    )}
                    {task.course && (
                      <div className="flex items-center gap-1">
                        <BookOpen className="h-3 w-3" />
                        <span>{task.course.course_name}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    setEditingTask(task)
                    setFormData(task)
                    setShowModal(true)
                  }}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <Edit2 className="h-4 w-4 text-gray-500" />
                </button>
                <button
                  onClick={() => handleDelete(task.task_id)}
                  className="p-2 rounded-lg hover:bg-red-50 transition-colors"
                >
                  <Trash2 className="h-4 w-4 text-red-500" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredTasks.length === 0 && (
        <div className="text-center py-12">
          <CheckCircle className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No tasks found</h3>
          <p className="text-gray-500">Create a new task to get started</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">{editingTask ? 'Edit Task' : 'Create New Task'}</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="input"
                  rows="3"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Course</label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({ ...formData, course_id: parseInt(e.target.value) })}
                  className="input"
                >
                  <option value="">Select Course</option>
                  {courses.map(course => (
                    <option key={course.course_id} value={course.course_id}>{course.course_name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Deadline</label>
                <input
                  type="datetime-local"
                  value={formData.deadline?.slice(0, 16)}
                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                  className="input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  className="input"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Time (minutes)</label>
                <input
                  type="number"
                  value={formData.estimated_time}
                  onChange={(e) => setFormData({ ...formData, estimated_time: parseInt(e.target.value) })}
                  className="input"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingTask ? 'Update' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Tasks