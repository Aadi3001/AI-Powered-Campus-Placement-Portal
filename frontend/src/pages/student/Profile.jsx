import { useEffect, useState } from 'react'
import api from '../../api.js'

// Must match BRANCH_CHOICES in backend/students/models.py
const BRANCHES = [
    ['CSE', 'Computer Engineering'],
    ['IT', 'Information Technology'],
    ['AIDS', 'AI & Data Science Engineering'],
    ['AIML', 'AI/ML Engineering'],
    ['ENTC', 'Electronics and Telecommunication'],
    ['MECH', 'Mechanical Engineering'],
    ['CIVIL', 'Civil Engineering'],
    ['ELECTRICAL', 'Electrical Engineering'],
]

const TEXT_FIELDS = [
    { name: 'full_name', label: 'Full name', type: 'text' },
    { name: 'phone_number', label: 'Phone number', type: 'text' },
    { name: 'degree', label: 'Degree (for example B.E.)', type: 'text' },
    { name: 'graduation_year', label: 'Graduation year', type: 'number' },
    { name: 'cgpa', label: 'CGPA', type: 'number', step: '0.01' },
]

// Turns the API's validation errors into one readable sentence
function errorText(err, fallback) {
    const data = err.response?.data
    if (data && typeof data === 'object') {
        return Object.values(data).flat().join(' ')
    }
    return fallback
}

export default function Profile() {
    const [profile, setProfile] = useState(null)
    const [skills, setSkills] = useState([])
    const [form, setForm] = useState(null)
    const [file, setFile] = useState(null)
    const [fileKey, setFileKey] = useState(0)
    const [loading, setLoading] = useState(true)
    const [busy, setBusy] = useState(false)
    const [error, setError] = useState('')
    const [message, setMessage] = useState('')

    useEffect(() => {
        Promise.all([api.get('/student/profile/'), api.get('/student/skills/')])
            .then(([profileRes, skillsRes]) => {
                const p = profileRes.data
                setProfile(p)
                setSkills(skillsRes.data)
                setForm({
                    full_name: p.full_name ?? '',
                    phone_number: p.phone_number ?? '',
                    degree: p.degree ?? '',
                    branch: p.branch ?? '',
                    graduation_year: p.graduation_year ?? '',
                    cgpa: p.cgpa ?? '',
                })
            })
            .catch(() => setError('Could not load your profile.'))
            .finally(() => setLoading(false))
    }, [])

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const saveProfile = async (e) => {
        e.preventDefault()
        setError('')
        setMessage('')
        setBusy(true)
        try {
            const res = await api.patch('/student/profile/', {
                ...form,
                graduation_year: form.graduation_year || null,
                cgpa: form.cgpa || null,
            })
            setProfile(res.data)
            setMessage('Profile saved.')
        } catch (err) {
            setError(errorText(err, 'Could not save your profile.'))
        } finally {
            setBusy(false)
        }
    }

    const uploadResume = async (e) => {
        e.preventDefault()
        if (!file) return
        setError('')
        setMessage('')
        setBusy(true)
        try {
            const data = new FormData()
            data.append('resume', file)
            const res = await api.patch('/student/profile/', data)
            setProfile(res.data)
            const skillsRes = await api.get('/student/skills/')
            setSkills(skillsRes.data)
            setMessage('Resume uploaded. Your skills list has been updated.')
            setFile(null)
            setFileKey((k) => k + 1) // resets the file picker
        } catch (err) {
            setError(errorText(err, 'Could not upload your resume.'))
        } finally {
            setBusy(false)
        }
    }

    if (loading) return <div className="container py-5">Loading...</div>
    if (!profile) {
        return (
            <div className="container py-5">
                <div className="alert alert-danger">{error}</div>
            </div>
        )
    }

    return (
        <div className="container py-4">
            <h1 className="mb-4">My profile</h1>
            {message && <div className="alert alert-success">{message}</div>}
            {error && <div className="alert alert-danger">{error}</div>}

            <div className="row g-4">
                <div className="col-lg-6">
                    <form onSubmit={saveProfile} className="card card-body">
                        <h5 className="mb-3">Details</h5>
                        {TEXT_FIELDS.map((f) => (
                            <div className="mb-3" key={f.name}>
                                <label className="form-label" htmlFor={f.name}>{f.label}</label>
                                <input
                                    id={f.name}
                                    name={f.name}
                                    type={f.type}
                                    step={f.step}
                                    className="form-control"
                                    value={form[f.name]}
                                    onChange={handleChange}
                                />
                            </div>
                        ))}
                        <div className="mb-3">
                            <label className="form-label" htmlFor="branch">Branch</label>
                            <select
                                id="branch"
                                name="branch"
                                className="form-select"
                                value={form.branch}
                                onChange={handleChange}
                            >
                                <option value="">Select a branch</option>
                                {BRANCHES.map(([code, label]) => (
                                    <option key={code} value={code}>{label}</option>
                                ))}
                            </select>
                        </div>
                        <button className="btn btn-primary" disabled={busy}>Save profile</button>
                    </form>
                </div>

                <div className="col-lg-6">
                    <form onSubmit={uploadResume} className="card card-body mb-4">
                        <h5 className="mb-3">Resume</h5>
                        {profile.resume ? (
                            <a href={profile.resume} target="_blank" rel="noreferrer">
                                View current resume
                            </a>
                        ) : (
                            <p className="text-muted mb-0">No resume uploaded yet.</p>
                        )}
                        <input
                            key={fileKey}
                            type="file"
                            accept="application/pdf"
                            className="form-control my-3"
                            onChange={(e) => setFile(e.target.files[0] ?? null)}
                        />
                        <button className="btn btn-primary" disabled={busy || !file}>
                            Upload resume
                        </button>
                        {profile.resume_text && (
                            <details className="mt-3">
                                <summary>Text we read from your resume</summary>
                                <pre className="small mt-2" style={{ whiteSpace: 'pre-wrap' }}>
                                    {profile.resume_text}
                                </pre>
                            </details>
                        )}
                    </form>

                    <div className="card card-body">
                        <h5 className="mb-3">My skills</h5>
                        {skills.length === 0 ? (
                            <p className="text-muted mb-0">
                                No skills yet. Upload a resume and the skills we recognise will be added.
                            </p>
                        ) : (
                            <div>
                                {skills.map((s) => (
                                    <span key={s.id} className="badge text-bg-secondary me-1 mb-1">
                                        {s.name} · {s.proficiency.toLowerCase()}
                                    </span>
                                ))}
                            </div>
                        )}
                        <p className="text-muted small mt-3 mb-0">
                            We can only recognise skills that are in the portal's skill list.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}