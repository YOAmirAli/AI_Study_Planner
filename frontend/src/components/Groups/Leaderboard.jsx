import React, { useState, useEffect } from 'react'
import { Trophy, Medal, Star, TrendingUp, Award } from 'lucide-react'
import { groupAPI } from '../../api/client'
import toast from 'react-hot-toast'
const Leaderboard = ({ groupId }) => {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLeaderboard()
  }, [groupId])

  const fetchLeaderboard = async () => {
    try {
      const response = await groupAPI.getLeaderboard(groupId)
      setLeaderboard(response.data.leaderboard || [])
    } catch (error) {
      toast.error('Failed to load leaderboard')
    } finally {
      setLoading(false)
    }
  }

  const getRankIcon = (rank) => {
    switch(rank) {
      case 1: return <Trophy className="h-6 w-6 text-yellow-500" />
      case 2: return <Medal className="h-6 w-6 text-gray-400" />
      case 3: return <Medal className="h-6 w-6 text-amber-600" />
      default: return <span className="text-gray-500 font-semibold">{rank}</span>
    }
  }

  const getScoreColor = (score) => {
    if (score >= 100) return 'text-purple-600'
    if (score >= 50) return 'text-indigo-600'
    return 'text-gray-600'
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
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg p-4 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm opacity-90">Top Learner</p>
              <p className="text-2xl font-bold">{leaderboard[0]?.name || 'N/A'}</p>
            </div>
            <Trophy className="h-8 w-8" />
          </div>
          <p className="text-sm mt-2">{leaderboard[0]?.points || 0} points</p>
        </div>
        
        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg p-4 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm opacity-90">Total Members</p>
              <p className="text-2xl font-bold">{leaderboard.length}</p>
            </div>
            <Users className="h-8 w-8" />
          </div>
          <p className="text-sm mt-2">Active learners</p>
        </div>
        
        <div className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg p-4 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm opacity-90">Average Score</p>
              <p className="text-2xl font-bold">
                {Math.round(leaderboard.reduce((acc, m) => acc + (m.avg_quiz_score || 0), 0) / leaderboard.length || 0)}%
              </p>
            </div>
            <TrendingUp className="h-8 w-8" />
          </div>
          <p className="text-sm mt-2">Quiz performance</p>
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <h3 className="font-semibold text-gray-800 flex items-center gap-2">
            <Award className="h-5 w-5 text-yellow-500" />
            Rankings
          </h3>
        </div>
        
        <div className="divide-y divide-gray-200">
          {leaderboard.map((member, idx) => (
            <div key={member.user_id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 text-center">
                    {getRankIcon(member.rank)}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">{member.name}</p>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                      <span>Tasks: {member.tasks_completed}</span>
                      <span>•</span>
                      <span>Quizzes: {member.quizzes_taken}</span>
                      <span>•</span>
                      <span>Avg Score: {member.avg_quiz_score}%</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-2xl font-bold ${getScoreColor(member.points)}`}>
                    {member.points}
                  </p>
                  <p className="text-xs text-gray-500">points</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Empty State */}
      {leaderboard.length === 0 && (
        <div className="text-center py-12">
          <Trophy className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">No leaderboard data yet</p>
          <p className="text-sm text-gray-400">Complete tasks and quizzes to earn points!</p>
        </div>
      )}
    </div>
  )
}

// Add Users import
import { Users } from 'lucide-react'

export default Leaderboard