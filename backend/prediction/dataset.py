import pandas as pd

from applications.models import Application
from matching.utils import generate_match_report


def build_training_dataframe():
    """
    Builds one row per RESOLVED application (SELECTED or REJECTED).
    Unresolved applications (APPLIED, SHORTLISTED) have no known outcome,
    so they cannot be used as training labels.
    """
    resolved = Application.objects.filter(
        status__in=['SELECTED', 'REJECTED']
    ).select_related('student', 'job')

    rows = []
    for app in resolved:
        student = app.student
        job = app.job
        report = generate_match_report(student, job)

        rows.append({
            'application_id': app.id,
            'cgpa': float(student.cgpa) if student.cgpa is not None else None,
            'job_min_cgpa': float(job.min_cgpa) if job.min_cgpa is not None else None,
            'skill_match_percentage': report['skill_match_percentage'],
            'num_student_skills': student.skills.count(),
            'num_required_skills': job.required_skills.count(),
            'cgpa_eligible': int(report['cgpa_eligible']),
            'branch_eligible': int(report['branch_eligible']),
            'graduation_year_eligible': int(report['graduation_year_eligible']),
            'selected': 1 if app.status == 'SELECTED' else 0,
        })

    return pd.DataFrame(rows)