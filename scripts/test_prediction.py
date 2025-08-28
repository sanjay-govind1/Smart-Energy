import joblib
import pandas as pd
from datetime import datetime

# Load trained model
model = joblib.load("daily_energy_model.pkl")

# Example input: tomorrow is day 3, today usage = 20 Wh
tomorrow_day = (datetime.now().weekday() + 1) % 7
X_test = pd.DataFrame([{
    "day_of_week": tomorrow_day,
    "prev_usage": 20
}])

prediction = model.predict(X_test)[0]
print(f"🔮 Predicted energy usage for tomorrow: {prediction:.2f} Wh")
