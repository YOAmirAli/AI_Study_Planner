import React, { useState, useEffect } from 'react'
import { Plus, Search, Filter, FileText, Link as LinkIcon, Video, BookOpen, Star, Trash2, Edit2, ExternalLink, Grid, List } from 'lucide-react'
import { resourceAPI, courseAPI } from '../api/client'
import toast from 'react-hot-toast'

const Resources = () => {
  const [resources, setResources] = useState([])
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingResource, setEditingResource] = useState(null)
  const [viewMode, setViewMode] = useState('grid')
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [showFavorites, setShowFavorites] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    resource_type: 'link',
    url: '',
    course_id: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [resourcesRes, coursesRes] = await Promise.all([
        resourceAPI.getAll(),
        courseAPI.getAll()
      ])
      setResources(resourcesRes.data.resources || [])
      setCourses(coursesRes.data.courses || [])
    } catch (error) {
      toast.error('Failed to load resources')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingResource) {
        await resourceAPI.update(editingResource.resource_id, formData)
        toast.success('Resource updated successfully')
      } else {
        await resourceAPI.create(formData)
        toast.success('Resource added successfully')
      }
      setShowModal(false)
      setEditingResource(null)
      setFormData({ title: '', description: '', resource_type: 'link', url: '', course_id: '' })
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const handleDelete = async (resourceId) => {
    if (window.confirm('Are you sure you want to delete this resource?')) {
      try {
        await resourceAPI.delete(resourceId)
        toast.success('Resource deleted')
        fetchData()
      } catch (error) {
        toast.error('Failed to delete resource')
      }
    }
  }

  const handleToggleFavorite = async (resourceId) => {
    try {
      await resourceAPI.toggleFavorite(resourceId)
      fetchData()
    } catch (error) {
      toast.error('Failed to update favorite')
    }
  }

  const getResourceIcon = (type) => {
    switch(type) {
      case 'video': return <Video className="h-8 w-8 text-red-500" />
      case 'link': return <LinkIcon className="h-8 w-8 text-blue-500" />
      case 'pdf': return <FileText className="h-8 w-8 text-red-600" />
      case 'document': return <FileText className="h-8 w-8 text-green-500" />
      default: return <BookOpen className="h-8 w-8 text-gray-500" />
    }
  }

  const filteredResources = resources.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          resource.description?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = filterType === 'all' || resource.resource_type === filterType
    const matchesFavorite = !showFavorites || resource.is_favorite
    return matchesSearch && matchesType && matchesFavorite
  })

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
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Learning Resources</h1>
          <p className="text-gray-600 mt-1">Organize and access your study materials</p>
        </div>
        <button
          onClick={() => {
            setEditingResource(null)
            setFormData({ title: '', description: '', resource_type: 'link', url: '', course_id: '' })
            setShowModal(true)
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-5 w-5" />
          Add Resource
        </button>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex flex-wrap gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search resources..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
            />
          </div>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 rounded-xl border border-gray-300 focus:border-indigo-500 outline-none"
          >
            <option value="all">All Types</option>
            <option value="link">Links</option>
            <option value="video">Videos</option>
            <option value="pdf">PDFs</option>
            <option value="document">Documents</option>
          </select>
          
          <button
            onClick={() => setShowFavorites(!showFavorites)}
            className={`px-4 py-2 rounded-xl border transition-colors flex items-center gap-2 ${
              showFavorites ? 'bg-yellow-50 border-yellow-400 text-yellow-700' : 'border-gray-300 hover:bg-gray-50'
            }`}
          >
            <Star className={`h-4 w-4 ${showFavorites ? 'fill-yellow-400' : ''}`} />
            Favorites
          </button>
          
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg ${viewMode === 'grid' ? 'bg-indigo-100 text-indigo-600' : 'hover:bg-gray-100'}`}
            >
              <Grid className="h-5 w-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg ${viewMode === 'list' ? 'bg-indigo-100 text-indigo-600' : 'hover:bg-gray-100'}`}
            >
              <List className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Resources Grid/List */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredResources.map((resource) => (
            <div key={resource.resource_id} className="card p-6 hover:scale-105 transition-all duration-300">
              <div className="flex justify-between items-start mb-4">
                {getResourceIcon(resource.resource_type)}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleToggleFavorite(resource.resource_id)}
                    className="p-1 rounded hover:bg-gray-100"
                  >
                    <Star className={`h-5 w-5 ${resource.is_favorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'}`} />
                  </button>
                  <button
                    onClick={() => {
                      setEditingResource(resource)
                      setFormData(resource)
                      setShowModal(true)
                    }}
                    className="p-1 rounded hover:bg-gray-100"
                  >
                    <Edit2 className="h-4 w-4 text-gray-500" />
                  </button>
                  <button
                    onClick={() => handleDelete(resource.resource_id)}
                    className="p-1 rounded hover:bg-red-100"
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </button>
                </div>
              </div>
              
              <h3 className="font-semibold text-gray-800 mb-2">{resource.title}</h3>
              {resource.description && (
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">{resource.description}</p>
              )}
              
              {resource.url && (
                <a
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-indigo-600 hover:text-indigo-700 flex items-center gap-1 mb-3"
                >
                  <ExternalLink className="h-3 w-3" />
                  Open Resource
                </a>
              )}
              
              {resource.course && (
                <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-100">
                  📚 {resource.course.course_name}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {filteredResources.map((resource) => (
            <div key={resource.resource_id} className="card p-4 hover:shadow-md transition-all">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1">
                  {getResourceIcon(resource.resource_type)}
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800">{resource.title}</h3>
                    {resource.description && (
                      <p className="text-sm text-gray-600">{resource.description}</p>
                    )}
                    {resource.url && (
                      <a
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-indigo-600 hover:text-indigo-700 flex items-center gap-1 mt-1"
                      >
                        <ExternalLink className="h-3 w-3" />
                        {resource.url.substring(0, 50)}...
                      </a>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleToggleFavorite(resource.resource_id)}
                    className="p-2 rounded hover:bg-gray-100"
                  >
                    <Star className={`h-5 w-5 ${resource.is_favorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'}`} />
                  </button>
                  <button
                    onClick={() => {
                      setEditingResource(resource)
                      setFormData(resource)
                      setShowModal(true)
                    }}
                    className="p-2 rounded hover:bg-gray-100"
                  >
                    <Edit2 className="h-4 w-4 text-gray-500" />
                  </button>
                  <button
                    onClick={() => handleDelete(resource.resource_id)}
                    className="p-2 rounded hover:bg-red-100"
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {filteredResources.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No resources found</h3>
          <p className="text-gray-500">Click the "Add Resource" button to get started</p>
        </div>
      )}

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">{editingResource ? 'Edit Resource' : 'Add Resource'}</h2>
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Resource Type</label>
                <select
                  value={formData.resource_type}
                  onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
                  className="input"
                >
                  <option value="link">Link</option>
                  <option value="video">Video</option>
                  <option value="pdf">PDF</option>
                  <option value="document">Document</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">URL</label>
                <input
                  type="url"
                  value={formData.url}
                  onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                  className="input"
                  placeholder="https://..."
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Course (Optional)</label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                  className="input"
                >
                  <option value="">Select Course</option>
                  {courses.map(course => (
                    <option key={course.course_id} value={course.course_id}>{course.course_name}</option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingResource ? 'Update' : 'Add'}
                </button>
                <button type="button" onClick={() => setShowModal(false)} className="btn-secondary flex-1">
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

export default Resources