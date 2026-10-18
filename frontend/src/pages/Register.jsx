import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api.js'
import { useAuth } from '../AuthContext.jsx'
import { errorText } from '../errors.js'

const FIELDS = [
    ['username', 'Username', 'text'],
    ['email', 'Email', 'email'],
    ['password', 'Password (at least 8 characters)', 'password'],
    ['confirm', 'Confirm password', 'password'],
]

export default function Register() {
    const { login } = useAuth()
    const navigate = useNavigate()
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: '',
        confirm: '',
        role: 'STUDENT',
    })
    const [error, setError] = useState('')
    const [submitting, setSubmitting] = useState(false)

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        if (form.password !== form.confirm) {
            setError('The two passwords do not match.')
            return
        }
        setSubmitting(true)
        try {
            await api.post('/register/', {
                username: form.username,
                email: form.email,
                password: form.password,
                role: form.role,
            })
            // Log the new user straight in
            const me = await login(form.username, form.password)
            navigate(me.role === 'STUDENT' ? '/student/profile' : '/recruiter/profile')
        } catch (err) {
            setError(errorText(err, 'Could not create your account. Is the backend running?'))
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="container py-5" style={{ maxWidth: 420 }}>
            <h1 className="mb-4">Create an account</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label" htmlFor="role">I am a</label>
                    <select
                        id="role"
                        name="role"
                        className="form-select"
                        value={form.role}
                        onChange={handleChange}
                    >
                        <option value="STUDENT">Student</option>
                        <option value="RECRUITER">Recruiter</option>
                    </select>
                </div>
                {FIELDS.map(([name, label, type]) => (
                    <div className="mb-3" key={name}>
                        <label className="form-label" htmlFor={name}>{label}</label>
                        <input
                            id={name}
                            name={name}
                            type={type}
                            className="form-control"
                            value={form[name]}
                            onChange={handleChange}
                            required
                        />
                    </div>
                ))}
                <button className="btn btn-primary w-100" disabled={submitting}>
                    {submitting ? 'Creating account...' : 'Register'}
                </button>
            </form>
            <p className="mt-3 text-center small">
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    )
}