import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import sklearn

ARTIFACT_DIR = Path(__file__).resolve().parent / 'artifacts'
MODEL_PATH = ARTIFACT_DIR / 'placement_model.joblib'
META_PATH = ARTIFACT_DIR / 'placement_model_meta.json'


def save_model(model, metadata):
    """Saves the fitted pipeline plus a readable metadata file."""
    ARTIFACT_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metadata = {
        **metadata,
        'saved_at': datetime.now(timezone.utc).isoformat(),
        'sklearn_version': sklearn.__version__,
    }
    META_PATH.write_text(json.dumps(metadata, indent=2))


def load_model():
    return joblib.load(MODEL_PATH)


def load_metadata():
    return json.loads(META_PATH.read_text())