import joblib
import os
import pandas as pd
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "daily_energy_model.pkl")
_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_tomorrow_energy(latest_reading):
    """
    Predicts tomorrow's energy usage based on the latest reading.
    Uses the same features as used during training: 
    - day_of_week
    - prev_usage (today's energy)
    """
    model = load_model()

    day_of_week = (latest_reading.timestamp.weekday() + 1) % 7  # tomorrow's day
    prev_usage = latest_reading.today_energy

    # Feature dataframe with exact same columns as training
    X = pd.DataFrame([{
        "day_of_week": day_of_week,
        "prev_usage": prev_usage
    }])

    prediction = model.predict(X)[0]
    return round(float(prediction), 2)
