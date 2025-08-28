import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_data(days=60):
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]

    # Create synthetic daily usage (random with weekly pattern)
    usage = []
    for i, d in enumerate(dates):
        base = 15 + (d.weekday() % 5) * 2   # weekdays grow
        noise = np.random.randint(-3, 3)    # random fluctuation
        usage.append(max(10, base + noise)) # minimum 10 Wh

    df = pd.DataFrame({
        "date": [d.date() for d in dates],
        "daily_usage": usage
    })

    df.to_csv("dummy_daily_energy.csv", index=False)
    print("✅ Dummy dataset created: dummy_daily_energy.csv")

if __name__ == "__main__":
    generate_dummy_data()
