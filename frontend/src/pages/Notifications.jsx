import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api.js'

export default function Notifications() {
    const navigate = useNavigate()
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        api.get('/notifications/')
            .then((res) => setItems(res.data))
            .catch(() => setError('Could not load your notifications.'))
            .finally(() => setLoading(false))
    }, [])

    const openItem = async (item) => {
        if (!item.is_read) {
            try {
                await api.post(`/notifications/${item.id}/read/`)
                setItems((prev) => prev.map((n) => (n.id === item.id ? { ...n, is_read: true } : n)))
                window.dispatchEvent(new Event('notifications-changed'))
            } catch {
                setError('Could not update that notification.')
                return
            }
        }
        if (item.link) navigate(item.link)
    }

    const markAll = async () => {
        try {
            await api.post('/notifications/read-all/')
            setItems((prev) => prev.map((n) => ({ ...n, is_read: true })))
            window.dispatchEvent(new Event('notifications-changed'))
        } catch {
            setError('Could not update your notifications.')
        }
    }

    if (loading) return <div className="container py-5">Loading...</div>

    return (
        <div className="container py-4" style={{ maxWidth: 720 }}>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1 className="mb-0">Notifications</h1>
                <button className="btn btn-outline-secondary btn-sm" onClick={markAll}>
                    Mark all as read
                </button>
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            {!error && items.length === 0 && (
                <p className="text-muted">You have no notifications yet.</p>
            )}
            <ul className="list-group">
                {items.map((n) => (
                    <li
                        key={n.id}
                        className={`list-group-item ${n.is_read ? '' : 'list-group-item-primary fw-semibold'}`}
                        style={{ cursor: 'pointer' }}
                        onClick={() => openItem(n)}
                    >
                        {n.message}
                        <div className="small text-muted fw-normal">
                            {new Date(n.created_at).toLocaleString()}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    )
}