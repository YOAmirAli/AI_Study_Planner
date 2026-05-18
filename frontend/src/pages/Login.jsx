import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Mail, Lock, Eye, EyeOff, GraduationCap, Sparkles } from 'lucide-react'
import ThemeToggle from '../components/common/ThemeToggle'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    setEmail('')
    setPassword('')
  }, [])

  const clearAutofill = (e) => {
    e.target.removeAttribute('readonly')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const result = await login(email, password)
    setLoading(false)
    if (result.success) {
      navigate('/')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-900 p-4">
      <div className="absolute top-4 right-4 z-20">
        <ThemeToggle />
      </div>

      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-indigo-200 dark:bg-indigo-900/40 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-200 dark:bg-purple-900/40 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse delay-1000" />
      </div>

      <div className="relative w-full max-w-md">
        <div className="bg-white/80 dark:bg-slate-800/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/50 dark:border-slate-700 animate-fade-in">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-lg mb-4">
              <GraduationCap className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
              StudyAI Planner
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-2">Your AI-powered learning companion</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5" autoComplete="off" noValidate>
            <input type="text" name="prevent_autofill" className="hidden" tabIndex={-1} autoComplete="off" aria-hidden="true" />
            <input type="password" name="prevent_autofill_pw" className="hidden" tabIndex={-1} autoComplete="new-password" aria-hidden="true" />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type="email"
                  name="login_email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-4"
                  placeholder="Enter your email"
                  autoComplete="off"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="login_password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-12"
                  placeholder="Enter your password"
                  autoComplete="new-password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2"
                >
                  {showPassword ? <EyeOff className="h-5 w-5 text-gray-400" /> : <Eye className="h-5 w-5 text-gray-400" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2">
                <input type="checkbox" className="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-slate-600" />
                <span className="text-sm text-gray-600 dark:text-gray-400">Remember me</span>
              </label>
              <a href="#" className="text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300">Forgot password?</a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                  <span>Logging in...</span>
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Don&apos;t have an account?{' '}
              <Link to="/register" className="text-indigo-600 dark:text-indigo-400 font-semibold hover:text-indigo-700 dark:hover:text-indigo-300">
                Create Account
              </Link>
            </p>
          </div>

          <div className="mt-8 flex items-center justify-center gap-2 text-xs text-gray-400 dark:text-gray-500">
            <Sparkles className="h-3 w-3" />
            <span>Powered by Amir and usman</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
