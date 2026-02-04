import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# --- CONFIGURATION ---
# Try to find the CSV file (checks both 'data' folder and root)
if os.path.exists("data/mumbai_weather_cleaned.csv"):
    INPUT_FILE = "data/mumbai_weather_cleaned.csv"
elif os.path.exists("mumbai_weather_cleaned.csv"):
    INPUT_FILE = "mumbai_weather_cleaned.csv"
else:
    print("❌ ERROR: Could not find 'mumbai_weather_cleaned.csv'.")
    print("   Please make sure your data file exists!")
    exit()

# Force save to the models folder
if not os.path.exists("models"):
    os.makedirs("models")
MODEL_FILE = "models/weather_model.pkl"

def train_now():
    print(f"📂 Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # --- 1. FEATURE ENGINEERING (MATCHING APP.PY EXACTLY) ---
    print("🛠️  Building features...")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    
    # These MUST match what is in app.py
    df['temp_lag_24h'] = df['temperature'].shift(24)
    df['wbt_lag_24h'] = df['wet_bulb'].shift(24)
    df['temp_rolling_3h'] = df['temperature'].rolling(window=3).mean()
    df['humidity_rolling_3h'] = df['humidity'].rolling(window=3).mean()
    df['temp_change_1h'] = df['temperature'].diff(1)
    
    # Target
    df['target_future_wbt'] = df['wet_bulb'].shift(-24)
    
    # Clean NaNs
    df_clean = df.dropna()

    # Define EXACT Features
    features = [
        'temperature', 'humidity', 'wet_bulb', 
        'hour', 'day_of_week', 
        'temp_lag_24h', 'wbt_lag_24h', 
        'temp_rolling_3h', 'humidity_rolling_3h', 'temp_change_1h'
    ]
    
    X = df_clean[features]
    y = df_clean['target_future_wbt']
    
    print(f"🧠 Training on {len(X)} rows...")
    model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
    model.fit(X, y)
    
    # --- 2. SAVE TO CORRECT FOLDER ---
    print(f"💾 Saving new brain to '{MODEL_FILE}'...")
    joblib.dump(model, MODEL_FILE)
    print("✅ SUCCESS! The new model is in the 'models' folder.")

if __name__ == "__main__":
    train_now()