from collections import Counter

from recruiters.models import Job
from .utils import check_eligibility, generate_match_report


def recommend_skills(student, job):
    """
    Skill-gap report for one target job. Each missing skill is ranked by how
    many OTHER active jobs the student is eligible for also require it.
    """
    report = generate_match_report(student, job)
    display = {tag.name.lower(): tag.name for tag in job.required_skills.all()}
    missing = set(report['missing_skills'])

    demand = Counter()
    other_jobs = (
        Job.objects.filter(is_active=True)
        .exclude(pk=job.pk)
        .prefetch_related('required_skills')
    )
    for other in other_jobs:
        if not check_eligibility(student, other)['overall_eligible']:
            continue
        for tag in other.required_skills.all():
            key = tag.name.lower()
            if key in missing:
                demand[key] += 1

    ranked = sorted(
        (
            {
                'skill': display[key],
                'also_required_by_other_eligible_jobs': demand[key],
            }
            for key in missing
        ),
        key=lambda r: (-r['also_required_by_other_eligible_jobs'], r['skill']),
    )

    return {
        'job_id': job.id,
        'job_title': job.title,
        'eligible_for_this_job': report['overall_eligible'],
        'skill_match_percentage': report['skill_match_percentage'],
        'matched_skills': [display[k] for k in report['matched_skills']],
        'missing_skills_ranked': ranked,
    }