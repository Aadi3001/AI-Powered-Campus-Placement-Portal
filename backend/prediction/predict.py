from functools import lru_cache

import pandas as pd

from matching.utils import generate_match_report
from .features import SELECTED_FEATURES
from .persistence import load_model

DISCLAIMER = (
    "Estimate from a demonstration model trained on synthetic data. "
    "It is not a prediction of real hiring outcomes."
)


@lru_cache(maxsize=1)
def get_model():
    """Loads the saved model once and reuses it for later calls."""
    return load_model()


def predict_selection_probability(student, job):
    report = generate_match_report(student, job)

    result = {
        'job_id': job.id,
        'job_title': job.title,
        'eligible': report['overall_eligible'],
        'eligibility_checks': {
            'cgpa': report['cgpa_eligible'],
            'branch': report['branch_eligible'],
            'graduation_year': report['graduation_year_eligible'],
        },
        'matched_skills': report['matched_skills'],
        'missing_skills': report['missing_skills'],
        'selection_probability': None,
        'disclaimer': DISCLAIMER,
    }

    if not report['overall_eligible']:
        result['detail'] = "Not eligible for this job, so no estimate is given."
        return result

    if student.cgpa is None:
        result['detail'] = "Add your CGPA to your profile to get an estimate."
        return result

    # Same two features, from the same sources, as in training
    row = pd.DataFrame([{
        'cgpa': float(student.cgpa),
        'skill_match_percentage': report['skill_match_percentage'],
    }])[SELECTED_FEATURES]

    probability = get_model().predict_proba(row)[0, 1]
    result['selection_probability'] = round(float(probability), 3)
    return result