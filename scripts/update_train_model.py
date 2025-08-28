import os
import sys
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# ----- Setup Django environment -----
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_energy.settings")

import django
django.setup()

from energy.models import EnergyReading

# ----- Paths -----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMMY_CSV = os.path.join(BASE_DIR, "dummy_daily_energy.csv")
COMBINED_CSV = os.path.join(BASE_DIR, "combined_daily_energy.csv")
MODEL_PATH = os.path.join(BASE_DIR, "daily_energy_model.pkl")

# ----- Step 1: Load dummy dataset -----
dummy_df = pd.read_csv(DUMMY_CSV)
dummy_count = len(dummy_df)

# ----- Step 2: Pull real readings from DB -----
readings = EnergyReading.objects.all().order_by("timestamp")
df_real = pd.DataFrame(list(readings.values("timestamp", "today_energy")))

if not df_real.empty:
    df_real['date'] = pd.to_datetime(df_real['timestamp']).dt.date
    daily_real = df_real.groupby('date')['today_energy'].max().reset_index()
    daily_real.rename(columns={'today_energy': 'daily_usage'}, inplace=True)
    real_count = len(daily_real)
else:
    daily_real = pd.DataFrame(columns=['date', 'daily_usage'])
    real_count = 0

# ----- Step 3: Combine dummy + real -----
combined_df = pd.concat([dummy_df, daily_real], ignore_index=True)
combined_df = combined_df.drop_duplicates(subset='date', keep='last')
combined_df.to_csv(COMBINED_CSV, index=False)

print(f" Combined dataset saved: {COMBINED_CSV}")
print(f"   → Dummy records: {dummy_count}, Real records: {real_count}, Total: {len(combined_df)}")

# ----- Step 4: Prepare features -----
combined_df["day_of_week"] = pd.to_datetime(combined_df["date"]).dt.dayofweek
combined_df["prev_usage"] = combined_df["daily_usage"].shift(1)
combined_df = combined_df.dropna()

X = combined_df[["day_of_week", "prev_usage"]]
y = combined_df["daily_usage"]

# ----- Step 5: Train model -----
if len(X) > 5:  # ensure enough data for train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f" Model trained. R² score: {score:.3f}")
else:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    print(" Not enough data for proper train/test split, trained on all data.")

# ----- Step 6: Save model -----
joblib.dump(model, MODEL_PATH)
print(f" Updated model saved: {MODEL_PATH}")
