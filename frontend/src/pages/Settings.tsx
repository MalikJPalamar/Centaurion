import { useState } from 'react'
import { Save, Key, Bell, Palette } from 'lucide-react'

interface SettingsData {
  api_keys: {
    openai: string
    anthropic: string
    market_data: string
  }
  notifications: {
    email: boolean
    slack: boolean
    discord: boolean
  }
  preferences: {
    theme: string
    auto_refresh: boolean
    refresh_interval: number
  }
}

const defaultSettings: SettingsData = {
  api_keys: {
    openai: '',
    anthropic: '',
    market_data: ''
  },
  notifications: {
    email: true,
    slack: false,
    discord: false
  },
  preferences: {
    theme: 'dark',
    auto_refresh: true,
    refresh_interval: 30
  }
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsData>(() => {
    const saved = localStorage.getItem('centaurion-settings')
    return saved ? JSON.parse(saved) : defaultSettings
  })
  const [saved, setSaved] = useState(false)
  
  const handleSave = () => {
    localStorage.setItem('centaurion-settings', JSON.stringify(settings))
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }
  
  const updateApiKey = (key: string, value: string) => {
    setSettings(prev => ({
      ...prev,
      api_keys: { ...prev.api_keys, [key]: value }
    }))
  }
  
  const toggleNotification = (key: keyof typeof settings.notifications) => {
    setSettings(prev => ({
      ...prev,
      notifications: { ...prev.notifications, [key]: !prev.notifications[key] }
    }))
  }
  
  const updatePreference = (key: keyof typeof settings.preferences, value: any) => {
    setSettings(prev => ({
      ...prev,
      preferences: { ...prev.preferences, [key]: value }
    }))
  }
  
  return (
    <>
      <div className="section-header">
        <h2 className="section-title">Settings</h2>
        <button className="btn btn-primary" onClick={handleSave}>
          <Save size={18} />
          {saved ? 'Saved!' : 'Save Changes'}
        </button>
      </div>
      
      <div style={{ display: 'grid', gap: '24px', maxWidth: '800px' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Key className="card-title-icon" size={20} />
              API Keys
            </h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">OpenAI API Key</label>
                <input 
                  type="password" 
                  className="form-input"
                  placeholder="sk-..."
                  value={settings.api_keys.openai}
                  onChange={(e) => updateApiKey('openai', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Anthropic API Key</label>
                <input 
                  type="password" 
                  className="form-input"
                  placeholder="sk-ant-..."
                  value={settings.api_keys.anthropic}
                  onChange={(e) => updateApiKey('anthropic', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Market Data API Key</label>
                <input 
                  type="password" 
                  className="form-input"
                  placeholder="Enter API key..."
                  value={settings.api_keys.market_data}
                  onChange={(e) => updateApiKey('market_data', e.target.value)}
                />
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Bell className="card-title-icon" size={20} />
              Notifications
            </h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>Email Notifications</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Receive updates via email
                  </div>
                </div>
                <div 
                  className={`toggle ${settings.notifications.email ? 'active' : ''}`}
                  onClick={() => toggleNotification('email')}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>Slack Notifications</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Send alerts to Slack channel
                  </div>
                </div>
                <div 
                  className={`toggle ${settings.notifications.slack ? 'active' : ''}`}
                  onClick={() => toggleNotification('slack')}
                />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>Discord Notifications</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Send alerts to Discord webhook
                  </div>
                </div>
                <div 
                  className={`toggle ${settings.notifications.discord ? 'active' : ''}`}
                  onClick={() => toggleNotification('discord')}
                />
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Palette className="card-title-icon" size={20} />
              Preferences
            </h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Theme</label>
                <select 
                  className="form-input"
                  value={settings.preferences.theme}
                  onChange={(e) => updatePreference('theme', e.target.value)}
                >
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="system">System</option>
                </select>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ fontWeight: 500 }}>Auto Refresh</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Automatically refresh dashboard data
                  </div>
                </div>
                <div 
                  className={`toggle ${settings.preferences.auto_refresh ? 'active' : ''}`}
                  onClick={() => updatePreference('auto_refresh', !settings.preferences.auto_refresh)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Refresh Interval (seconds)</label>
                <input 
                  type="number" 
                  className="form-input"
                  min={10}
                  max={300}
                  value={settings.preferences.refresh_interval}
                  onChange={(e) => updatePreference('refresh_interval', parseInt(e.target.value))}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
