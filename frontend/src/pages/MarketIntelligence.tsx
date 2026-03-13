import { TrendingUp, TrendingDown, Users, FileText, Download } from 'lucide-react'

const marketData = {
  sectors: [
    { name: 'Technology', sentiment: 'bullish', change: 2.4 },
    { name: 'Healthcare', sentiment: 'neutral', change: 0.8 },
    { name: 'Finance', sentiment: 'bullish', change: 1.2 },
    { name: 'Energy', sentiment: 'bearish', change: -1.5 }
  ],
  trends: [
    { topic: 'AI Automation', volume: 15420, sentiment: 0.78 },
    { topic: 'Cloud Computing', volume: 12300, sentiment: 0.65 },
    { topic: 'Cybersecurity', volume: 9800, sentiment: 0.82 }
  ],
  competitors: [
    { name: 'TechCorp Inc', mention_volume: 450, sentiment: 0.62 },
    { name: 'DataSystems', mention_volume: 320, sentiment: 0.71 },
    { name: 'CloudNine', mention_volume: 280, sentiment: 0.55 }
  ]
}

export default function MarketIntelligence() {
  return (
    <>
      <div className="section-header">
        <h2 className="section-title">Market Intelligence</h2>
        <button className="btn btn-secondary">
          <FileText size={18} />
          Generate Report
        </button>
      </div>
      
      <div className="dashboard-grid">
        {marketData.sectors.map((sector, index) => (
          <div key={index} className="stat-card">
            <div className="stat-value" style={{ color: sector.change >= 0 ? 'var(--accent-emerald)' : 'var(--accent-crimson)' }}>
              {sector.change >= 0 ? '+' : ''}{sector.change}%
            </div>
            <div className="stat-label">{sector.name}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '12px', fontSize: '0.8rem' }}>
              {sector.change >= 0 ? (
                <TrendingUp size={14} color="var(--accent-emerald)" />
              ) : (
                <TrendingDown size={14} color="var(--accent-crimson)" />
              )}
              <span style={{ color: sector.change >= 0 ? 'var(--accent-emerald)' : 'var(--accent-crimson)' }}>
                {sector.sentiment}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="two-col-grid">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <TrendingUp className="card-title-icon" size={20} />
              Trending Topics
            </h3>
          </div>
          <div className="card-body">
            <div className="activity-list">
              {marketData.trends.map((trend, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-content">
                    <div className="activity-title">{trend.topic}</div>
                    <div className="activity-time">
                      {trend.volume.toLocaleString()} mentions • Sentiment: {Math.round(trend.sentiment * 100)}%
                    </div>
                  </div>
                  <div style={{ 
                    width: '60px', 
                    height: '60px', 
                    borderRadius: '50%', 
                    background: `conic-gradient(var(--accent-gold) ${trend.sentiment * 360}deg, var(--bg-tertiary) 0deg)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.8rem',
                    fontWeight: 600
                  }}>
                    {Math.round(trend.sentiment * 100)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Users className="card-title-icon" size={20} />
              Competitor Mentions
            </h3>
          </div>
          <div className="card-body">
            <div className="activity-list">
              {marketData.competitors.map((competitor, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-content">
                    <div className="activity-title">{competitor.name}</div>
                    <div className="activity-time">
                      {competitor.mention_volume} mentions this week
                    </div>
                  </div>
                  <div style={{ 
                    padding: '4px 12px', 
                    borderRadius: '20px',
                    background: competitor.sentiment >= 0.6 ? 'rgba(26, 95, 74, 0.2)' : 'rgba(201, 162, 39, 0.2)',
                    color: competitor.sentiment >= 0.6 ? '#4ade80' : 'var(--accent-gold)',
                    fontSize: '0.8rem',
                    fontWeight: 500
                  }}>
                    {competitor.sentiment >= 0.6 ? 'Positive' : 'Neutral'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
