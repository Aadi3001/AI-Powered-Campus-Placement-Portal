import { useEffect, useState } from 'react'
import api from '../api.js'

const CHECK_LABELS = {
    cgpa: 'CGPA',
    branch: 'Branch',
    graduation_year: 'Graduation year',
}

export default function JobInsights({ jobId }) {
    const [chance, setChance] = useState(null)
    const [gap, setGap] = useState(null)
    const [error, setError] = useState('')

    useEffect(() => {
        Promise.all([
            api.get(`/prediction/jobs/${jobId}/my-chance/`),
            api.get(`/matching/jobs/${jobId}/skill-gap/`),
        ])
            .then(([chanceRes, gapRes]) => {
                setChance(chanceRes.data)
                setGap(gapRes.data)
            })
            .catch(() => setError('Could not load your match details.'))
    }, [jobId])

    if (error) return <div className="alert alert-danger mt-3 mb-0">{error}</div>
    if (!chance || !gap) {
        return <p className="text-muted small mt-3 mb-0">Loading...</p>
    }

    const percent =
        chance.selection_probability === null
            ? null
            : Math.round(chance.selection_probability * 100)

    return (
        <div className="border-top mt-3 pt-3 small">
            <div className="mb-3">
                <strong>Eligibility</strong>
                <ul className="list-unstyled mb-0">
                    {Object.entries(chance.eligibility_checks).map(([key, ok]) => (
                        <li key={key}>
                            {ok ? '✓' : '✗'} {CHECK_LABELS[key]}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="mb-3">
                <strong>Estimated chance of selection</strong>
                {percent === null ? (
                    <div className="text-muted">{chance.detail}</div>
                ) : (
                    <div className="progress" role="progressbar" aria-valuenow={percent}
                        aria-valuemin="0" aria-valuemax="100">
                        <div className="progress-bar" style={{ width: `${percent}%` }}>
                            {percent}%
                        </div>
                    </div>
                )}
                <div className="text-muted fst-italic">{chance.disclaimer}</div>
            </div>

            <div>
                <strong>Skills</strong>
                <div>
                    {gap.matched_skills.map((name) => (
                        <span key={name} className="badge text-bg-success me-1">{name}</span>
                    ))}
                    {gap.missing_skills_ranked.map((item) => {
                        const n = item.also_required_by_other_eligible_jobs
                        return (
                            <span key={item.skill} className="badge text-bg-warning me-1">
                                {item.skill}
                                {n > 0 && ` (also needed by ${n} other job${n > 1 ? 's' : ''})`}
                            </span>
                        )
                    })}
                    {gap.matched_skills.length === 0 &&
                        gap.missing_skills_ranked.length === 0 && (
                            <span className="text-muted">This job lists no required skills.</span>
                        )}
                </div>
                <div className="text-muted">Green: skills you have. Yellow: skills to learn.</div>
            </div>
        </div>
    )
}