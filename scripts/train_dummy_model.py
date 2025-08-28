import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train_dummy_model():
    df = pd.read_csv("dummy_daily_energy.csv")
    df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["prev_usage"] = df["daily_usage"].shift(1)
    df = df.dropna()

    X = df[["day_of_week", "prev_usage"]]
    y = df["daily_usage"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print("✅ Model trained with dummy data. R² score:", round(score, 3))

    joblib.dump(model, "daily_energy_model.pkl")
    print("📂 Saved model: daily_energy_model.pkl")

if __name__ == "__main__":
    train_dummy_model()
