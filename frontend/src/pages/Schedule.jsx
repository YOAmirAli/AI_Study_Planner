import React, { useState, useEffect } from 'react'
import { Calendar as CalendarIcon, Clock, Plus, Zap, ChevronLeft, ChevronRight, Coffee, BookOpen, GraduationCap } from 'lucide-react'
import { scheduleAPI, taskAPI } from '../api/client'
import toast from 'react-hot-toast'
import { format, addDays, subDays, startOfWeek, addWeeks, subWeeks } from 'date-fns'

const Schedule = () => {
  const [schedule, setSchedule] = useState({})
  const [currentWeek, setCurrentWeek] = useState(new Date())
  const [loading, setLoading] = useState(true)
  const [showGenerateModal, setShowGenerateModal] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [studyHours, setStudyHours] = useState(4)

  useEffect(() => {
    fetchSchedule()
  }, [currentWeek])

  const fetchSchedule = async () => {
    try {
      const weekStart = startOfWeek(currentWeek, { weekStartsOn: 1 })
      const response = await scheduleAPI.getWeekly(format(weekStart, 'yyyy-MM-dd'))
      setSchedule(response.data.schedule || {})
    } catch (error) {
      toast.error('Failed to load schedule')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateSchedule = async () => {
    setGenerating(true)
    try {
      const weekStart = startOfWeek(currentWeek, { weekStartsOn: 1 })
      await scheduleAPI.generate({
        week_start: format(weekStart, 'yyyy-MM-dd'),
        study_hours_per_day: studyHours
      })
      toast.success('AI schedule generated successfully!')
      setShowGenerateModal(false)
      fetchSchedule()
    } catch (error) {
      toast.error('Failed to generate schedule')
    } finally {
      setGenerating(false)
    }
  }

  const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const timeSlots = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']

  const getBlockColor = (type) => {
    switch(type) {
      case 'study': return 'bg-indigo-100 border-indigo-300 text-indigo-700'
      case 'class': return 'bg-purple-100 border-purple-300 text-purple-700'
      case 'break': return 'bg-green-100 border-green-300 text-green-700'
      default: return 'bg-gray-100 border-gray-300 text-gray-700'
    }
  }

  const getBlockIcon = (type) => {
    switch(type) {
      case 'study': return <BookOpen className="h-4 w-4" />
      case 'class': return <GraduationCap className="h-4 w-4" />
      case 'break': return <Coffee className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
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
          <h1 className="text-3xl font-bold text-gray-900">Study Schedule</h1>
          <p className="text-gray-600 mt-1">AI-powered weekly study planner</p>
        </div>
        <button
          onClick={() => setShowGenerateModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Zap className="h-5 w-5" />
          Generate AI Schedule
        </button>
      </div>

      {/* Week Navigation */}
      <div className="card p-4 flex justify-between items-center">
        <button
          onClick={() => setCurrentWeek(subWeeks(currentWeek, 1))}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <ChevronLeft className="h-5 w-5" />
        </button>
        <div className="text-center">
          <h3 className="text-xl font-semibold">
            {format(startOfWeek(currentWeek, { weekStartsOn: 1 }), 'MMM dd')} - {format(addDays(startOfWeek(currentWeek, { weekStartsOn: 1 }), 6), 'MMM dd, yyyy')}
          </h3>
        </div>
        <button
          onClick={() => setCurrentWeek(addWeeks(currentWeek, 1))}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      {/* Calendar Grid */}
      <div className="overflow-x-auto">
        <div className="min-w-[800px]">
          {/* Header */}
          <div className="grid grid-cols-8 gap-2 mb-2">
            <div className="p-3"></div>
            {weekDays.map(day => (
              <div key={day} className="p-3 text-center font-semibold bg-gray-100 rounded-lg">
                {day}
              </div>
            ))}
          </div>

          {/* Time Slots */}
          {timeSlots.map(time => (
            <div key={time} className="grid grid-cols-8 gap-2 mb-2">
              <div className="p-3 text-sm font-medium text-gray-500 bg-gray-50 rounded-lg">
                {time}
              </div>
              {weekDays.map(day => {
                const dateKey = format(addDays(startOfWeek(currentWeek, { weekStartsOn: 1 }), weekDays.indexOf(day)), 'yyyy-MM-dd')
                const blocks = schedule[dateKey] || []
                const blockAtTime = blocks.find(block => block.start_time?.slice(0, 5) === time)
                
                return (
                  <div key={`${day}-${time}`} className={`p-2 rounded-lg border-2 transition-all min-h-[70px] ${blockAtTime ? getBlockColor(blockAtTime.block_type) : 'bg-gray-50 border-gray-200'}`}>
                    {blockAtTime && (
                      <div className="h-full flex flex-col gap-1">
                        <div className="flex items-center gap-1 text-xs font-medium">
                          {getBlockIcon(blockAtTime.block_type)}
                          <span>{blockAtTime.block_type}</span>
                        </div>
                        <p className="text-xs font-semibold">{blockAtTime.title}</p>
                        <p className="text-xs opacity-75">
                          {blockAtTime.start_time?.slice(0, 5)} - {blockAtTime.end_time?.slice(0, 5)}
                        </p>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="card p-4 flex justify-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-indigo-100 border border-indigo-300"></div>
          <span className="text-sm">Study</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-purple-100 border border-purple-300"></div>
          <span className="text-sm">Class</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-green-100 border border-green-300"></div>
          <span className="text-sm">Break</span>
        </div>
      </div>

      {/* Generate Modal */}
      {showGenerateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold mb-4">Generate AI Schedule</h2>
            <p className="text-gray-600 mb-6">
              AI will create an optimized study schedule based on your pending tasks and commitments.
            </p>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Study Hours Per Day
              </label>
              <input
                type="range"
                min="1"
                max="8"
                value={studyHours}
                onChange={(e) => setStudyHours(parseInt(e.target.value))}
                className="w-full"
              />
              <div className="text-center mt-2 font-semibold text-indigo-600">
                {studyHours} hours/day
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleGenerateSchedule}
                disabled={generating}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                {generating ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Zap className="h-5 w-5" />
                    Generate Schedule
                  </>
                )}
              </button>
              <button
                onClick={() => setShowGenerateModal(false)}
                className="btn-secondary flex-1"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Schedule