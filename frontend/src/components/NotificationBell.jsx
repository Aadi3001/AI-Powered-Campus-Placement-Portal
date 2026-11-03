import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api.js'

const POLL_MS = 30000 // ask the server every 30 seconds

export default function NotificationBell() {
    const navigate = useNavigate()
    const [count, setCount] = useState(0)
    const [items, setItems] = useState([])
    const [open, setOpen] = useState(false)

    const loadCount = useCallback(() => {
        api.get('/notifications/unread-count/')
            .then((res) => setCount(res.data.count))
            .catch(() => { })
    }, [])

    useEffect(() => {
        loadCount()
        const timer = setInterval(loadCount, POLL_MS)
        window.addEventListener('notifications-changed', loadCount)
        return () => {
            clearInterval(timer)
            window.removeEventListener('notifications-changed', loadCount)
        }
    }, [loadCount])

    const toggle = async () => {
        const next = !open
        setOpen(next)
        if (next) {
            try {
                const res = await api.get('/notifications/')
                setItems(res.data.slice(0, 8))
            } catch {
                // keep whatever we had; the bell must never break the page
            }
        }
    }

    const openItem = async (item) => {
        setOpen(false)
        if (!item.is_read) {
            await api.post(`/notifications/${item.id}/read/`).catch(() => { })
            loadCount()
        }
        if (item.link) navigate(item.link)
    }

    const markAll = async () => {
        await api.post('/notifications/read-all/').catch(() => { })
        setItems((prev) => prev.map((n) => ({ ...n, is_read: true })))
        setCount(0)
    }

    return (
        <div className="position-relative">
            <button
                className="btn btn-outline-light btn-sm position-relative"
                onClick={toggle}
                aria-label="Notifications"
            >
                🔔
                {count > 0 && (
                    <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                        {count}
                    </span>
                )}
            </button>

            {open && (
                <div
                    className="card shadow position-absolute end-0 mt-2"
                    style={{ width: 340, zIndex: 1000 }}
                >
                    <div className="card-header d-flex justify-content-between align-items-center">
                        <span>Notifications</span>
                        <button className="btn btn-link btn-sm p-0" onClick={markAll}>
                            Mark all as read
                        </button>
                    </div>
                    <ul className="list-group list-group-flush">
                        {items.length === 0 && (
                            <li className="list-group-item text-muted small">No notifications yet.</li>
                        )}
                        {items.map((n) => (
                            <li
                                key={n.id}
                                className={`list-group-item small ${n.is_read ? '' : 'fw-semibold'}`}
                                style={{ cursor: 'pointer' }}
                                onClick={() => openItem(n)}
                            >
                                {n.message}
                                <div className="text-muted fw-normal">
                                    {new Date(n.created_at).toLocaleString()}
                                </div>
                            </li>
                        ))}
                    </ul>
                    <div className="card-footer text-center">
                        <Link to="/notifications" onClick={() => setOpen(false)}>See all</Link>
                    </div>
                </div>
            )}
        </div>
    )
}