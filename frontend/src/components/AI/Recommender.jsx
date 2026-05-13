import React, { useState } from 'react'
import { Sparkles, Youtube, Search, ExternalLink, Clock, Hash, Loader } from 'lucide-react'
import { aiAPI } from '../../api/client'
import toast from 'react-hot-toast'

const Recommender = () => {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [recommendations, setRecommendations] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!topic.trim()) {
      toast.error('Please enter a topic')
      return
    }
    
    setLoading(true)
    
    try {
      const response = await aiAPI.recommendMaterials({ topic })
      setRecommendations(response.data)
      toast.success('Recommendations generated!')
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to get recommendations')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl">
            <Youtube className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Learning Resource Recommender</h2>
            <p className="text-gray-500">Discover the best educational content for any topic</p>
          </div>
        </div>
        
        {!recommendations ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                What do you want to learn?
              </label>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
                  placeholder="e.g., React.js, Machine Learning, Digital Marketing"
                  required
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all shadow-lg disabled:opacity-50 flex items-center gap-2"
                >
                  {loading ? (
                    <Loader className="h-5 w-5 animate-spin" />
                  ) : (
                    <Search className="h-5 w-5" />
                  )}
                  <span>Search</span>
                </button>
              </div>
            </div>
          </form>
        ) : (
          <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-gray-800">
                  Results for "{recommendations.search_query}"
                </h3>
                <p className="text-gray-500">{recommendations.total_results} recommendations found</p>
              </div>
              <button
                onClick={() => {
                  setRecommendations(null)
                  setTopic('')
                }}
                className="text-sm text-indigo-600 hover:text-indigo-700"
              >
                New Search →
              </button>
            </div>

            {/* Video Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {recommendations.videos.map((video, idx) => (
                <div key={idx} className="group bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-all hover:scale-105">
                  <div className="relative h-48 bg-gray-900 flex items-center justify-center">
                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 to-purple-600/20"></div>
                    <Youtube className="h-16 w-16 text-red-500 opacity-75 group-hover:opacity-100 transition-opacity" />
                    <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                      {video.duration}
                    </div>
                  </div>
                  <div className="p-4">
                    <h4 className="font-semibold text-gray-800 mb-1 line-clamp-2">{video.title}</h4>
                    <p className="text-sm text-gray-500 mb-2">{video.channel}</p>
                    <p className="text-xs text-gray-400 mb-3 line-clamp-2">{video.description}</p>
                    <a
                      href={video.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-sm text-indigo-600 hover:text-indigo-700 font-medium"
                    >
                      Watch on YouTube
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>

            {/* Note */}
            {recommendations.note && (
              <div className="p-4 bg-yellow-50 rounded-lg text-center text-sm text-yellow-800">
                <Hash className="h-4 w-4 inline mr-1" />
                {recommendations.note}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Recommender