from django.core.management.base import BaseCommand
from sklearn.dummy import DummyClassifier

from prediction.cleaning import clean_dataframe
from prediction.dataset import build_training_dataframe
from prediction.evaluation import evaluate_on_test
from prediction.features import SELECTED_FEATURES, prepare_features
from prediction.persistence import MODEL_PATH, save_model
from prediction.training import split_data, train_model


class Command(BaseCommand):
    help = "Trains the placement prediction model, evaluates it, and saves it."

    def handle(self, *args, **options):
        df, cleaning_report = clean_dataframe(build_training_dataframe())
        X, y = prepare_features(df)
        X = X[SELECTED_FEATURES]
        self.stdout.write(f"Cleaning report: {cleaning_report}")
        self.stdout.write(f"Eligible rows used: {len(X)}")

        X_train, X_test, y_train, y_test = split_data(X, y)

        # 1. Fit on the training split, score once on the held-out test set
        eval_model = train_model(X_train, y_train)
        test_metrics = evaluate_on_test(eval_model, X_test, y_test)
        baseline = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
        baseline_metrics = evaluate_on_test(baseline, X_test, y_test)
        self.stdout.write(f"MODEL    {test_metrics}")
        self.stdout.write(f"BASELINE {baseline_metrics}")

        # 2. Refit the same procedure on ALL eligible rows for the saved model
        final_model = train_model(X, y)

        save_model(final_model, {
            'features': SELECTED_FEATURES,
            'rows_total': len(X),
            'rows_train_split': len(X_train),
            'rows_test_split': len(X_test),
            'test_metrics': test_metrics,
            'baseline_metrics': baseline_metrics,
            'note': (
                "Trained on SYNTHETIC data. test_metrics were measured on a "
                "model fitted on the training split only; the saved model was "
                "refitted on all eligible rows with the same procedure."
            ),
        })
        self.stdout.write(self.style.SUCCESS(f"Model saved to {MODEL_PATH}"))