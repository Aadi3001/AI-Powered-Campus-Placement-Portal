import { useEffect, useState } from 'react'
import api from '../../api.js'

const STATUS_STYLES = {
    APPLIED: 'secondary',
    SHORTLISTED: 'info',
    REJECTED: 'danger',
    SELECTED: 'success',
}

export default function Applications() {
    const [applications, setApplications] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        api.get('/applications/my/')
            .then((res) => setApplications(res.data))
            .catch(() => setError('Could not load your applications.'))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="container py-5">Loading...</div>

    return (
        <div className="container py-4">
            <h1 className="mb-4">My applications</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            {!error && applications.length === 0 && (
                <p className="text-muted">You have not applied to any jobs yet.</p>
            )}
            {applications.length > 0 && (
                <table className="table">
                    <thead>
                        <tr>
                            <th>Job</th>
                            <th>Status</th>
                            <th>Applied on</th>
                        </tr>
                    </thead>
                    <tbody>
                        {applications.map((app) => (
                            <tr key={app.id}>
                                <td>{app.job_title}</td>
                                <td>
                                    <span className={`badge text-bg-${STATUS_STYLES[app.status]}`}>
                                        {app.status}
                                    </span>
                                </td>
                                <td>{new Date(app.applied_at).toLocaleDateString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    )
}