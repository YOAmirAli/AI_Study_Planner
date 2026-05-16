import React, { useState, useEffect } from 'react'
import { Users, Plus, Search, Hash, MessageCircle, FolderOpen, Trophy, LogIn, LogOut, Crown, UserPlus } from 'lucide-react'
import { groupAPI } from '../api/client'
import toast from 'react-hot-toast'
import ChatRoom from '../components/Groups/ChatRoom'
import GroupResources from '../components/Groups/GroupResources'
import Leaderboard from '../components/Groups/Leaderboard'
const Groups = () => {
  const [groups, setGroups] = useState([])
  const [selectedGroup, setSelectedGroup] = useState(null)
  const [activeTab, setActiveTab] = useState('chat')
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showJoinModal, setShowJoinModal] = useState(false)
  const [joinCode, setJoinCode] = useState('')
  const [formData, setFormData] = useState({
    group_name: '',
    description: '',
    is_private: false,
    max_members: 50
  })

  useEffect(() => {
    fetchGroups()
  }, [])

  const fetchGroups = async () => {
    try {
      const response = await groupAPI.getAll()
      setGroups(response.data.groups || [])
    } catch (error) {
      toast.error('Failed to load groups')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateGroup = async (e) => {
    e.preventDefault()
    try {
      const response = await groupAPI.create(formData)
      toast.success('Group created successfully!')
      setShowCreateModal(false)
      setFormData({ group_name: '', description: '', is_private: false, max_members: 50 })
      fetchGroups()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to create group')
    }
  }

  const handleJoinGroup = async () =>{
    if (!joinCode.trim()) {
      toast.error('Please enter a join code')
      return
    }
    try {
      const response = await groupAPI.joinByCode({ join_code: joinCode.toUpperCase() })
      toast.success('Joined group successfully!')
      setShowJoinModal(false)
      setJoinCode('')
      fetchGroups()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Invalid join code')
    }
  }

  const handleLeaveGroup = async (groupId) => {
    if (window.confirm('Are you sure you want to leave this group?')) {
      try {
        await groupAPI.leave(groupId)
        toast.success('Left group')
        if (selectedGroup?.group_id === groupId) {
          setSelectedGroup(null)
        }
        fetchGroups()
      } catch (error) {
        toast.error('Failed to leave group')
      }
    }
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
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Study Groups</h1>
          <p className="text-gray-600 mt-1">Collaborate with peers and learn together</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowJoinModal(true)}
            className="btn-outline flex items-center gap-2"
          >
            <UserPlus className="h-5 w-5" />
            Join Group
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Create Group
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Groups List */}
        <div className="lg:col-span-1 space-y-3">
          <div className="card p-4">
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search groups..."
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:border-indigo-500 outline-none"
              />
            </div>
            <div className="space-y-2">
              {groups.map((group) => (
                <button
                  key={group.group_id}
                  onClick={() => setSelectedGroup(group)}
                  className={`w-full p-4 rounded-xl text-left transition-all ${
                    selectedGroup?.group_id === group.group_id
                      ? 'bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200'
                      : 'hover:bg-gray-50 border border-transparent'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">{group.group_name}</h3>
                      <p className="text-xs text-gray-500 mt-1">
                        {group.member_count} members
                      </p>
                    </div>
                    {group.unread_count > 0 && (
                      <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                        {group.unread_count}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>

            {groups.length === 0 && (
              <div className="text-center py-8">
                <Users className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                <p className="text-gray-500">No groups yet</p>
                <p className="text-xs text-gray-400">Create or join a group to get started</p>
              </div>
            )}
          </div>
        </div>

        {/* Group Content */}
        <div className="lg:col-span-2">
          {selectedGroup ? (
            <div className="card overflow-hidden">
              {/* Group Header */}
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-2xl font-bold">{selectedGroup.group_name}</h2>
                    <p className="text-indigo-100 mt-1">{selectedGroup.description}</p>
                    <div className="flex gap-3 mt-3">
                      <div className="flex items-center gap-1 text-sm">
                        <Hash className="h-4 w-4" />
                        <span>Code: {selectedGroup.join_code}</span>
                      </div>
                      <div className="flex items-center gap-1 text-sm">
                        <Users className="h-4 w-4" />
                        <span>{selectedGroup.member_count} members</span>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleLeaveGroup(selectedGroup.group_id)}
                    className="px-3 py-1 bg-white/20 rounded-lg text-sm hover:bg-white/30 transition-colors flex items-center gap-1"
                  >
                    <LogOut className="h-4 w-4" />
                    Leave
                  </button>
                </div>
              </div>

              {/* Tabs */}
              <div className="flex border-b border-gray-200">
                {[
                  { id: 'chat', icon: MessageCircle, label: 'Chat' },
                  { id: 'resources', icon: FolderOpen, label: 'Resources' },
                  { id: 'leaderboard', icon: Trophy, label: 'Leaderboard' }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-6 py-3 font-medium transition-all ${
                      activeTab === tab.id
                        ? 'text-indigo-600 border-b-2 border-indigo-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    <tab.icon className="h-4 w-4" />
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="p-4">
                {activeTab === 'chat' && <ChatRoom groupId={selectedGroup.group_id} />}
                {activeTab === 'resources' && <GroupResources groupId={selectedGroup.group_id} />}
                {activeTab === 'leaderboard' && <Leaderboard groupId={selectedGroup.group_id} />}
              </div>
            </div>
          ) : (
            <div className="card p-12 text-center">
              <Users className="h-16 w-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-xl font-semibold text-gray-700 mb-2">No Group Selected</h3>
              <p className="text-gray-500">Select a group from the list to start collaborating</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Group Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Create Study Group</h2>
            <form onSubmit={handleCreateGroup} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Group Name *</label>
                <input
                  type="text"
                  value={formData.group_name}
                  onChange={(e) => setFormData({ ...formData, group_name: e.target.value })}
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Max Members</label>
                <input
                  type="number"
                  value={formData.max_members}
                  onChange={(e) => setFormData({ ...formData, max_members: parseInt(e.target.value) })}
                  className="input"
                  min="2"
                  max="100"
                />
              </div>
              
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="is_private"
                  checked={formData.is_private}
                  onChange={(e) => setFormData({ ...formData, is_private: e.target.checked })}
                  className="rounded"
                />
                <label htmlFor="is_private" className="text-sm text-gray-700">Private Group</label>
              </div>
              
              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">Create</button>
                <button type="button" onClick={() => setShowCreateModal(false)} className="btn-secondary flex-1">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Join Group Modal */}
      {showJoinModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Join Study Group</h2>
            <p className="text-gray-600 mb-4">Enter the 6-character join code provided by the group admin</p>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Join Code</label>
              <input
                type="text"
                value={joinCode}
                onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                className="input text-center text-2xl font-mono tracking-widest"
                placeholder="ABC123"
                maxLength="6"
              />
            </div>
            
            <div className="flex gap-3">
              <button onClick={handleJoinGroup} className="btn-primary flex-1">Join Group</button>
              <button onClick={() => setShowJoinModal(false)} className="btn-secondary flex-1">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Groups