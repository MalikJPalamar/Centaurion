import { useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  BrainCircuit, 
  LineChart, 
  GitBranch, 
  Settings,
  Search,
  Bell,
  Shield,
  Menu,
  X
} from 'lucide-react'
import Dashboard from './pages/Dashboard'
import AIOperations from './pages/AIOperations'
import MarketIntelligence from './pages/MarketIntelligence'
import Cicd from './pages/Cicd'
import SettingsPage from './pages/Settings'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/ai-operations', icon: BrainCircuit, label: 'AI Operations' },
  { path: '/market-intelligence', icon: LineChart, label: 'Market Intelligence' },
  { path: '/cicd', icon: GitBranch, label: 'CI/CD Automation' },
  { path: '/settings', icon: Settings, label: 'Settings' },
]

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  
  return (
    <BrowserRouter>
      <div className="app-layout">
        <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
          <div className="sidebar-header">
            <div className="logo">
              <div className="logo-icon">C</div>
              <span>Centaurion</span>
            </div>
            <div className="logo-subtitle">Cognitive OS</div>
          </div>
          
          <nav className="sidebar-nav">
            <div className="nav-section">
              <div className="nav-section-title">Main</div>
              {navItems.slice(0, 1).map(item => (
                <NavLink 
                  key={item.path} 
                  to={item.path} 
                  className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                  end
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="nav-icon" />
                  {item.label}
                </NavLink>
              ))}
            </div>
            
            <div className="nav-section">
              <div className="nav-section-title">Modules</div>
              {navItems.slice(1, 4).map(item => (
                <NavLink 
                  key={item.path} 
                  to={item.path} 
                  className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="nav-icon" />
                  {item.label}
                </NavLink>
              ))}
            </div>
            
            <div className="nav-section">
              <div className="nav-section-title">System</div>
              {navItems.slice(4).map(item => (
                <NavLink 
                  key={item.path} 
                  to={item.path} 
                  className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="nav-icon" />
                  {item.label}
                </NavLink>
              ))}
            </div>
          </nav>
          
          <div className="sidebar-footer">
            <div className="system-status">
              <span className="status-dot"></span>
              <span>All Systems Operational</span>
            </div>
          </div>
        </aside>
        
        <main className="main-content">
          <header className="header">
            <div className="header-left">
              <button className="mobile-menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
                {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
              <h1 className="page-title">Centaurion</h1>
            </div>
            <div className="header-right">
              <div className="search-bar">
                <Search size={18} color="var(--text-tertiary)" />
                <input type="text" placeholder="Search..." />
                <span className="search-shortcut">⌘K</span>
              </div>
              <button className="icon-btn">
                <Bell size={20} />
                <span className="notification-badge"></span>
              </button>
              <button className="icon-btn">
                <Shield size={20} />
              </button>
            </div>
          </header>
          
          <div className="page-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/ai-operations" element={<AIOperations />} />
              <Route path="/market-intelligence" element={<MarketIntelligence />} />
              <Route path="/cicd" element={<Cicd />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </div>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
