from sklearn.model_selection import train_test_split

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