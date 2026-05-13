import React, { useState, useEffect } from 'react'
import { ClipboardList, Clock, CheckCircle, Award, Play, Eye, Trash2, TrendingUp } from 'lucide-react'
import { quizAPI, taskAPI } from '../api/client'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

const Quizzes = () => {
  const [quizzes, setQuizzes] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({})
  const [timeLeft, setTimeLeft] = useState(null)
  const [quizStarted, setQuizStarted] = useState(false)
  const [quizCompleted, setQuizCompleted] = useState(false)
  const [result, setResult] = useState(null)

  useEffect(() => {
    fetchQuizzes()
  }, [])

  useEffect(() => {
    if (timeLeft > 0 && quizStarted && !quizCompleted) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000)
      return () => clearTimeout(timer)
    } else if (timeLeft === 0 && quizStarted && !quizCompleted) {
      handleSubmitQuiz()
    }
  }, [timeLeft, quizStarted, quizCompleted])

  const fetchQuizzes = async () => {
    try {
      const response = await quizAPI.getAll()
      setQuizzes(response.data.quizzes || [])
    } catch (error) {
      toast.error('Failed to load quizzes')
    } finally {
      setLoading(false)
    }
  }

  const handleStartQuiz = async (quiz) => {
    try {
      const response = await quizAPI.start(quiz.quiz_id)
      setSelectedQuiz(response.data.quiz)
      setCurrentQuestion(0)
      setAnswers({})
      setQuizStarted(true)
      setQuizCompleted(false)
      setResult(null)
      setTimeLeft(quiz.total_questions * 60) // 1 minute per question
      toast.success('Quiz started! Good luck!')
    } catch (error) {
      toast.error('Failed to start quiz')
    }
  }

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }))
  }

  const handleNextQuestion = () => {
    if (currentQuestion < selectedQuiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      handleSubmitQuiz()
    }
  }

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const handleSubmitQuiz = async () => {
    try {
      const response = await quizAPI.submit(selectedQuiz.quiz_id, {
        answers: answers,
        time_taken: (selectedQuiz.total_questions * 60) - timeLeft
      })
      setResult(response.data.result)
      setQuizCompleted(true)
      setQuizStarted(false)
      toast.success(`You scored ${response.data.result.score}/${response.data.result.total_questions}!`)
      fetchQuizzes()
    } catch (error) {
      toast.error('Failed to submit quiz')
    }
  }

  const handleViewResults = async (quiz) => {
    try {
      const response = await quizAPI.getById(quiz.quiz_id)
      setSelectedQuiz(response.data.quiz)
      setResult(response.data.quiz.result)
      setQuizCompleted(true)
      setQuizStarted(false)
    } catch (error) {
      toast.error('Failed to load results')
    }
  }

  const handleDeleteQuiz = async (quizId) => {
    if (window.confirm('Are you sure you want to delete this quiz?')) {
      try {
        await quizAPI.delete(quizId)
        toast.success('Quiz deleted')
        fetchQuizzes()
      } catch (error) {
        toast.error('Failed to delete quiz')
      }
    }
  }

  const getStatusBadge = (status) => {
    switch(status) {
      case 'pending':
        return <span className="badge-warning">Not Started</span>
      case 'in_progress':
        return <span className="badge-info">In Progress</span>
      case 'completed':
        return <span className="badge-success">Completed</span>
      default:
        return null
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  // Quiz taking view
  if (quizStarted && selectedQuiz) {
    const question = selectedQuiz.questions[currentQuestion]
    return (
      <div className="max-w-3xl mx-auto">
        <div className="card p-6">
          {/* Progress */}
          <div className="mb-6">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Question {currentQuestion + 1} of {selectedQuiz.questions.length}</span>
              <span className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                Time left: {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-indigo-600 rounded-full h-2 transition-all"
                style={{ width: `${((currentQuestion + 1) / selectedQuiz.questions.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Question */}
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">{question.question_text}</h3>
            <div className="space-y-3">
              {['A', 'B', 'C', 'D'].map(option => (
                <label
                  key={option}
                  className={`flex items-center gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
                    answers[question.question_id] === option
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name={`question-${question.question_id}`}
                    value={option}
                    checked={answers[question.question_id] === option}
                    onChange={() => handleAnswerSelect(question.question_id, option)}
                    className="w-4 h-4 text-indigo-600"
                  />
                  <span className="font-medium">{option}.</span>
                  <span>{question[`option_${option.toLowerCase()}`]}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between gap-3">
            <button
              onClick={handlePreviousQuestion}
              disabled={currentQuestion === 0}
              className="px-6 py-2 rounded-xl border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <button
              onClick={handleNextQuestion}
              className="px-6 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700"
            >
              {currentQuestion === selectedQuiz.questions.length - 1 ? 'Submit' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Results view
  if (quizCompleted && selectedQuiz && result) {
    const percentage = (result.score / result.total_questions) * 100
    return (
      <div className="max-w-3xl mx-auto">
        <div className="card p-6 text-center">
          <div className={`inline-flex p-4 rounded-full mb-4 ${
            percentage >= 80 ? 'bg-green-100' : percentage >= 60 ? 'bg-yellow-100' : 'bg-red-100'
          }`}>
            <Award className={`h-12 w-12 ${
              percentage >= 80 ? 'text-green-600' : percentage >= 60 ? 'text-yellow-600' : 'text-red-600'
            }`} />
          </div>
          
          <h2 className="text-2xl font-bold mb-2">Quiz Completed!</h2>
          <p className="text-gray-600 mb-6">{selectedQuiz.title}</p>
          
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="p-4 bg-gray-50 rounded-xl">
              <p className="text-2xl font-bold text-indigo-600">{result.score}/{result.total_questions}</p>
              <p className="text-sm text-gray-500">Score</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-xl">
              <p className="text-2xl font-bold text-green-600">{percentage.toFixed(1)}%</p>
              <p className="text-sm text-gray-500">Percentage</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-xl">
              <p className="text-2xl font-bold text-blue-600">{Math.floor(result.time_taken / 60)}:{String(result.time_taken % 60).padStart(2, '0')}</p>
              <p className="text-sm text-gray-500">Time Taken</p>
            </div>
          </div>
          
          <button
            onClick={() => {
              setQuizCompleted(false)
              setSelectedQuiz(null)
              setResult(null)
            }}
            className="btn-primary"
          >
            Back to Quizzes
          </button>
        </div>

        {/* Review Questions */}
        <div className="mt-6 space-y-4">
          <h3 className="text-xl font-bold">Review Answers</h3>
          {selectedQuiz.questions.map((q, idx) => (
            <div key={q.question_id} className="card p-4">
              <p className="font-semibold mb-2">{idx + 1}. {q.question_text}</p>
              <p className="text-sm">Your answer: <span className={q.is_correct ? 'text-green-600' : 'text-red-600'}>{q.user_answer}</span></p>
              <p className="text-sm">Correct answer: <span className="text-green-600">{q.correct_answer}</span></p>
              {q.explanation && <p className="text-sm text-gray-600 mt-2">{q.explanation}</p>}
            </div>
          ))}
        </div>
      </div>
    )
  }

  // Quiz list view
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Quizzes</h1>
        <p className="text-gray-600 mt-1">Test your knowledge with AI-generated quizzes</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Quizzes</p>
              <p className="text-2xl font-bold">{quizzes.length}</p>
            </div>
            <ClipboardList className="h-8 w-8 text-indigo-500" />
          </div>
        </div>
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Completed</p>
              <p className="text-2xl font-bold text-green-600">{quizzes.filter(q => q.status === 'completed').length}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-500" />
          </div>
        </div>
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Pending</p>
              <p className="text-2xl font-bold text-yellow-600">{quizzes.filter(q => q.status === 'pending').length}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-500" />
          </div>
        </div>
      </div>

      {/* Quizzes List */}
      <div className="space-y-4">
        {quizzes.map((quiz) => (
          <div key={quiz.quiz_id} className="card p-6 hover:shadow-lg transition-all">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-gray-800">{quiz.title}</h3>
                  {getStatusBadge(quiz.status)}
                </div>
                {quiz.description && <p className="text-gray-600 mb-3">{quiz.description}</p>}
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>{quiz.total_questions} questions</span>
                  <span>Created: {format(new Date(quiz.created_at), 'MMM dd, yyyy')}</span>
                  {quiz.result && (
                    <span className="text-green-600 flex items-center gap-1">
                      <TrendingUp className="h-4 w-4" />
                      Score: {quiz.result.score}/{quiz.result.total_questions}
                    </span>
                  )}
                </div>
              </div>
              <div className="flex gap-2">
                {quiz.status === 'pending' && (
                  <button
                    onClick={() => handleStartQuiz(quiz)}
                    className="p-2 rounded-lg bg-green-50 text-green-600 hover:bg-green-100"
                  >
                    <Play className="h-5 w-5" />
                  </button>
                )}
                {quiz.status === 'completed' && (
                  <button
                    onClick={() => handleViewResults(quiz)}
                    className="p-2 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100"
                  >
                    <Eye className="h-5 w-5" />
                  </button>
                )}
                <button
                  onClick={() => handleDeleteQuiz(quiz.quiz_id)}
                  className="p-2 rounded-lg bg-red-50 text-red-600 hover:bg-red-100"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {quizzes.length === 0 && (
        <div className="text-center py-12">
          <ClipboardList className="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No quizzes yet</h3>
          <p className="text-gray-500">Complete tasks to generate AI-powered quizzes</p>
        </div>
      )}
    </div>
  )
}

export default Quizzes