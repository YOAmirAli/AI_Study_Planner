import React, { useState } from 'react'
import { FileText, Upload, Sparkles, Download, Copy, Check } from 'lucide-react'
import { aiAPI } from '../../api/client'
import toast from 'react-hot-toast'

const Summarizer = () => {
  const [inputType, setInputType] = useState('text')
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [length, setLength] = useState('moderate')
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState(null)
  const [copied, setCopied] = useState(false)

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
      toast.error('Please enter some text to summarize')
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
    formData.append('length', length)
    
    try {
      const response = await aiAPI.summarize(formData)
      setSummary(response.data)
      toast.success('Summary generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to generate summary')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (summary?.summary) {
      navigator.clipboard.writeText(summary.summary)
      setCopied(true)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleDownload = () => {
    if (summary?.summary) {
      const blob = new Blob([summary.summary], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'summary.txt'
      a.click()
      URL.revokeObjectURL(url)
      toast.success('Downloaded!')
    }
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">AI Text Summarizer</h2>
            <p className="text-gray-500">Transform long texts into concise summaries</p>
          </div>
        </div>
        
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
                Text to Summarize
              </label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={10}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-none"
                placeholder="Paste your text here (minimum 50 characters)..."
              />
              <p className="text-xs text-gray-500 mt-1">
                {text.length} characters • Minimum 50 recommended
              </p>
            </div>
          )}
          
          {/* File Input */}
          {inputType === 'file' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                PDF File
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-indigo-500 transition-colors">
                <Upload className="h-10 w-10 mx-auto text-gray-400 mb-3" />
                <p className="text-gray-600">Click or drag to upload PDF</p>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                  id="pdf-upload"
                />
                <label
                  htmlFor="pdf-upload"
                  className="inline-block mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition-colors"
                >
                  Select File
                </label>
                {file && <p className="mt-3 text-sm text-green-600">✓ {file.name}</p>}
              </div>
            </div>
          )}
          
          {/* Summary Length */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Summary Length
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'brief', label: 'Brief', desc: '2-3 sentences' },
                { value: 'moderate', label: 'Moderate', desc: '1-2 paragraphs' },
                { value: 'detailed', label: 'Detailed', desc: 'Full summary' }
              ].map(option => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setLength(option.value)}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    length === option.value
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
            className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg disabled:opacity-50"
          >
            {loading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Generating Summary...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2">
                <Sparkles className="h-5 w-5" />
                <span>Generate Summary</span>
              </div>
            )}
          </button>
        </form>
        
        {/* Results */}
        {summary && (
          <div className="mt-8 pt-6 border-t border-gray-200 animate-fade-in">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <FileText className="h-5 w-5 text-indigo-600" />
                Generated Summary
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={handleCopy}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Copy to clipboard"
                >
                  {copied ? <Check className="h-5 w-5 text-green-500" /> : <Copy className="h-5 w-5 text-gray-500" />}
                </button>
                <button
                  onClick={handleDownload}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Download summary"
                >
                  <Download className="h-5 w-5 text-gray-500" />
                </button>
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-gray-50 to-indigo-50/30 rounded-xl p-6">
              <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                {summary.summary}
              </p>
            </div>
            
            <div className="mt-4 grid grid-cols-3 gap-4 text-center">
              <div className="bg-gray-50 rounded-xl p-3">
                <p className="text-xs text-gray-500">Original</p>
                <p className="font-semibold text-gray-800">{summary.original_length} chars</p>
              </div>
              <div className="bg-gray-50 rounded-xl p-3">
                <p className="text-xs text-gray-500">Summary</p>
                <p className="font-semibold text-gray-800">{summary.summary_length} chars</p>
              </div>
              <div className="bg-gray-50 rounded-xl p-3">
                <p className="text-xs text-gray-500">Compression</p>
                <p className="font-semibold text-green-600">{summary.compression_ratio}%</p>
              </div>
            </div>
            
            {summary.ai_provider && (
              <p className="text-xs text-center text-gray-400 mt-4">
                Powered by {summary.ai_provider === 'openai' ? 'OpenAI GPT-4' : 'Groq'}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Summarizer