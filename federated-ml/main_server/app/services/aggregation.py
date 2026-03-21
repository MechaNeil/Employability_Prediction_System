from __future__ import annotations

import numpy as np
import joblib

from main_server.app.core.config import GLOBAL_MODEL_PATH


class MajorityVoteEnsemble:
    def __init__(self, models):
        self.models = models

    def predict(self, x):
        predictions = np.array([model.predict(x) for model in self.models])
        # Tie handling: choose class 1 when vote count is equal.
        votes_for_one = predictions.sum(axis=0)
        return (votes_for_one >= (len(self.models) / 2)).astype(int)

    def predict_proba(self, x):
        probability_slices = []
        for model in self.models:
            if hasattr(model, "predict_proba"):
                probability_slices.append(model.predict_proba(x))
            else:
                preds = model.predict(x)
                probability_slices.append(np.vstack([1 - preds, preds]).T)
        return np.mean(probability_slices, axis=0)


def aggregate_models(models: list[object]) -> str:
    ensemble_model = MajorityVoteEnsemble(models)
    joblib.dump(ensemble_model, GLOBAL_MODEL_PATH)
    return str(GLOBAL_MODEL_PATH)
