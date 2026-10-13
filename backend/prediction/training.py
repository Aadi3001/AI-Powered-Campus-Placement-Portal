from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def split_data(X, y, test_size=0.25):
    """
    Splits features and labels into a training set and a held-out test set.
    stratify=y keeps the selected/rejected proportions the same in both
    parts, which matters when the dataset is small.
    """
    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )

def build_model():
    """
    Logistic Regression wrapped in a pipeline with feature scaling.
    The scaler is fitted on the training data only (when .fit is called),
    so nothing leaks from the test set.
    """
    return Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter=1000)),
    ])


def train_model(X_train, y_train):
    model = build_model()
    model.fit(X_train, y_train)
    return model