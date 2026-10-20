import { useEffect, useState } from 'react'
import api from '../../api.js'

const STATUS_ORDER = ['SELECTED', 'SHORTLISTED', 'APPLIED', 'REJECTED']
const STATUS_COLORS = {
    SELECTED: 'success',
    SHORTLISTED: 'info',
    APPLIED: 'secondary',
    REJECTED: 'danger',
}

function StatCard({ label, value, hint }) {
    return (
        <div className="col-6 col-md-4 col-lg-2">
            <div className="card h-100">
                <div className="card-body">
                    <div className="text-muted small">{label}</div>
                    <div className="fs-3 fw-semibold">{value}</div>
                    {hint && <div className="text-muted small">{hint}</div>}
                </div>
            </div>
        </div>
    )
}

export default function Dashboard() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        api.get('/tpo/stats/')
            .then((res) => setStats(res.data))
            .catch(() => setError('Could not load the statistics.'))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="container py-5">Loading...</div>
    if (!stats) {
        return (
            <div className="container py-5">
                <div className="alert alert-danger">{error}</div>
            </div>
        )
    }

    const {
        totals,
        placement,
        application_status: statusCounts,
        by_branch: byBranch,
        top_companies: topCompanies,
        busiest_jobs: busiestJobs,
        model,
    } = stats

    const totalApplications = totals.applications || 1

    return (
        <div className="container py-4">
            <h1 className="mb-3">Placement dashboard</h1>

            <div className="alert alert-warning">
                <strong>Demonstration data.</strong> This portal currently holds records
                generated for testing. The selected and rejected outcomes were produced by
                a synthetic rule, so these figures show how the dashboard works. They are
                not real placement results.
            </div>

            <div className="row g-3 mb-4">
                <StatCard label="Students" value={totals.students} />
                <StatCard label="Recruiters" value={totals.recruiters} />
                <StatCard label="Companies" value={totals.companies} />
                <StatCard
                    label="Jobs"
                    value={totals.jobs}
                    hint={`${totals.open_jobs} open`}
                />
                <StatCard label="Applications" value={totals.applications} />
                <StatCard
                    label="Placement rate"
                    value={`${placement.placement_rate}%`}
                    hint={`${placement.students_placed} students placed`}
                />
            </div>

            <div className="card mb-4">
                <div className="card-body">
                    <h5 className="card-title">Applications by status</h5>
                    <div className="progress mb-2" style={{ height: 24 }}>
                        {STATUS_ORDER.map((status) => (
                            <div
                                key={status}
                                className={`progress-bar bg-${STATUS_COLORS[status]}`}
                                style={{ width: `${((statusCounts[status] ?? 0) / totalApplications) * 100}%` }}
                                title={`${status}: ${statusCounts[status] ?? 0}`}
                            />
                        ))}
                    </div>
                    <div className="d-flex flex-wrap gap-3 small">
                        {STATUS_ORDER.map((status) => (
                            <span key={status}>
                                <span className={`badge text-bg-${STATUS_COLORS[status]} me-1`}>
                                    {status}
                                </span>
                                {statusCounts[status] ?? 0}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            <div className="card mb-4">
                <div className="card-body">
                    <h5 className="card-title">Placement by branch</h5>
                    <table className="table align-middle mb-2">
                        <thead>
                            <tr>
                                <th>Branch</th>
                                <th>Students</th>
                                <th>Placed</th>
                                <th style={{ width: '35%' }}>Placement rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            {byBranch.map((row) => {
                                const rate = row.total ? Math.round((100 * row.placed) / row.total) : 0
                                return (
                                    <tr key={row.branch}>
                                        <td>{row.label}</td>
                                        <td>{row.total}</td>
                                        <td>{row.placed}</td>
                                        <td>
                                            <div className="progress" role="progressbar" aria-valuenow={rate}
                                                aria-valuemin="0" aria-valuemax="100">
                                                <div className="progress-bar" style={{ width: `${rate}%` }}>
                                                    {rate}%
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                    <div className="text-muted small">
                        Differences between branches here come from randomly generated demo
                        data and say nothing about real branches.
                    </div>
                </div>
            </div>

            <div className="row g-4 mb-4">
                <div className="col-lg-5">
                    <div className="card h-100">
                        <div className="card-body">
                            <h5 className="card-title">Most selections by company</h5>
                            <table className="table table-sm mb-0">
                                <tbody>
                                    {topCompanies.map((row) => (
                                        <tr key={row.company}>
                                            <td>{row.company}</td>
                                            <td className="text-end">{row.selected}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div className="col-lg-7">
                    <div className="card h-100">
                        <div className="card-body">
                            <h5 className="card-title">Busiest jobs</h5>
                            <table className="table table-sm mb-0">
                                <thead>
                                    <tr>
                                        <th>Job</th>
                                        <th>Company</th>
                                        <th className="text-end">Applicants</th>
                                        <th className="text-end">Selected</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {busiestJobs.map((job, i) => (
                                        <tr key={i}>
                                            <td>{job.job}</td>
                                            <td>{job.company ?? '—'}</td>
                                            <td className="text-end">{job.applicants}</td>
                                            <td className="text-end">{job.selected}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            {model && (
                <div className="card">
                    <div className="card-body">
                        <h5 className="card-title">Selection-estimate model</h5>
                        <table className="table table-sm w-auto">
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Model</th>
                                    <th>Always-reject baseline</th>
                                </tr>
                            </thead>
                            <tbody>
                                {[
                                    ['Accuracy', 'accuracy'],
                                    ['ROC AUC', 'roc_auc'],
                                    ['Precision', 'precision'],
                                    ['Recall', 'recall'],
                                ].map(([label, key]) => (
                                    <tr key={key}>
                                        <td>{label}</td>
                                        <td>{model.test_metrics[key]}</td>
                                        <td>{model.baseline_metrics[key]}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <p className="small text-muted mb-1">
                            Features used: {model.features.join(', ')}. Measured on{' '}
                            {model.rows_test_split} held-out applications out of{' '}
                            {model.rows_total} eligible ones. With a test set this small, these
                            figures are approximate.
                        </p>
                        <p className="small fst-italic text-muted mb-0">{model.note}</p>
                    </div>
                </div>
            )}
        </div>
    )
}