import React, { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from '../components/Layout/Sidebar'
import Navbar from '../components/Layout/Navbar'

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      
      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
        <Navbar toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout