import React, { useState, useEffect } from 'react'
import { Link, FileText, Video, BookOpen, Trash2, Plus, ExternalLink } from 'lucide-react'
import { groupAPI } from '../../api/client'
import toast from 'react-hot-toast'

const GroupResources = ({ groupId }) => {
  const [resources, setResources] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    resource_type: 'link',
    resource_url: '',
    content: ''
  })

  useEffect(() => {
    fetchResources()
  }, [groupId])

  const fetchResources = async () => {
    try {
      const response = await groupAPI.getResources(groupId)
      setResources(response.data.resources || [])
    } catch (error) {
      toast.error('Failed to load resources')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await groupAPI.shareResource(groupId, formData)
      toast.success('Resource shared successfully!')
      setShowModal(false)
      setFormData({ title: '', description: '', resource_type: 'link', resource_url: '', content: '' })
      fetchResources()
    } catch (error) {
      toast.error('Failed to share resource')
    }
  }

  const handleDelete = async (resourceId) => {
    if (window.confirm('Are you sure you want to delete this resource?')) {
      try {
        await groupAPI.deleteResource(groupId, resourceId)
        toast.success('Resource deleted')
        fetchResources()
      } catch (error) {
        toast.error('Failed to delete resource')
      }
    }
  }

  const getResourceIcon = (type) => {
    switch(type) {
      case 'video': return <Video className="h-5 w-5 text-red-500" />
      case 'link': return <Link className="h-5 w-5 text-blue-500" />
      case 'file': return <FileText className="h-5 w-5 text-green-500" />
      case 'note': return <BookOpen className="h-5 w-5 text-purple-500" />
      default: return <FileText className="h-5 w-5 text-gray-500" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Shared Resources</h3>
        <button
          onClick={() => setShowModal(true)}
          className="px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Share Resource
        </button>
      </div>

      {/* Resources List */}
      <div className="space-y-3">
        {resources.map((resource) => (
          <div key={resource.resource_id} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3 flex-1">
                {getResourceIcon(resource.resource_type)}
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800">{resource.title}</h4>
                  {resource.description && (
                    <p className="text-sm text-gray-600 mt-1">{resource.description}</p>
                  )}
                  {resource.resource_url && (
                    <a
                      href={resource.resource_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-indigo-600 hover:text-indigo-700 flex items-center gap-1 mt-2"
                    >
                      <ExternalLink className="h-3 w-3" />
                      Open Link
                    </a>
                  )}
                  {resource.content && (
                    <p className="text-sm text-gray-600 mt-2 p-2 bg-white rounded">{resource.content}</p>
                  )}
                  <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
                    <span>Shared by: {resource.shared_by?.name || 'Unknown'}</span>
                    <span>•</span>
                    <span>{new Date(resource.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => handleDelete(resource.resource_id)}
                className="p-1 rounded hover:bg-red-100 transition-colors"
              >
                <Trash2 className="h-4 w-4 text-red-500" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {resources.length === 0 && (
        <div className="text-center py-8">
          <BookOpen className="h-12 w-12 mx-auto text-gray-400 mb-3" />
          <p className="text-gray-500">No resources shared yet</p>
          <p className="text-sm text-gray-400">Be the first to share a resource!</p>
        </div>
      )}

      {/* Share Resource Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Share Resource</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Resource Type</label>
                <select
                  value={formData.resource_type}
                  onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="link">Link</option>
                  <option value="video">Video</option>
                  <option value="note">Note</option>
                  <option value="file">File</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">URL (for links/videos)</label>
                <input
                  type="url"
                  value={formData.resource_url}
                  onChange={(e) => setFormData({ ...formData, resource_url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="https://..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="flex-1 btn-primary">Share</button>
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default GroupResources