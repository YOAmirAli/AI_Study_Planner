import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Mail, Lock, Eye, EyeOff, User, Building, GraduationCap } from 'lucide-react'
import ThemeToggle from '../components/common/ThemeToggle'

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    university: '',
    program: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const emptyForm = {
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    university: '',
    program: ''
  }

  useEffect(() => {
    setFormData(emptyForm)
  }, [])

  const clearAutofill = (e) => {
    e.target.removeAttribute('readonly')
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match')
      return
    }

    setLoading(true)
    const result = await register({
      name: formData.name,
      email: formData.email,
      password: formData.password,
      university: formData.university,
      program: formData.program
    })
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
        <div className="bg-white/80 dark:bg-slate-800/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/50 dark:border-slate-700 max-h-[90vh] overflow-y-auto">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
              Create Account
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-2">Start your learning journey today</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4" autoComplete="off" noValidate>
            <input type="text" name="prevent_autofill" className="hidden" tabIndex={-1} autoComplete="off" aria-hidden="true" />
            <input type="password" name="prevent_autofill_pw" className="hidden" tabIndex={-1} autoComplete="new-password" aria-hidden="true" />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-4 py-2"
                  placeholder="Enter your full name"
                  autoComplete="off"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-4 py-2"
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
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-12 py-2"
                  placeholder="Create a password"
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

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Confirm Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  onFocus={clearAutofill}
                  readOnly
                  className="auth-input pl-10 pr-4 py-2"
                  placeholder="Confirm your password"
                  autoComplete="new-password"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">University (Optional)</label>
              <div className="relative">
                <Building className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type="text"
                  name="university"
                  value={formData.university}
                  onChange={handleChange}
                  className="auth-input pl-10 pr-4 py-2"
                  placeholder="Enter your university"
                  autoComplete="off"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Program (Optional)</label>
              <div className="relative">
                <GraduationCap className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-slate-500" />
                <input
                  type="text"
                  name="program"
                  value={formData.program}
                  onChange={handleChange}
                  className="auth-input pl-10 pr-4 py-2"
                  placeholder="Enter your program"
                  autoComplete="off"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Already have an account?{' '}
              <Link to="/login" className="text-indigo-600 dark:text-indigo-400 font-semibold hover:text-indigo-700 dark:hover:text-indigo-300">
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
