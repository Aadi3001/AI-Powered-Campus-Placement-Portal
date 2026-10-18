import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../../api.js'
import { errorText } from '../../errors.js'
import { BRANCHES } from '../../constants.js'

// Adds the value to the list if it's missing, removes it if it's there
const toggle = (list, setList, value) =>
    setList(list.includes(value) ? list.filter((v) => v !== value) : [...list, value])

const TEXT_FIELDS = [
    { name: 'title', label: 'Job title', type: 'text', required: true },
    { name: 'location', label: 'Location', type: 'text' },
    { name: 'salary_range', label: 'Salary range (for example 6-8 LPA)', type: 'text' },
    { name: 'min_cgpa', label: 'Minimum CGPA', type: 'number', step: '0.01', max: '10' },
    { name: 'min_graduation_year', label: 'Earliest graduation year', type: 'number' },
    { name: 'max_graduation_year', label: 'Latest graduation year', type: 'number' },
]

export default function NewJob() {
    const navigate = useNavigate()
    const [skills, setSkills] = useState([])
    const [form, setForm] = useState({
        title: '',
        description: '',
        location: '',
        salary_range: '',
        min_cgpa: '',
        min_graduation_year: '',
        max_graduation_year: '',
    })
    const [selectedSkills, setSelectedSkills] = useState([])
    const [selectedBranches, setSelectedBranches] = useState([])
    const [busy, setBusy] = useState(false)
    const [error, setError] = useState('')

    useEffect(() => {
        api.get('/recruiter/skills/')
            .then((res) => setSkills(res.data))
            .catch(() => setError('Could not load the skill list.'))
    }, [])

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setBusy(true)
        try {
            await api.post('/recruiter/jobs/', {
                title: form.title,
                description: form.description,
                location: form.location,
                salary_range: form.salary_range,
                required_skills: selectedSkills,
                min_cgpa: form.min_cgpa || null,
                min_graduation_year: form.min_graduation_year || null,
                max_graduation_year: form.max_graduation_year || null,
                eligible_branches: selectedBranches.join(', '),
            })
            navigate('/recruiter/jobs')
        } catch (err) {
            setError(errorText(err, 'Could not post the job.'))
        } finally {
            setBusy(false)
        }
    }

    return (
        <div className="container py-4" style={{ maxWidth: 720 }}>
            <Link to="/recruiter/jobs" className="small">← Back to my jobs</Link>
            <h1 className="mt-2 mb-4">Post a new job</h1>
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit} className="card card-body">
                {TEXT_FIELDS.slice(0, 1).map((f) => (
                    <div className="mb-3" key={f.name}>
                        <label className="form-label" htmlFor={f.name}>{f.label}</label>
                        <input
                            id={f.name}
                            name={f.name}
                            type={f.type}
                            className="form-control"
                            value={form[f.name]}
                            onChange={handleChange}
                            required={f.required}
                        />
                    </div>
                ))}

                <div className="mb-3">
                    <label className="form-label" htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        name="description"
                        rows="4"
                        className="form-control"
                        value={form.description}
                        onChange={handleChange}
                        required
                    />
                    <div className="form-text">
                        Mention the skills in plain words, for example "experience with Python
                        and Django". If you don't tick any skills below, we detect them from
                        this text.
                    </div>
                </div>

                <div className="mb-3">
                    <div className="form-label">Required skills (optional)</div>
                    {skills.map((s) => (
                        <div className="form-check form-check-inline" key={s.id}>
                            <input
                                className="form-check-input"
                                type="checkbox"
                                id={`skill-${s.id}`}
                                checked={selectedSkills.includes(s.id)}
                                onChange={() => toggle(selectedSkills, setSelectedSkills, s.id)}
                            />
                            <label className="form-check-label" htmlFor={`skill-${s.id}`}>
                                {s.name}
                            </label>
                        </div>
                    ))}
                </div>

                <div className="mb-3">
                    <div className="form-label">Eligible branches (leave empty for all)</div>
                    {BRANCHES.map(([code, label]) => (
                        <div className="form-check form-check-inline" key={code}>
                            <input
                                className="form-check-input"
                                type="checkbox"
                                id={`branch-${code}`}
                                checked={selectedBranches.includes(code)}
                                onChange={() => toggle(selectedBranches, setSelectedBranches, code)}
                            />
                            <label className="form-check-label" htmlFor={`branch-${code}`}>
                                {label}
                            </label>
                        </div>
                    ))}
                </div>

                <div className="row">
                    {TEXT_FIELDS.slice(1).map((f) => (
                        <div className="col-md-6 mb-3" key={f.name}>
                            <label className="form-label" htmlFor={f.name}>{f.label}</label>
                            <input
                                id={f.name}
                                name={f.name}
                                type={f.type}
                                step={f.step}
                                max={f.max}
                                className="form-control"
                                value={form[f.name]}
                                onChange={handleChange}
                            />
                        </div>
                    ))}
                </div>

                <button className="btn btn-primary" disabled={busy}>
                    {busy ? 'Posting...' : 'Post job'}
                </button>
            </form>
        </div>
    )
}