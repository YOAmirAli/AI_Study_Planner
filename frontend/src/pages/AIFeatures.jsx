import React, { useState } from 'react'
import { Sparkles, FileText, ClipboardList, Layers, MessageSquare, Video, Zap, Brain, TrendingUp } from 'lucide-react'
import Summarizer from '../components/AI/Summarizer'
import QuizGenerator from '../components/AI/QuizGenerator'
import FlashcardGenerator from '../components/AI/FlashcardGenerator'
import TaskTutor from '../components/AI/TaskTutor'
import Recommender from '../components/AI/Recommender'

const features = [
  { id: 'summarizer', name: 'Text Summarizer', icon: FileText, description: 'Summarize any text or PDF document', color: 'from-blue-500 to-cyan-500' },
  { id: 'quiz', name: 'Quiz Generator', icon: ClipboardList, description: 'Generate AI-powered quizzes', color: 'from-green-500 to-emerald-500' },
  { id: 'flashcards', name: 'Flashcards', icon: Layers, description: 'Create study flashcards automatically', color: 'from-orange-500 to-red-500' },
  { id: 'tutor', name: 'AI Tutor', icon: MessageSquare, description: 'Get personalized learning guidance', color: 'from-purple-500 to-pink-500' },
  { id: 'recommend', name: 'Recommendations', icon: Video, description: 'Discover learning resources', color: 'from-indigo-500 to-purple-500' },
]

const AIFeatures = () => {
  const [activeFeature, setActiveFeature] = useState('summarizer')

  const renderFeature = () => {
    switch(activeFeature) {
      case 'summarizer': return <Summarizer />
      case 'quiz': return <QuizGenerator />
      case 'flashcards': return <FlashcardGenerator />
      case 'tutor': return <TaskTutor />
      case 'recommend': return <Recommender />
      default: return <Summarizer />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 text-white">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Brain className="h-8 w-8" />
              <h1 className="text-3xl font-bold">Nova AI</h1>
            </div>
            <p className="text-indigo-100 text-lg">
              Hybrid AI: Gemini · Trained T5 flashcards · YouTube recommendations
            </p>
            <div className="flex gap-3 mt-4">
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2">
                <Zap className="h-4 w-4 text-yellow-400" />
                <span className="text-sm">Real-time AI</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-2">
                <TrendingUp className="h-4 w-4 text-green-400" />
                <span className="text-sm">Smart Learning</span>
              </div>
            </div>
          </div>
          <Sparkles className="h-12 w-12 text-yellow-400 animate-pulse" />
        </div>
      </div>

      {/* Feature Navigation */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {features.map(feature => (
          <button
            key={feature.id}
            onClick={() => setActiveFeature(feature.id)}
            className={`card p-4 text-center transition-all hover:scale-105 ${
              activeFeature === feature.id 
                ? `bg-gradient-to-r ${feature.color} text-white shadow-lg` 
                : 'bg-white hover:shadow-md'
            }`}
          >
            <feature.icon className={`h-8 w-8 mx-auto mb-2 ${activeFeature === feature.id ? 'text-white' : 'text-indigo-600'}`} />
            <h3 className={`font-semibold ${activeFeature === feature.id ? 'text-white' : 'text-gray-800'}`}>
              {feature.name}
            </h3>
            <p className={`text-xs mt-1 ${activeFeature === feature.id ? 'text-white/80' : 'text-gray-500'}`}>
              {feature.description}
            </p>
          </button>
        ))}
      </div>

      {/* Feature Content */}
      <div className="animate-fade-in">
        {renderFeature()}
      </div>
    </div>
  )
}

export default AIFeatures