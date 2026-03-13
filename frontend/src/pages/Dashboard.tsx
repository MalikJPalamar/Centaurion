import { useEffect, useState } from 'react'
import { 
  BrainCircuit, 
  Activity, 
  CheckCircle, 
  AlertTriangle,
  TrendingUp,
  GitBranch,
  Server
} from 'lucide-react'

interface DashboardStats {
  total_operations: number
  active_operations: number
  completed_today: number
  success_rate: number
  system_health: number
  active_pipelines: number
  recent_activity: Array<{
    type: string
    message: string
    time: string
  }>
}

const mockStats: DashboardStats = {
  total_operations: 127,
  active_operations: 3,
  completed_today: 12,
  success_rate: 94.5,
  system_health: 98,
  active_pipelines: 2,
  recent_activity: [
    { type: 'operation', message: 'Market Analysis completed', time: '10m ago' },
    { type: 'pipeline', message: 'Production Deploy succeeded', time: '2h ago' },
    { type: 'system', message: 'Health check passed', time: '5m ago' }
  ]
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  
  useEffect(() => {
    fetch('/api/dashboard/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(() => setStats(mockStats))
  }, [])
  
  const displayStats = stats || mockStats
  
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'operation': return BrainCircuit
      case 'pipeline': return GitBranch
      case 'system': return Server
      default: return Activity
    }
  }
  
  return (
    <>
      <div className="dashboard-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <BrainCircuit size={24} />
          </div>
          <div className="stat-value">{displayStats.total_operations}</div>
          <div className="stat-label">Total Operations</div>
          <div className="stat-trend up">
            <TrendingUp size={14} />
            <span>+12% this week</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-value">{displayStats.active_operations}</div>
          <div className="stat-label">Active Operations</div>
          <div className="stat-trend up">
            <TrendingUp size={14} />
            <span>Running now</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <CheckCircle size={24} />
          </div>
          <div className="stat-value">{displayStats.completed_today}</div>
          <div className="stat-label">Completed Today</div>
          <div className="stat-trend up">
            <TrendingUp size={14} />
            <span>+3 from yesterday</span>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <AlertTriangle size={24} />
          </div>
          <div className="stat-value">{displayStats.system_health}%</div>
          <div className="stat-label">System Health</div>
          <div className="stat-trend up">
            <TrendingUp size={14} />
            <span>Optimal</span>
          </div>
        </div>
      </div>
      
      <div className="two-col-grid">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Activity className="card-title-icon" size={20} />
              Recent Activity
            </h3>
            <button className="btn btn-ghost btn-sm">View All</button>
          </div>
          <div className="card-body">
            <div className="activity-list">
              {displayStats.recent_activity.map((activity, index) => {
                const Icon = getActivityIcon(activity.type)
                return (
                  <div key={index} className="activity-item">
                    <div className={`activity-icon ${activity.type}`}>
                      <Icon size={18} />
                    </div>
                    <div className="activity-content">
                      <div className="activity-title">{activity.message}</div>
                      <div className="activity-time">{activity.time}</div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <GitBranch className="card-title-icon" size={20} />
              Pipeline Status
            </h3>
            <button className="btn btn-ghost btn-sm">Manage</button>
          </div>
          <div className="card-body">
            <div className="activity-list">
              <div className="activity-item">
                <div className="activity-icon pipeline">
                  <GitBranch size={18} />
                </div>
                <div className="activity-content">
                  <div className="activity-title">Production Deploy</div>
                  <div className="activity-time">Last run: 2 hours ago • 4m 32s</div>
                </div>
                <span className="status-badge success">Success</span>
              </div>
              <div className="activity-item">
                <div className="activity-icon pipeline">
                  <GitBranch size={18} />
                </div>
                <div className="activity-content">
                  <div className="activity-title">Staging Deploy</div>
                  <div className="activity-time">Running now...</div>
                </div>
                <span className="status-badge running">Running</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
