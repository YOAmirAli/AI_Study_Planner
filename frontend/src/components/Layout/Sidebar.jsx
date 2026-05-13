import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, BookOpen, CheckSquare, Calendar, 
  Brain, Users, FolderOpen, BarChart3, User,
  LogOut, Sparkles, GraduationCap, Trophy
} from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

const menuItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard', color: 'text-indigo-500' },
  { path: '/courses', icon: BookOpen, label: 'Courses', color: 'text-blue-500' },
  { path: '/tasks', icon: CheckSquare, label: 'Tasks', color: 'text-green-500' },
  { path: '/schedule', icon: Calendar, label: 'Schedule', color: 'text-purple-500' },
  { path: '/ai-features', icon: Brain, label: 'AI Features', color: 'text-pink-500' },
  { path: '/groups', icon: Users, label: 'Study Groups', color: 'text-orange-500' },
  { path: '/resources', icon: FolderOpen, label: 'Resources', color: 'text-cyan-500' },
  { path: '/quizzes', icon: BarChart3, label: 'Quizzes', color: 'text-red-500' },
  { path: '/analytics', icon: Trophy, label: 'Analytics', color: 'text-yellow-500' },
  { path: '/profile', icon: User, label: 'Profile', color: 'text-gray-500' },
]

const Sidebar = ({ isOpen, setIsOpen }) => {
  const { logout } = useAuth()

  return (
    <div className={`fixed left-0 top-0 h-full bg-gradient-to-b from-gray-900 to-gray-800 text-white transition-all duration-300 z-20 shadow-2xl ${isOpen ? 'w-64' : 'w-20'}`}>
      {/* Logo */}
      <div className="flex items-center justify-center h-20 border-b border-gray-700">
        {isOpen ? (
          <div className="flex items-center gap-2">
            <GraduationCap className="h-8 w-8 text-indigo-400" />
            <span className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              StudyAI
            </span>
            <Sparkles className="h-4 w-4 text-yellow-400" />
          </div>
        ) : (
          <GraduationCap className="h-8 w-8 text-indigo-400" />
        )}
      </div>

      {/* Navigation */}
      <nav className="mt-8">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 mx-3 my-1 rounded-xl transition-all duration-200 group ${
                isActive
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
              }`
            }
          >
            <item.icon className={`h-5 w-5 ${isOpen ? 'mr-3' : 'mx-auto'} transition-transform group-hover:scale-110`} />
            {isOpen && (
              <span className="font-medium">{item.label}</span>
            )}
          </NavLink>
        ))}

        {/* Logout button */}
        <button
          onClick={logout}
          className="flex items-center px-4 py-3 mx-3 my-1 mt-8 rounded-xl text-gray-300 hover:bg-red-500/20 hover:text-red-400 transition-all duration-200 w-full"
        >
          <LogOut className={`h-5 w-5 ${isOpen ? 'mr-3' : 'mx-auto'}`} />
          {isOpen && <span className="font-medium">Logout</span>}
        </button>
      </nav>

      {/* Footer */}
      {isOpen && (
        <div className="absolute bottom-0 left-0 right-0 p-4 text-center text-xs text-gray-500 border-t border-gray-700">
          <p>© 2024 StudyAI</p>
          <p className="mt-1">Smart Learning Platform</p>
        </div>
      )}
    </div>
  )
}

export default Sidebar