FEATURE_COLUMNS = [
    'cgpa',
    'cgpa_margin',
    'skill_match_percentage',
    'num_student_skills',
    'num_required_skills',
]

ELIGIBILITY_FLAGS = [
    'cgpa_eligible',
    'branch_eligible',
    'graduation_year_eligible',
]


def prepare_features(df):
    """
    Turns the cleaned table into (X, y) for training.
    Only applications that pass ALL hard eligibility checks are kept:
    the portal already enforces those exactly, so the model's job is to
    estimate selection chances among eligible candidates.
    """
    df = df[df[ELIGIBILITY_FLAGS].min(axis=1) == 1].copy()
    df['cgpa_margin'] = df['cgpa'] - df['job_min_cgpa']

    X = df[FEATURE_COLUMNS]
    y = df['selected']
    return X, y

# Chosen by 5-fold cross-validation on the training data (see evaluation.py).
# All four candidate feature sets had ROC AUC within noise of each other
# (0.877-0.882), so the simplest set was kept.
SELECTED_FEATURES = ['cgpa', 'skill_match_percentage']