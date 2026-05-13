import React, { useState } from 'react'
import { FileText, Upload, Sparkles, CheckCircle, XCircle, HelpCircle } from 'lucide-react'
import { aiAPI } from '../../api/client'
import toast from 'react-hot-toast'

const QuizGenerator = () => {
  const [inputType, setInputType] = useState('text')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [numQuestions, setNumQuestions] = useState(10)
  const [questionType, setQuestionType] = useState('mixed')
  const [loading, setLoading] = useState(false)
  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      toast.error('Please upload a PDF file')
      return
    }
    setFile(selectedFile)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (inputType === 'text' && !text.trim()) {
      toast.error('Please enter some text to generate quiz')
      return
    }
    
    if (inputType === 'file' && !file) {
      toast.error('Please select a PDF file')
      return
    }
    
    setLoading(true)
    setSubmitted(false)
    setAnswers({})
    setScore(null)
    
    const formData = new FormData()
    if (inputType === 'text') {
      formData.append('text', text)
    } else {
      formData.append('file', file)
    }
    formData.append('num_questions', numQuestions)
    formData.append('question_type', questionType)
    
    try {
      const response = await aiAPI.generateQuiz(formData)
      setQuiz(response.data)
      toast.success('Quiz generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to generate quiz')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = (questionIndex, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }))
  }

  const handleSubmitQuiz = () => {
    let correct = 0
    quiz.questions.forEach((q, idx) => {
      if (answers[idx] === q.correct_answer) {
        correct++
      }
    })
    const percentage = (correct / quiz.questions.length) * 100
    setScore({ correct, total: quiz.questions.length, percentage })
    setSubmitted(true)
    toast.success(`You scored ${correct}/${quiz.questions.length}!`)
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">AI Quiz Generator</h2>
            <p className="text-gray-500">Create personalized quizzes from your study materials</p>
          </div>
        </div>
        
        {!quiz ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Input Type Toggle */}
            <div className="flex gap-4 p-1 bg-gray-100 rounded-xl">
              {['text', 'file'].map(type => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setInputType(type)}
                  className={`flex-1 py-2 rounded-lg font-medium transition-all ${
                    inputType === type 
                      ? 'bg-white text-indigo-600 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  {type === 'text' ? 'Paste Text' : 'Upload PDF'}
                </button>
              ))}
            </div>
            
            {/* Text Input */}
            {inputType === 'text' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Source Material
                </label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  rows={10}
                  className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-none"
                  placeholder="Paste your study material here..."
                />
              </div>
            )}
            
            {/* File Input */}
            {inputType === 'file' && (
              <div>
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-indigo-500 transition-colors">
                  <Upload className="h-10 w-10 mx-auto text-gray-400 mb-3" />
                  <p className="text-gray-600">Upload PDF document</p>
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="hidden"
                    id="quiz-pdf-upload"
                  />
                  <label
                    htmlFor="quiz-pdf-upload"
                    className="inline-block mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors"
                  >
                    Select PDF
                  </label>
                  {file && <p className="mt-3 text-sm text-green-600">✓ {file.name}</p>}
                </div>
              </div>
            )}
            
            {/* Number of Questions */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Questions: {numQuestions}
              </label>
              <input
                type="range"
                min="5"
                max="20"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                className="w-full"
              />
            </div>
            
            {/* Question Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Question Type
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'mcq', label: 'Multiple Choice', desc: '4 options each' },
                  { value: 'short_answer', label: 'Short Answer', desc: 'Written response' },
                  { value: 'mixed', label: 'Mixed', desc: 'Combination of both' }
                ].map(option => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => setQuestionType(option.value)}
                    className={`p-3 rounded-xl border-2 transition-all ${
                      questionType === option.value
                        ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-semibold">{option.label}</div>
                    <div className="text-xs text-gray-500">{option.desc}</div>
                  </button>
                ))}
              </div>
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transition-all shadow-lg disabled:opacity-50"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Generating Quiz...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  <span>Generate Quiz</span>
                </div>
              )}
            </button>
          </form>
        ) : (
          <div className="space-y-6">
            {/* Quiz Header */}
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-gray-800">{quiz.quiz_title || 'Generated Quiz'}</h3>
                <p className="text-gray-500">{quiz.total_questions} questions</p>
              </div>
              {!submitted && (
                <button
                  onClick={handleSubmitQuiz}
                  className="btn-primary"
                >
                  Submit Quiz
                </button>
              )}
            </div>

            {/* Score Display */}
            {submitted && score && (
              <div className={`p-6 rounded-xl text-center ${
                score.percentage >= 80 ? 'bg-green-50 border border-green-200' :
                score.percentage >= 60 ? 'bg-yellow-50 border border-yellow-200' :
                'bg-red-50 border border-red-200'
              }`}>
                <h4 className="text-2xl font-bold mb-2">Your Score</h4>
                <p className="text-4xl font-bold mb-2">{score.correct}/{score.total}</p>
                <p className="text-xl">{score.percentage.toFixed(1)}%</p>
                <p className="mt-2 text-gray-600">
                  {score.percentage >= 80 ? 'Excellent! 🎉' : 
                   score.percentage >= 60 ? 'Good job! Keep practicing 📚' : 
                   'Keep studying! You can do better 💪'}
                </p>
              </div>
            )}

            {/* Questions */}
            <div className="space-y-6">
              {quiz.questions.map((q, idx) => (
                <div key={idx} className="p-6 bg-gray-50 rounded-xl">
                  <p className="font-semibold text-gray-800 mb-4">
                    {idx + 1}. {q.question}
                  </p>
                  
                  {q.options ? (
                    // Multiple Choice
                    <div className="space-y-2 ml-4">
                      {q.options.map((option, optIdx) => {
                        const optionLetter = String.fromCharCode(65 + optIdx)
                        const isSelected = answers[idx] === optionLetter
                        const isCorrect = submitted && optionLetter === q.correct_answer
                        const isWrong = submitted && isSelected && optionLetter !== q.correct_answer
                        
                        return (
                          <label
                            key={optIdx}
                            className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all ${
                              submitted ? 'cursor-default' : 'hover:bg-gray-100'
                            } ${
                              isCorrect ? 'bg-green-100 border border-green-300' :
                              isWrong ? 'bg-red-100 border border-red-300' :
                              isSelected ? 'bg-indigo-100 border border-indigo-300' :
                              'border border-transparent'
                            }`}
                          >
                            <input
                              type="radio"
                              name={`question-${idx}`}
                              value={optionLetter}
                              checked={isSelected}
                              onChange={() => !submitted && handleAnswerSelect(idx, optionLetter)}
                              disabled={submitted}
                              className="w-4 h-4 text-indigo-600"
                            />
                            <span className="font-medium">{optionLetter}.</span>
                            <span>{option.substring(2)}</span>
                            {submitted && optionLetter === q.correct_answer && (
                              <CheckCircle className="h-5 w-5 text-green-500 ml-auto" />
                            )}
                            {submitted && isSelected && optionLetter !== q.correct_answer && (
                              <XCircle className="h-5 w-5 text-red-500 ml-auto" />
                            )}
                          </label>
                        )
                      })}
                    </div>
                  ) : (
                    // Short Answer
                    <div className="ml-4">
                      <textarea
                        className="w-full p-3 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
                        rows="3"
                        placeholder="Type your answer here..."
                        value={answers[idx] || ''}
                        onChange={(e) => !submitted && handleAnswerSelect(idx, e.target.value)}
                        disabled={submitted}
                      />
                    </div>
                  )}
                  
                  {/* Explanation */}
                  {submitted && q.explanation && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <HelpCircle className="h-4 w-4 text-blue-600" />
                        <p className="text-sm font-semibold text-blue-800">Explanation</p>
                      </div>
                      <p className="text-sm text-blue-700">{q.explanation}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Regenerate Button */}
            <button
              onClick={() => {
                setQuiz(null)
                setSubmitted(false)
                setAnswers({})
                setScore(null)
              }}
              className="w-full btn-secondary"
            >
              Generate New Quiz
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default QuizGenerator