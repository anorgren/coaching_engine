from abc import ABC
from typing import Optional
import numpy as np

from ..dto import UserProfile


class DemoModel:
    """Trivial model for demonstration purposes."""
    def predict_proba(self, data: np.ndarray) -> float:
        """Predicts a random value between 0 and 1 for the user profile based off the profile data"""
        # Collapse the array to a single deterministic integer seed w/ 32 bit mask
        seed = int(abs(data.sum()) * 1e6) & 0xFFFFFFFF

        return np.random.default_rng(seed).random()


class RiskPredictor(ABC):
    def __init__(self, path: Optional[str] = None, model: Optional = None):
        """
        Initialize the RiskPredictor.

        Args:
            path (str): Path to the model file.
            model: Preloaded model object, must implement 'predict_proba' function.
        """
        if not path and not model:
            raise ValueError("Either path or model must be provided.")

        if model:
            self.model = model
        else:
            import joblib

            if not path.endswith(".joblib"):
                raise ValueError("Model file must be a .joblib file.")

            self.model = joblib.load(path)

    def score(self, profile: UserProfile) -> float:
        """Score the data and return a risk value from 0-1"""
        data = self.convert_user_profile_to_data(profile)
        return float(self.model.predict_proba(data))

    @staticmethod
    def convert_user_profile_to_data(profile: UserProfile) -> np.ndarray:
        """Convert the user profile to a format suitable for scoring."""
        h = float(profile.height_cm) if profile.height_cm is not None else np.nan
        w = float(profile.weight_kg) if profile.weight_kg is not None else np.nan

        # binary encode sex
        if profile.sex is None:
            s = np.nan
        elif profile.sex.lower() == "female":
            s = 1.0
        else:
            s = 0.0

        return np.array([profile.age, h, w, s], dtype=float)


class DemoRiskPredictor(RiskPredictor):
    """Demo risk predictor for testing purposes."""
    DEMO_HIGH_RISK_IDS = {"high_risk_user_1", "high_risk_user_2"}
    DEMO_MED_RISK_IDS = {"med_risk_user_1", "med_risk_user_2"}
    DEMO_LOW_RISK_IDS = {"low_risk_user_1", "low_risk_user_2"}

    def __init__(self):
        super().__init__(model=DemoModel())

    def score(self, profile: UserProfile) -> float:
        """Score the data and return a risk value."""
        if profile.user_id in self.DEMO_HIGH_RISK_IDS:
            return 1.0
        if profile.user_id in self.DEMO_MED_RISK_IDS:
            return 0.5
        if profile.user_id in self.DEMO_LOW_RISK_IDS:
            return 0.0

        return super().score(profile)


class XGBoostRiskPredictor(RiskPredictor):
    """
    XGBoost risk predictor created using the data set here:
    https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset/data
    """
    def __init__(self):
        super().__init__(path="xgb_risk_model.joblib")


class XGBoostSyntheticRiskPredictor(RiskPredictor):
    """XGBoost risk predictor created using the real dataset from below as well as synthetic data:
    https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset/data
    """
    def __init__(self):
        super().__init__(path="xgb_synthetic_risk_model.joblib")


# singletons
demo_risk_predictor = DemoRiskPredictor()
