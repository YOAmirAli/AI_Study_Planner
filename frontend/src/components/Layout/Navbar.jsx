import React, { useState } from 'react'
import { Menu, Bell, Search, User, Sun, Moon } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

const Navbar = ({ toggleSidebar }) => {
  const { user } = useAuth()
  const [darkMode, setDarkMode] = useState(false)

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-10">
      <div className="px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <Menu className="h-5 w-5 text-gray-600" />
          </button>
          
          <div className="hidden md:flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2">
            <Search className="h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              className="bg-transparent outline-none text-sm w-64"
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {darkMode ? <Sun className="h-5 w-5 text-gray-600" /> : <Moon className="h-5 w-5 text-gray-600" />}
          </button>
          
          <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors relative">
            <Bell className="h-5 w-5 text-gray-600" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
          </button>
          
          <div className="flex items-center gap-3">
            <div className="text-right hidden md:block">
              <p className="text-sm font-medium text-gray-800">{user?.name || 'Student'}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
            <div className="h-10 w-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center text-white font-semibold">
              {user?.name?.charAt(0) || 'U'}
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar