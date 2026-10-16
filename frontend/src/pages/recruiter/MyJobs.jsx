import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../api.js'

export default function MyJobs() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        api.get('/recruiter/my-jobs/')
            .then((res) => setJobs(res.data))
            .catch(() => setError('Could not load your jobs.'))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="container py-5">Loading...</div>

    return (
        <div className="container py-4">
            <h1 className="mb-4">My jobs</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            {!error && jobs.length === 0 && (
                <p className="text-muted">You have not posted any jobs yet.</p>
            )}
            {jobs.length > 0 && (
                <table className="table align-middle">
                    <thead>
                        <tr>
                            <th>Job</th>
                            <th>Required skills</th>
                            <th>Applicants</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.map((job) => (
                            <tr key={job.id}>
                                <td>
                                    {job.title}
                                    <div className="text-muted small">{job.location}</div>
                                </td>
                                <td>
                                    {job.required_skill_names.map((name) => (
                                        <span key={name} className="badge text-bg-secondary me-1">
                                            {name}
                                        </span>
                                    ))}
                                </td>
                                <td>{job.applicant_count}</td>
                                <td>
                                    <span className={`badge text-bg-${job.is_active ? 'success' : 'secondary'}`}>
                                        {job.is_active ? 'Open' : 'Closed'}
                                    </span>
                                </td>
                                <td>
                                    <Link
                                        className="btn btn-outline-primary btn-sm"
                                        to={`/recruiter/jobs/${job.id}/applicants`}
                                    >
                                        View applicants
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    )
}