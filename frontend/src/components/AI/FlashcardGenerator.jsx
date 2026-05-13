import React, { useState } from 'react'
import { FileText, Upload, Sparkles, ChevronLeft, ChevronRight, RotateCcw, BookOpen, Download } from 'lucide-react'
import { aiAPI } from '../../api/client'
import toast from 'react-hot-toast'

const FlashcardGenerator = () => {
  const [inputType, setInputType] = useState('text')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [numCards, setNumCards] = useState(10)
  const [loading, setLoading] = useState(false)
  const [flashcards, setFlashcards] = useState(null)
  const [currentCard, setCurrentCard] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

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
      toast.error('Please enter some text to generate flashcards')
      return
    }
    
    if (inputType === 'file' && !file) {
      toast.error('Please select a PDF file')
      return
    }
    
    setLoading(true)
    
    const formData = new FormData()
    if (inputType === 'text') {
      formData.append('text', text)
    } else {
      formData.append('file', file)
    }
    formData.append('num_cards', numCards)
    
    try {
      const response = await aiAPI.generateFlashcards(formData)
      setFlashcards(response.data)
      setCurrentCard(0)
      setIsFlipped(false)
      toast.success('Flashcards generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to generate flashcards')
    } finally {
      setLoading(false)
    }
  }

  const handleNext = () => {
    if (currentCard < flashcards.flashcards.length - 1) {
      setCurrentCard(currentCard + 1)
      setIsFlipped(false)
    }
  }

  const handlePrev = () => {
    if (currentCard > 0) {
      setCurrentCard(currentCard - 1)
      setIsFlipped(false)
    }
  }

  const handleDownload = () => {
    const content = flashcards.flashcards.map((card, idx) => {
      return `Card ${idx + 1}\nQ: ${card.question}\nA: ${card.answer}\n${'='.repeat(50)}`
    }).join('\n\n')
    
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'flashcards.txt'
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Flashcards downloaded!')
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">AI Flashcard Generator</h2>
            <p className="text-gray-500">Create study flashcards from your learning materials</p>
          </div>
        </div>
        
        {!flashcards ? (
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
                    id="flashcard-pdf-upload"
                  />
                  <label
                    htmlFor="flashcard-pdf-upload"
                    className="inline-block mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors"
                  >
                    Select PDF
                  </label>
                  {file && <p className="mt-3 text-sm text-green-600">✓ {file.name}</p>}
                </div>
              </div>
            )}
            
            {/* Number of Cards */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Flashcards: {numCards}
              </label>
              <input
                type="range"
                min="5"
                max="30"
                value={numCards}
                onChange={(e) => setNumCards(parseInt(e.target.value))}
                className="w-full"
              />
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-xl font-semibold hover:from-orange-700 hover:to-red-700 transition-all shadow-lg disabled:opacity-50"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Generating Flashcards...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  <span>Generate Flashcards</span>
                </div>
              )}
            </button>
          </form>
        ) : (
          <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-gray-800">Your Flashcards</h3>
                <p className="text-gray-500">
                  Card {currentCard + 1} of {flashcards.flashcards.length}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleDownload}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Download flashcards"
                >
                  <Download className="h-5 w-5 text-gray-600" />
                </button>
                <button
                  onClick={() => {
                    setFlashcards(null)
                    setCurrentCard(0)
                    setIsFlipped(false)
                  }}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Generate new set"
                >
                  <RotateCcw className="h-5 w-5 text-gray-600" />
                </button>
              </div>
            </div>

            {/* Flashcard */}
            <div className="perspective-1000">
              <div
                className={`relative w-full min-h-[400px] cursor-pointer transition-all duration-500 transform-style-3d ${
                  isFlipped ? 'rotate-y-180' : ''
                }`}
                onClick={() => setIsFlipped(!isFlipped)}
              >
                {/* Front */}
                <div className="absolute inset-0 backface-hidden">
                  <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-8 min-h-[400px] flex flex-col items-center justify-center text-white shadow-xl">
                    <BookOpen className="h-12 w-12 mb-6 opacity-50" />
                    <p className="text-2xl font-semibold text-center leading-relaxed">
                      {flashcards.flashcards[currentCard]?.question}
                    </p>
                    <p className="mt-6 text-sm opacity-75">Click to reveal answer</p>
                  </div>
                </div>
                
                {/* Back */}
                <div className="absolute inset-0 backface-hidden rotate-y-180">
                  <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl p-8 min-h-[400px] flex flex-col items-center justify-center text-white shadow-xl">
                    <Sparkles className="h-12 w-12 mb-6 opacity-50" />
                    <p className="text-xl text-center leading-relaxed">
                      {flashcards.flashcards[currentCard]?.answer}
                    </p>
                    <p className="mt-6 text-sm opacity-75">Click to see question</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Navigation */}
            <div className="flex justify-between items-center gap-4">
              <button
                onClick={handlePrev}
                disabled={currentCard === 0}
                className="flex-1 py-3 rounded-xl border border-gray-300 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <ChevronLeft className="h-5 w-5" />
                Previous
              </button>
              <button
                onClick={handleNext}
                disabled={currentCard === flashcards.flashcards.length - 1}
                className="flex-1 py-3 rounded-xl border border-gray-300 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                Next
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>

            {/* Progress */}
            <div className="flex justify-center gap-2">
              {flashcards.flashcards.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setCurrentCard(idx)
                    setIsFlipped(false)
                  }}
                  className={`h-2 rounded-full transition-all ${
                    idx === currentCard
                      ? 'w-8 bg-indigo-600'
                      : 'w-2 bg-gray-300 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>

            {/* Category Tags */}
            {flashcards.flashcards[currentCard]?.category && (
              <div className="text-center">
                <span className="inline-block px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">
                  {flashcards.flashcards[currentCard].category}
                </span>
              </div>
            )}
          </div>
        )}
      </div>

      <style jsx>{`
        .perspective-1000 {
          perspective: 1000px;
        }
        .transform-style-3d {
          transform-style: preserve-3d;
        }
        .backface-hidden {
          backface-visibility: hidden;
        }
        .rotate-y-180 {
          transform: rotateY(180deg);
        }
      `}</style>
    </div>
  )
}

export default FlashcardGenerator