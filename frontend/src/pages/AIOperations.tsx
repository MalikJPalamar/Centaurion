import { useState } from 'react'
import { Plus, Play, Pause, RotateCcw } from 'lucide-react'

interface AIOperation {
  id: string
  name: string
  type: string
  status: string
  created_at: string
  progress?: number
  result?: string
  error?: string
}

const mockOperations: AIOperation[] = [
  {
    id: 'op-001',
    name: 'Market Analysis - Tech Sector',
    type: 'market_analysis',
    status: 'completed',
    created_at: '2026-03-13T10:30:00Z',
    result: 'Analysis complete - 47 opportunities identified'
  },
  {
    id: 'op-002',
    name: 'Competitor Monitoring',
    type: 'monitoring',
    status: 'running',
    created_at: '2026-03-13T11:00:00Z',
    progress: 65
  },
  {
    id: 'op-003',
    name: 'Content Generation - Q1 Report',
    type: 'content_generation',
    status: 'queued',
    created_at: '2026-03-13T11:30:00Z'
  },
  {
    id: 'op-004',
    name: 'Data Processing Pipeline',
    type: 'data_processing',
    status: 'completed',
    created_at: '2026-03-12T14:00:00Z',
    result: 'Processed 15,000 records'
  },
  {
    id: 'op-005',
    name: 'Sentiment Analysis',
    type: 'nlp_analysis',
    status: 'failed',
    created_at: '2026-03-12T09:00:00Z',
    error: 'API rate limit exceeded'
  }
]

export default function AIOperations() {
  const [operations, setOperations] = useState<AIOperation[]>(mockOperations)
  const [showCreate, setShowCreate] = useState(false)
  const [newOpName, setNewOpName] = useState('')
  const [newOpType, setNewOpType] = useState('general')
  
  const handleCreate = () => {
    if (!newOpName.trim()) return
    
    const newOp: AIOperation = {
      id: `op-${Date.now()}`,
      name: newOpName,
      type: newOpType,
      status: 'queued',
      created_at: new Date().toISOString()
    }
    
    setOperations([newOp, ...operations])
    setNewOpName('')
    setShowCreate(false)
  }
  
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'market_analysis': return '📊'
      case 'monitoring': return '👁️'
      case 'content_generation': return '📝'
      case 'data_processing': return '⚙️'
      case 'nlp_analysis': return '🧠'
      default: return '🎯'
    }
  }
  
  return (
    <>
      <div className="section-header">
        <h2 className="section-title">AI Operations</h2>
        <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
          <Plus size={18} />
          New Operation
        </button>
      </div>
      
      {showCreate && (
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <h3 className="card-title">Create New Operation</h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '16px', maxWidth: '500px' }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Operation Name</label>
                <input 
                  type="text" 
                  className="form-input"
                  placeholder="Enter operation name..."
                  value={newOpName}
                  onChange={(e) => setNewOpName(e.target.value)}
                />
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Type</label>
                <select 
                  className="form-input"
                  value={newOpType}
                  onChange={(e) => setNewOpType(e.target.value)}
                >
                  <option value="general">General</option>
                  <option value="market_analysis">Market Analysis</option>
                  <option value="monitoring">Monitoring</option>
                  <option value="content_generation">Content Generation</option>
                  <option value="data_processing">Data Processing</option>
                  <option value="nlp_analysis">NLP Analysis</option>
                </select>
              </div>
              <div style={{ display: 'flex', gap: '12px' }}>
                <button className="btn btn-primary" onClick={handleCreate}>
                  <Plus size={18} />
                  Create
                </button>
                <button className="btn btn-ghost" onClick={() => setShowCreate(false)}>
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          <table className="table">
            <thead>
              <tr>
                <th>Operation</th>
                <th>Type</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {operations.map(op => (
                <tr key={op.id}>
                  <td>
                    <div style={{ fontWeight: 500 }}>{op.name}</div>
                    {op.result && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                        {op.result}
                      </div>
                    )}
                    {op.progress && (
                      <div style={{ 
                        height: '4px', 
                        background: 'var(--bg-hover)', 
                        borderRadius: '2px', 
                        marginTop: '8px',
                        overflow: 'hidden'
                      }}>
                        <div style={{ 
                          height: '100%', 
                          width: `${op.progress}%`,
                          background: 'var(--accent-gold)',
                          borderRadius: '2px'
                        }} />
                      </div>
                    )}
                  </td>
                  <td>
                    <span style={{ fontSize: '1.2rem', marginRight: '8px' }}>
                      {getTypeIcon(op.type)}
                    </span>
                    {op.type.replace('_', ' ')}
                  </td>
                  <td>
                    <span className={`status-badge ${op.status}`}>
                      {op.status}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {new Date(op.created_at).toLocaleString()}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      {op.status === 'running' ? (
                        <button className="btn btn-ghost btn-sm">
                          <Pause size={16} />
                        </button>
                      ) : (
                        <button className="btn btn-ghost btn-sm">
                          <Play size={16} />
                        </button>
                      )}
                      <button className="btn btn-ghost btn-sm">
                        <RotateCcw size={16} />
                      </button>
                    </div>
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
