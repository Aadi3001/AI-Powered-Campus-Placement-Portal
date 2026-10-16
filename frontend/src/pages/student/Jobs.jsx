import { useEffect, useState } from 'react'
import api from '../../api.js'
import JobInsights from '../../components/JobInsights.jsx'

export default function Jobs() {
    const [jobs, setJobs] = useState([])
    const [appliedIds, setAppliedIds] = useState(new Set())
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [message, setMessage] = useState('')
    const [openId, setOpenId] = useState(null)

    useEffect(() => {
        // Both requests run at the same time; we continue when both are done
        Promise.all([api.get('/recruiter/jobs/'), api.get('/applications/my/')])
            .then(([jobsRes, appsRes]) => {
                setJobs(jobsRes.data.filter((job) => job.is_active))
                setAppliedIds(new Set(appsRes.data.map((app) => app.job)))
            })
            .catch(() => setError('Could not load jobs.'))
            .finally(() => setLoading(false))
    }, [])

    const apply = async (jobId) => {
        setMessage('')
        setError('')
        try {
            await api.post('/applications/my/', { job: jobId })
            // React state must be replaced, not changed in place, so we copy the Set
            setAppliedIds((prev) => new Set(prev).add(jobId))
            setMessage('Application submitted.')
        } catch (err) {
            const detail = err.response?.data
            setError(Array.isArray(detail) ? detail[0] : 'Could not submit the application.')
        }
    }

    if (loading) return <div className="container py-5">Loading jobs...</div>

    return (
        <div className="container py-4">
            <h1 className="mb-4">Open jobs</h1>
            {message && <div className="alert alert-success">{message}</div>}
            {error && <div className="alert alert-danger">{error}</div>}
            {!error && jobs.length === 0 && (
                <p className="text-muted">No open jobs right now.</p>
            )}
            <div className="row g-3">
                {jobs.map((job) => (
                    <div className="col-md-6" key={job.id}>
                        <div className="card h-100">
                            <div className="card-body">
                                <h5 className="card-title">{job.title}</h5>
                                <p className="card-text text-muted">{job.description}</p>
                                <div className="mb-2">
                                    {job.required_skill_names.map((name) => (
                                        <span key={name} className="badge text-bg-secondary me-1">
                                            {name}
                                        </span>
                                    ))}
                                </div>
                                <ul className="list-unstyled small mb-0">
                                    {job.location && <li>Location: {job.location}</li>}
                                    {job.salary_range && <li>Salary: {job.salary_range}</li>}
                                    {job.min_cgpa && <li>Minimum CGPA: {job.min_cgpa}</li>}
                                    {job.eligible_branches && <li>Branches: {job.eligible_branches}</li>}
                                </ul>
                                {openId === job.id && <JobInsights jobId={job.id} />}
                            </div>
                            <div className="card-footer bg-transparent d-flex gap-2 align-items-center">
                                {appliedIds.has(job.id) ? (
                                    <span className="badge text-bg-success">Applied</span>
                                ) : (
                                    <button className="btn btn-primary btn-sm" onClick={() => apply(job.id)}>
                                        Apply
                                    </button>
                                )}
                                <button
                                    className="btn btn-outline-secondary btn-sm"
                                    onClick={() => setOpenId(openId === job.id ? null : job.id)}
                                >
                                    {openId === job.id ? 'Hide my match' : 'Show my match'}
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}