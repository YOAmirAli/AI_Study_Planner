import React from 'react'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../../contexts/ThemeContext'

const ThemeToggle = ({ className = '' }) => {
  const { darkMode, toggleTheme } = useTheme()

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
      className={`p-2 rounded-lg transition-colors hover:bg-gray-100 dark:hover:bg-slate-700 ${className}`}
    >
      {darkMode ? (
        <Sun className="h-5 w-5 text-amber-400" />
      ) : (
        <Moon className="h-5 w-5 text-gray-600 dark:text-slate-300" />
      )}
    </button>
  )
}

export default ThemeToggle
