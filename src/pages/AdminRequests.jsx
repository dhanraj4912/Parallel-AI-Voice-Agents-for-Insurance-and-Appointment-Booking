import { useState, useEffect } from 'react'
import axios from 'axios'

export default function AdminRequests() {
  const [pending, setPending] = useState([])
  const [allUsers, setAllUsers] = useState([])
  const [tab, setTab] = useState('pending')
  const [msg, setMsg] = useState('')

  const load = async () => {
    const [p, a] = await Promise.all([
      axios.get('/api/auth/admin/pending-users'),
      axios.get('/api/auth/admin/all-users')
    ])
    setPending(p.data)
    setAllUsers(a.data)
  }

  useEffect(() => { load() }, [])

  const approve = async (id, name) => {
    await axios.post(`/api/auth/admin/approve/${id}`)
    setMsg(`✅ ${name} approved`)
    load()
    setTimeout(() => setMsg(''), 3000)
  }

  const reject = async (id, name) => {
    if (!confirm(`Reject ${name}?`)) return
    await axios.post(`/api/auth/admin/reject/${id}`)
    setMsg(`❌ ${name} rejected`)
    load()
    setTimeout(() => setMsg(''), 3000)
  }

  return (
    <div>
      <h1 className="page-title">Patient Requests</h1>
      <p className="page-subtitle">Approve or reject new patient registrations</p>

      {msg && <div style={{padding:'10px 16px',background:'#dcfce7',borderRadius:8,marginBottom:16,color:'#16a34a',fontWeight:500}}>{msg}</div>}

      <div style={{display:'flex',gap:8,marginBottom:20}}>
        <button onClick={() => setTab('pending')} className={`btn ${tab==='pending'?'btn-primary':'btn-outline'}`}>
          Pending ({pending.length})
        </button>
        <button onClick={() => setTab('all')} className={`btn ${tab==='all'?'btn-primary':'btn-outline'}`}>
          All Users ({allUsers.length})
        </button>
      </div>

      {tab === 'pending' && (
        <div className="table-wrapper">
          <table>
            <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Registered</th><th>Actions</th></tr></thead>
            <tbody>
              {pending.length === 0 && <tr><td colSpan="5"><div className="empty-state"><p>No pending requests.</p></div></td></tr>}
              {pending.map(u => (
                <tr key={u.id}>
                  <td style={{fontWeight:600}}>{u.full_name}</td>
                  <td>{u.email}</td>
                  <td>{u.phone}</td>
                  <td style={{color:'#6b7280',fontSize:'0.85rem'}}>{new Date(u.created_at).toLocaleDateString()}</td>
                  <td style={{display:'flex',gap:8}}>
                    <button className="btn btn-primary btn-sm" onClick={() => approve(u.id, u.full_name)}>✓ Approve</button>
                    <button className="btn btn-danger btn-sm" onClick={() => reject(u.id, u.full_name)}>✗ Reject</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'all' && (
        <div className="table-wrapper">
          <table>
            <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Status</th><th>Patient ID</th></tr></thead>
            <tbody>
              {allUsers.map(u => (
                <tr key={u.id}>
                  <td style={{fontWeight:600}}>{u.full_name}</td>
                  <td>{u.email}</td>
                  <td>{u.phone}</td>
                  <td><span className={`badge badge-${u.is_approved?'confirmed':'pending'}`}>{u.is_approved ? 'Approved' : 'Pending'}</span></td>
                  <td style={{color:'#6b7280',fontSize:'0.85rem'}}>{u.patient_id || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}