import { useState, useRef, useEffect } from 'react'

const API_URL = '/api/v1/run/59b62845-782c-46e8-ad50-9384ec1ac075?stream=false'
const API_KEY = 'sk-k2K0pWRUxcOyKC39Kb9_HdpMB0-vOv-Ej-ZHnoyMQbg'

function App() {
  const [issueKey, setIssueKey] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sessionId] = useState(() => 'session_' + Date.now())
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function runTriage() {
    if (!issueKey.trim()) return
    const key = issueKey.trim().toUpperCase()
    setMessages(prev => [...prev, { role: 'user', text: `🔍 Triaging: ${key}` }])
    setLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-api-key': API_KEY },
        body: JSON.stringify({
          output_type: 'chat',
          input_type: 'text',
          issue_key: key,
          session_id: sessionId
        })
      })
      const data = await res.json()
      const text = data?.outputs?.[0]?.outputs?.[0]?.results?.message?.data?.text || 'No response'
      setMessages(prev => [...prev, { role: 'ai', text }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: '❌ Error: ' + err.message }])
    }
    setLoading(false)
    setIssueKey('')
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') runTriage()
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🐛 Bug Triage AI</h1>
        <p>Enter a Jira issue key (e.g. KAN-112) to analyze it</p>
      </header>

      <div className="chat">
        {messages.length === 0 && (
          <div className="empty">
            <div className="empty-icon">🤖</div>
            <p>Enter a Jira Issue Key above and click <strong>Run Triage</strong></p>
            <p className="hint">The AI will fetch the issue and return severity, priority & analysis</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg msg-${m.role}`}>
            <div className="msg-label">{m.role === 'user' ? '🔍 You' : '🤖 AI Triage'}</div>
            <div className="msg-text">{m.text}</div>
          </div>
        ))}
        {loading && <div className="loading">⏳ Analyzing...</div>}
        <div ref={bottomRef} />
      </div>

      <div className="input-bar">
        <input
          value={issueKey}
          onChange={e => setIssueKey(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. KAN-112"
          disabled={loading}
        />
        <button onClick={runTriage} disabled={loading || !issueKey.trim()}>
          {loading ? '⏳' : '🚀 Run Triage'}
        </button>
      </div>
    </div>
  )
}

export default App