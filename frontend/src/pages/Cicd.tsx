import { useState } from 'react'
import { Play, AlertCircle, RefreshCw } from 'lucide-react'

const pipelines = [
  {
    id: 'pipe-001',
    name: 'Production Deploy',
    status: 'success',
    last_run: '2026-03-13T08:00:00Z',
    duration: '4m 32s',
    branch: 'main'
  },
  {
    id: 'pipe-002',
    name: 'Staging Deploy',
    status: 'running',
    last_run: '2026-03-13T11:00:00Z',
    progress: 78,
    branch: 'develop'
  },
  {
    id: 'pipe-003',
    name: 'Integration Tests',
    status: 'success',
    last_run: '2026-03-13T07:30:00Z',
    duration: '12m 15s',
    branch: 'main'
  },
  {
    id: 'pipe-004',
    name: 'Security Scan',
    status: 'failed',
    last_run: '2026-03-12T22:00:00Z',
    duration: '8m 45s',
    error: '2 medium vulnerabilities found',
    branch: 'main'
  }
]

const healthServices = [
  { name: 'API', status: 'healthy', latency: '12ms' },
  { name: 'Database', status: 'healthy', latency: '8ms' },
  { name: 'Cache', status: 'healthy', latency: '2ms' },
  { name: 'AI Service', status: 'healthy', latency: '145ms' },
  { name: 'External APIs', status: 'degraded', latency: '320ms' }
]

export default function Cicd() {
  const [triggering, setTriggering] = useState<string | null>(null)
  
  const handleTrigger = (pipelineId: string) => {
    setTriggering(pipelineId)
    setTimeout(() => setTriggering(null), 2000)
  }
  
  return (
    <>
      <div className="section-header">
        <h2 className="section-title">CI/CD Automation</h2>
        <button className="btn btn-primary">
          <RefreshCw size={18} />
          Refresh Status
        </button>
      </div>
      
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <AlertCircle className="card-title-icon" size={20} />
            System Health
          </h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
            {healthServices.map((service, index) => (
              <div key={index} style={{ 
                padding: '16px', 
                background: 'var(--bg-tertiary)', 
                borderRadius: '12px',
                textAlign: 'center'
              }}>
                <div style={{ 
                  width: '12px', 
                  height: '12px', 
                  borderRadius: '50%', 
                  background: service.status === 'healthy' ? '#4ade80' : 'var(--accent-gold)',
                  margin: '0 auto 8px'
                }} />
                <div style={{ fontWeight: 500, marginBottom: '4px' }}>{service.name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>
                  {service.latency}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Play className="card-title-icon" size={20} />
            Pipelines
          </h3>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          <table className="table">
            <thead>
              <tr>
                <th>Pipeline</th>
                <th>Branch</th>
                <th>Status</th>
                <th>Last Run</th>
                <th>Duration</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {pipelines.map(pipe => (
                <tr key={pipe.id}>
                  <td>
                    <div style={{ fontWeight: 500 }}>{pipe.name}</div>
                    {pipe.error && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--accent-crimson)', marginTop: '4px' }}>
                        {pipe.error}
                      </div>
                    )}
                    {pipe.progress && (
                      <div style={{ 
                        height: '4px', 
                        background: 'var(--bg-hover)', 
                        borderRadius: '2px', 
                        marginTop: '8px',
                        overflow: 'hidden'
                      }}>
                        <div style={{ 
                          height: '100%', 
                          width: `${pipe.progress}%`,
                          background: 'var(--accent-gold)',
                          borderRadius: '2px'
                        }} />
                      </div>
                    )}
                  </td>
                  <td>
                    <span style={{ 
                      padding: '4px 8px', 
                      background: 'var(--bg-tertiary)', 
                      borderRadius: '4px',
                      fontSize: '0.8rem',
                      fontFamily: 'var(--font-mono)'
                    }}>
                      {pipe.branch}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge ${pipe.status}`}>
                      {pipe.status}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {new Date(pipe.last_run).toLocaleString()}
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>
                    {pipe.duration || 'Running...'}
                  </td>
                  <td>
                    <button 
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleTrigger(pipe.id)}
                      disabled={triggering === pipe.id}
                    >
                      <Play size={14} />
                      {triggering === pipe.id ? 'Triggering...' : 'Run'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
