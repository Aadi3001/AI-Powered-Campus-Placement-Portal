import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate

from .training import build_model, RANDOM_STATE
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
)


def cross_validate_feature_sets(X_train, y_train, feature_sets, n_splits=5):
    """
    Compares feature sets using stratified k-fold cross-validation on the
    TRAINING data only (the test set stays untouched).
    Returns a table with the mean and spread (std) of each metric.
    """
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    scoring = {'accuracy': 'accuracy', 'f1': 'f1', 'roc_auc': 'roc_auc'}

    rows = []
    for name, columns in feature_sets.items():
        scores = cross_validate(
            build_model(), X_train[columns], y_train, cv=cv, scoring=scoring
        )
        rows.append({
            'feature_set': name,
            'accuracy': scores['test_accuracy'].mean(),
            'accuracy_std': scores['test_accuracy'].std(),
            'f1': scores['test_f1'].mean(),
            'roc_auc': scores['test_roc_auc'].mean(),
            'roc_auc_std': scores['test_roc_auc'].std(),
        })

    return pd.DataFrame(rows).set_index('feature_set')

def evaluate_on_test(model, X_test, y_test):
    """
    Scores a fitted model on the held-out test set.
    zero_division=0 covers the baseline, which never predicts 'selected'.
    """
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        'accuracy': round(accuracy_score(y_test, predictions), 3),
        'precision': round(precision_score(y_test, predictions, zero_division=0), 3),
        'recall': round(recall_score(y_test, predictions, zero_division=0), 3),
        'f1': round(f1_score(y_test, predictions, zero_division=0), 3),
        'roc_auc': round(roc_auc_score(y_test, probabilities), 3),
        'confusion_matrix': confusion_matrix(y_test, predictions).tolist(),
    }