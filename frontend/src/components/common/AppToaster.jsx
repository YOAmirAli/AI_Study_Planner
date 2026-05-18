import React from 'react'
import { Toaster } from 'react-hot-toast'
import { useTheme } from '../../contexts/ThemeContext'

const AppToaster = () => {
  const { darkMode } = useTheme()

  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: darkMode ? '#1e293b' : '#ffffff',
          color: darkMode ? '#f1f5f9' : '#1f2937',
          border: darkMode ? '1px solid #334155' : '1px solid #e5e7eb',
          borderRadius: '12px',
          boxShadow: darkMode
            ? '0 10px 25px rgba(0,0,0,0.4)'
            : '0 10px 25px rgba(0,0,0,0.08)',
        },
        success: {
          iconTheme: {
            primary: '#10b981',
            secondary: darkMode ? '#1e293b' : '#ffffff',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444',
            secondary: darkMode ? '#1e293b' : '#ffffff',
          },
        },
      }}
    />
  )
}

export default AppToaster
