import React, { useState } from 'react'
import { Sparkles, BookOpen, List, Lightbulb, Link as LinkIcon, Clock, Send, Loader } from 'lucide-react'
import { aiAPI } from '../../api/client'
import toast from 'react-hot-toast'

const TaskTutor = () => {
  const [taskTitle, setTaskTitle] = useState('')
  const [taskDescription, setTaskDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [guidance, setGuidance] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!taskTitle.trim()) {
      toast.error('Please enter a task title')
      return
    }
    
    if (!taskDescription.trim()) {
      toast.error('Please enter a task description')
      return
    }
    
    setLoading(true)
    
    try {
      const response = await aiAPI.taskTutor({
        task_title: taskTitle,
        task_description: taskDescription
      })
      setGuidance(response.data)
      toast.success('Learning guidance generated!')
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to generate guidance')
    } finally {
      setLoading(false)
    }
  }

  const getResourceIcon = (type) => {
    switch(type) {
      case 'video': return '🎥'
      case 'article': return '📄'
      case 'tutorial': return '📚'
      case 'documentation': return '📖'
      default: return '🔗'
    }
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">AI Task Tutor</h2>
            <p className="text-gray-500">Get personalized learning guidance for any task</p>
          </div>
        </div>
        
        {!guidance ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Task Title
              </label>
              <input
                type="text"
                value={taskTitle}
                onChange={(e) => setTaskTitle(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
                placeholder="e.g., Understanding Machine Learning Algorithms"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Task Description
              </label>
              <textarea
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
                rows={6}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-none"
                placeholder="Describe what you need to learn or accomplish..."
                required
              />
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all shadow-lg disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader className="h-5 w-5 animate-spin" />
                  <span>Analyzing Task...</span>
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  <span>Get Learning Guidance</span>
                </>
              )}
            </button>
          </form>
        ) : (
          <div className="space-y-6 animate-fade-in">
            {/* Explanation */}
            <div className="p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb className="h-5 w-5 text-yellow-600" />
                <h3 className="font-semibold text-gray-800">What's This About?</h3>
              </div>
              <p className="text-gray-700 leading-relaxed">{guidance.explanation}</p>
              <div className="mt-3 flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                <span>Estimated time: {guidance.estimated_time} minutes</span>
              </div>
            </div>

            {/* Learning Steps */}
            <div className="p-6 bg-white border border-gray-200 rounded-xl">
              <div className="flex items-center gap-2 mb-4">
                <List className="h-5 w-5 text-green-600" />
                <h3 className="font-semibold text-gray-800">Learning Steps</h3>
              </div>
              <div className="space-y-3">
                {guidance.learning_steps.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-sm font-semibold">
                      {idx + 1}
                    </div>
                    <p className="text-gray-700">{step}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Key Concepts */}
            {guidance.key_concepts && guidance.key_concepts.length > 0 && (
              <div className="p-6 bg-white border border-gray-200 rounded-xl">
                <div className="flex items-center gap-2 mb-4">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold text-gray-800">Key Concepts</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {guidance.key_concepts.map((concept, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                      {concept}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Resources */}
            {guidance.resources && guidance.resources.length > 0 && (
              <div className="p-6 bg-white border border-gray-200 rounded-xl">
                <div className="flex items-center gap-2 mb-4">
                  <LinkIcon className="h-5 w-5 text-purple-600" />
                  <h3 className="font-semibold text-gray-800">Recommended Resources</h3>
                </div>
                <div className="space-y-3">
                  {guidance.resources.map((resource, idx) => (
                    <div key={idx} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <span className="text-2xl">{getResourceIcon(resource.type)}</span>
                      <div className="flex-1">
                        <p className="font-medium text-gray-800">{resource.title}</p>
                        <p className="text-sm text-gray-500">{resource.description}</p>
                      </div>
                      <a
                        href={`https://www.google.com/search?q=${encodeURIComponent(resource.title)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-3 py-1 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                      >
                        Search
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Study Tips */}
            {guidance.study_tips && guidance.study_tips.length > 0 && (
              <div className="p-6 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl">
                <div className="flex items-center gap-2 mb-4">
                  <Lightbulb className="h-5 w-5 text-orange-600" />
                  <h3 className="font-semibold text-gray-800">Study Tips</h3>
                </div>
                <ul className="space-y-2">
                  {guidance.study_tips.map((tip, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <span className="text-orange-500">•</span>
                      {tip}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* New Task Button */}
            <button
              onClick={() => {
                setGuidance(null)
                setTaskTitle('')
                setTaskDescription('')
              }}
              className="w-full btn-secondary"
            >
              Get Guidance for Another Task
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default TaskTutor