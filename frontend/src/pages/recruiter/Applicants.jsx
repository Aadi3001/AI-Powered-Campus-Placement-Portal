import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import api from '../../api.js'

const STATUSES = ['APPLIED', 'SHORTLISTED', 'REJECTED', 'SELECTED']
const PAGE_SIZE = 25

function failedChecks(r) {
    return [
        !r.cgpa_eligible && 'CGPA',
        !r.branch_eligible && 'Branch',
        !r.graduation_year_eligible && 'Graduation year',
    ].filter(Boolean)
}

export default function Applicants() {
    const { jobId } = useParams()
    const [reports, setReports] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [visible, setVisible] = useState(PAGE_SIZE)

    useEffect(() => {
        api.get(`/matching/jobs/${jobId}/report/`)
            .then((res) => setReports(res.data))
            .catch(() => setError('Could not load the applicants for this job.'))
            .finally(() => setLoading(false))
    }, [jobId])

    const changeStatus = async (applicationId, status) => {
        setError('')
        try {
            await api.patch(`/applications/${applicationId}/status/`, { status })
            setReports((prev) =>
                prev.map((r) => (r.application_id === applicationId ? { ...r, status } : r)),
            )
        } catch {
            setError('Could not update the status.')
        }
    }

    if (loading) return <div className="container py-5">Loading applicants...</div>

    const jobTitle = reports[0]?.job_title

    return (
        <div className="container py-4">
            <Link to="/recruiter/jobs" className="small">← Back to my jobs</Link>
            <h1 className="mt-2">Applicants{jobTitle ? `: ${jobTitle}` : ''}</h1>
            <p className="text-muted">
                Eligible candidates are listed first, then ranked by skill match (highest
                first), with CGPA breaking ties. This ranking is a tool to help your
                review. It does not make decisions.
            </p>
            {error && <div className="alert alert-danger">{error}</div>}
            {!error && reports.length === 0 && (
                <p className="text-muted">No one has applied yet.</p>
            )}
            {reports.length > 0 && (
                <>
                    <table className="table align-middle">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Candidate</th>
                                <th>CGPA</th>
                                <th>Skill match</th>
                                <th>Skills</th>
                                <th>Eligibility</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reports.slice(0, visible).map((r) => (
                                <tr key={r.application_id}>
                                    <td>{r.rank}</td>
                                    <td>{r.student_name || `Student #${r.student_id}`}</td>
                                    <td>{r.cgpa ?? '—'}</td>
                                    <td>{r.skill_match_percentage}%</td>
                                    <td>
                                        {r.matched_skills.map((s) => (
                                            <span key={s} className="badge text-bg-success text-capitalize me-1">
                                                {s}
                                            </span>
                                        ))}
                                        {r.missing_skills.map((s) => (
                                            <span key={s} className="badge text-bg-warning text-capitalize me-1">
                                                {s}
                                            </span>
                                        ))}
                                    </td>
                                    <td>
                                        {r.overall_eligible ? (
                                            <span className="badge text-bg-success">Eligible</span>
                                        ) : (
                                            <>
                                                <span className="badge text-bg-danger">Not eligible</span>
                                                <div className="small text-muted">
                                                    {failedChecks(r).join(', ')}
                                                </div>
                                            </>
                                        )}
                                    </td>
                                    <td>
                                        <select
                                            className="form-select form-select-sm"
                                            value={r.status}
                                            onChange={(e) => changeStatus(r.application_id, e.target.value)}
                                        >
                                            {STATUSES.map((s) => (
                                                <option key={s} value={s}>{s}</option>
                                            ))}
                                        </select>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {visible < reports.length && (
                        <button
                            className="btn btn-outline-secondary"
                            onClick={() => setVisible((v) => v + PAGE_SIZE)}
                        >
                            Show more ({reports.length - visible} remaining)
                        </button>
                    )}
                    <p className="text-muted small mt-2">
                        Showing {Math.min(visible, reports.length)} of {reports.length}.
                        Green: skills the candidate has. Yellow: required skills they are missing.
                    </p>
                </>
            )}
        </div>
    )
}