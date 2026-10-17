import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'

export default function Login() {
    const { login } = useAuth()
    const navigate = useNavigate()
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [submitting, setSubmitting] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setSubmitting(true)
        try {
            const me = await login(username, password)
            if (me.role === 'STUDENT') navigate('/student/jobs')
            else if (me.role === 'RECRUITER') navigate('/recruiter/jobs')
            else navigate('/')
        } catch (err) {
            if (err.response?.status === 401) {
                setError('Incorrect username or password.')
            } else {
                setError('Could not reach the server. Is the backend running?')
            }
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="container py-5" style={{ maxWidth: 420 }}>
            <h1 className="mb-4">Login</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label" htmlFor="username">Username</label>
                    <input
                        id="username"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label" htmlFor="password">Password</label>
                    <input
                        id="password"
                        type="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button className="btn btn-primary w-100" disabled={submitting}>
                    {submitting ? 'Logging in...' : 'Login'}
                </button>
            </form>
            <p className="mt-3 text-center small">
                No account yet? <Link to="/register">Register</Link>
            </p>
        </div>
    )
}