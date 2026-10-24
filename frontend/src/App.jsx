import { useState, useEffect } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const LOGO_AI = '/assets/nexora-ai-logo.png'
const LOGO_JARVIS = '/assets/nexora-jarvis-logo.png'

export default function App() {
  const [page, setPage] = useState('home')
  const [models, setModels] = useState([])
  const [health, setHealth] = useState('...')
  const [token, setToken] = useState(localStorage.getItem('nexora_token') || '')
  const [conversations, setConversations] = useState([])
  const [currentConv, setCurrentConv] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  useEffect(() => {
    fetch(API + '/health').then(r => r.json()).then(d => setHealth(d.status)).catch(() => setHealth('offline'))
    fetch(API + '/v1/models').then(r => r.json()).then(setModels).catch(() => {})
    if (token) loadConversations()
  }, [token])

  const loadConversations = async () => {
    const res = await fetch(API + '/v1/conversations', { headers: { Authorization: 'Bearer ' + token } })
    if (res.ok) setConversations(await res.json())
  }

  const openConv = async (id) => {
    setCurrentConv(id)
    const res = await fetch(API + `/v1/conversations/${id}/messages`, { headers: { Authorization: 'Bearer ' + token } })
    if (res.ok) setMessages(await res.json())
  }

  const sendMessage = async () => {
    if (!input.trim() || !currentConv) return
    await fetch(API + `/v1/conversations/${currentConv}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
      body: JSON.stringify({ content: input, role: 'user' })
    })
    setInput('')
    openConv(currentConv)
  }

  return (
    <div style={{ fontFamily: 'system-ui, -apple-system, sans-serif', background: '#050510', color: '#e8e8f0', minHeight: '100vh' }}>
      <nav style={{ padding: '1rem 1.5rem', borderBottom: '1px solid #1a1a2e', display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <img src={LOGO_AI} alt="Nexora AI" style={{ height: 36, marginRight: '0.5rem' }} onError={e => e.target.style.display='none'} />
        <strong style={{ fontSize: '1.1rem' }}>Nexora AI</strong>
        <button onClick={() => setPage('home')} style={navBtn}>Home</button>
        <button onClick={() => setPage('models')} style={navBtn}>Models</button>
        <button onClick={() => setPage('chat')} style={navBtn}>Chat</button>
        <button onClick={() => setPage('keys')} style={navBtn}>API Keys</button>
        <button onClick={() => setPage('jarvis')} style={{ ...navBtn, color: '#00d4ff' }}>JARVIS</button>
        <span style={{ marginLeft: 'auto', fontSize: '0.85rem', opacity: 0.7 }}>Status: {health}</span>
      </nav>

      <div style={{ padding: '1.5rem', maxWidth: 1100, margin: '0 auto' }}>
        {page === 'home' && <Home setPage={setPage} />}
        {page === 'models' && <Models models={models} />}
        {page === 'chat' && <Chat token={token} conversations={conversations} loadConversations={loadConversations} openConv={openConv} currentConv={currentConv} messages={messages} input={input} setInput={setInput} sendMessage={sendMessage} />}
        {page === 'keys' && <KeysPage token={token} setToken={setToken} />}
        {page === 'jarvis' && <JarvisPage />}
      </div>
    </div>
  )
}

const navBtn = { background: 'transparent', color: '#ccc', border: 'none', cursor: 'pointer', fontSize: '0.95rem' }

function Home({ setPage }) {
  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <img src={LOGO_AI} alt="Nexora AI Logo" style={{ height: 120, marginBottom: '1rem' }} />
        <h1 style={{ margin: '0.5rem 0', background: 'linear-gradient(90deg, #00d4ff, #7b68ee)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Nexora AI</h1>
        <p>Free AI platform with its own API and specialized models. All standard models are free under fair-use limits.</p>
      </div>

      <h2>Products</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
        <div style={card}>
          <h3>Nexora Models</h3>
          <p>Free conversational and specialized AI models. Chat, code, analyze, and more.</p>
          <span style={badgeFree}>Free</span>
          <button onClick={() => setPage('models')} style={btn}>View Models</button>
        </div>
        <div style={{ ...card, border: '1px solid #00d4ff55' }}>
          <img src={LOGO_JARVIS} alt="Nexora JARVIS" style={{ height: 80, marginBottom: '0.5rem' }} />
          <h3>Nexora JARVIS</h3>
          <p>Premium personal AI assistant. Your AI. Your Devices. Your Commands.</p>
          <span style={badgeSoon}>Coming Soon</span>
          <button onClick={() => setPage('jarvis')} style={{ ...btn, background: '#00d4ff22', borderColor: '#00d4ff' }}>Learn More</button>
        </div>
      </div>
    </div>
  )
}

function Models({ models }) {
  return (
    <div>
      <h2>Model Catalog</h2>
      <p>All standard Nexora models are free. Status reflects actual backend availability.</p>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {models.map(m => (
          <li key={m.id} style={{ padding: '0.6rem 0', borderBottom: '1px solid #222' }}>
            <strong>{m.id}</strong> — {m.status} {m.is_free && <span style={badgeFree}>free</span>}
          </li>
        ))}
      </ul>
    </div>
  )
}

function Chat({ token, conversations, loadConversations, openConv, currentConv, messages, input, setInput, sendMessage }) {
  if (!token) return <p>Please log in via the API Keys page to use chat history.</p>
  return (
    <div>
      <h2>Chat</h2>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ width: 260, minWidth: 200 }}>
          <button onClick={async () => {
            const res = await fetch(API + '/v1/conversations', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
              body: JSON.stringify({ title: 'New Chat', model_id: 'nexora-chat' })
            })
            if (res.ok) { loadConversations(); const d = await res.json(); openConv(d.id) }
          }} style={btn}>New Conversation</button>
          <ul style={{ listStyle: 'none', padding: 0, marginTop: '0.5rem' }}>
            {conversations.map(c => (
              <li key={c.id} onClick={() => openConv(c.id)} style={{ cursor: 'pointer', padding: '0.4rem', background: currentConv === c.id ? '#1a1a2e' : 'transparent' }}>{c.title}</li>
            ))}
          </ul>
        </div>
        <div style={{ flex: 1, minWidth: 280 }}>
          <div style={{ minHeight: 280, border: '1px solid #333', padding: '0.75rem', marginBottom: '0.5rem', borderRadius: 8 }}>
            {messages.map(m => <div key={m.id} style={{ margin: '0.4rem 0' }}><b>{m.role}:</b> {m.content}</div>)}
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()} style={{ flex: 1, padding: '0.5rem', background: '#111', color: '#eee', border: '1px solid #333', borderRadius: 6 }} placeholder="Message..." />
            <button onClick={sendMessage} style={btn}>Send</button>
          </div>
          <p style={{ fontSize: '0.85rem', opacity: 0.7 }}>AI replies require a configured free backend. Models currently report unavailable until set up.</p>
        </div>
      </div>
    </div>
  )
}

function KeysPage({ token, setToken }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [keys, setKeys] = useState([])

  const login = async () => {
    const form = new URLSearchParams({ username: email, password })
    const res = await fetch(API + '/v1/auth/login', { method: 'POST', body: form })
    if (res.ok) {
      const d = await res.json()
      setToken(d.access_token)
      localStorage.setItem('nexora_token', d.access_token)
    } else alert('Login failed. Register first via the API.')
  }

  const load = async () => {
    if (!token) return
    const res = await fetch(API + '/v1/api-keys', { headers: { Authorization: 'Bearer ' + token } })
    if (res.ok) setKeys(await res.json())
  }

  useEffect(() => { load() }, [token])

  return (
    <div>
      <h2>API Keys</h2>
      {!token ? (
        <div>
          <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} style={inputStyle} />
          <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} style={inputStyle} />
          <button onClick={login} style={btn}>Login</button>
          <p>Register via POST /v1/auth/register</p>
        </div>
      ) : (
        <div>
          <button onClick={async () => {
            const name = prompt('Key name') || 'My Key'
            const res = await fetch(API + '/v1/api-keys', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
              body: JSON.stringify({ name })
            })
            if (res.ok) {
              const d = await res.json()
              alert('Save this key now (shown once): ' + d.raw_key)
              load()
            }
          }} style={btn}>Create API Key</button>
          <ul>{keys.map(k => <li key={k.id}>{k.name} ({k.key_prefix}...)</li>)}</ul>
        </div>
      )}
    </div>
  )
}

function JarvisPage() {
  const [email, setEmail] = useState('')
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)

  const notify = async () => {
    if (!email) return
    setLoading(true)
    setMsg('')
    try {
      const res = await fetch(API + '/v1/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, product: 'nexora-jarvis' })
      })
      const data = await res.json()
      if (res.ok) {
        setMsg(data.message || 'Added to waitlist.')
        setEmail('')
      } else {
        setMsg(data.detail || 'Unable to join waitlist.')
      }
    } catch {
      setMsg('Network error. Waitlist endpoint unavailable.')
    }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <img src={LOGO_JARVIS} alt="Nexora JARVIS Logo" style={{ height: 140, marginBottom: '1rem', filter: 'drop-shadow(0 0 20px #00d4ff66)' }} />
        <h1 style={{ margin: '0.3rem 0', fontSize: '2.2rem' }}>NEXORA JARVIS</h1>
        <p style={{ fontSize: '1.2rem', color: '#00d4ff' }}>Your AI. Your Devices. Your Commands.</p>
        <span style={badgeSoon}>Premium Product — Coming Soon</span>
      </div>

      <p style={{ maxWidth: 700, margin: '0 auto 1.5rem', lineHeight: 1.6 }}>
        Meet the next generation of personal AI assistance. A smarter assistant designed to help you interact with your devices, automate tasks, and control supported workflows through natural conversation.
      </p>

      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <input
          type="email"
          placeholder="Your email for launch notification"
          value={email}
          onChange={e => setEmail(e.target.value)}
          style={{ ...inputStyle, width: 280, marginRight: '0.5rem' }}
        />
        <button onClick={notify} disabled={loading} style={btn}>
          {loading ? 'Submitting...' : 'Notify Me at Launch'}
        </button>
        {msg && <p style={{ marginTop: '0.75rem', color: msg.includes('added') || msg.includes('Added') ? '#00ffaa' : '#ffaa00' }}>{msg}</p>}
      </div>

      <h2>Planned Features</h2>
      <p style={{ opacity: 0.8, fontSize: '0.9rem' }}>These capabilities are planned and not yet implemented or tested.</p>
      <ul style={{ lineHeight: 1.7 }}>
        <li><strong>Natural voice conversations</strong> — Talk to JARVIS without needing to click a talk button every time, where supported and permission is granted.</li>
        <li><strong>Wake-word activation</strong> — Optional “JARVIS” activation with an explicit user-controlled microphone permission and visible listening indicator.</li>
        <li><strong>Cross-device assistant</strong> — A shared assistant experience across supported PCs, phones, and other connected devices.</li>
        <li><strong>Device integrations</strong> — Control supported devices through authorized APIs and integrations.</li>
        <li><strong>Smart automation</strong> — Run user-approved workflows and routines.</li>
        <li><strong>AI conversations</strong> — Remember relevant context according to user-controlled memory and privacy settings.</li>
        <li><strong>Developer integrations</strong> — Documented APIs or integrations if implemented.</li>
        <li><strong>Voice responses</strong> — Speak naturally and provide configurable voice settings.</li>
        <li><strong>Permission controls</strong> — Users decide what JARVIS can access and which actions it may perform.</li>
        <li><strong>Security and privacy</strong> — Secure authentication, protected credentials, clear microphone controls, and revocable device access.</li>
      </ul>
      <p style={{ fontSize: '0.85rem', opacity: 0.7, marginTop: '1rem' }}>
        JARVIS cannot turn on a completely powered-off phone, access locked devices, or control every device universally. Actual capabilities will depend on platform permissions, hardware support, and user authorization.
      </p>
      <p style={{ marginTop: '1.5rem', fontSize: '0.9rem' }}>
        Existing Nexora AI models remain free. JARVIS is a planned paid product. No checkout or payment is active.
      </p>
    </div>
  )
}

const card = { background: '#0f0f1a', border: '1px solid #222', borderRadius: 12, padding: '1.25rem', textAlign: 'center' }
const btn = { background: '#1a1a2e', color: '#eee', border: '1px solid #444', padding: '0.5rem 1rem', borderRadius: 6, cursor: 'pointer', marginTop: '0.5rem' }
const badgeFree = { display: 'inline-block', background: '#00ffaa22', color: '#00ffaa', padding: '0.15rem 0.5rem', borderRadius: 4, fontSize: '0.75rem', marginLeft: '0.4rem' }
const badgeSoon = { display: 'inline-block', background: '#00d4ff22', color: '#00d4ff', padding: '0.2rem 0.6rem', borderRadius: 4, fontSize: '0.8rem', fontWeight: 600 }
const inputStyle = { padding: '0.5rem', background: '#111', color: '#eee', border: '1px solid #333', borderRadius: 6, margin: '0.3rem 0' }