import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib 
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
INPUT_FILE = "mumbai_weather_cleaned.csv"
MODEL_FILE = "weather_model.pkl"

def train_and_save():
    print("🚀 STARTING ADVANCED TRAINING...")

    # 1. Load Data
    print(f"📂 Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print("❌ Error: File not found. Run 'clean_data.py' first!")
        return

    # 2. FEATURE ENGINEERING (Improvement #1)
    # We are adding "context" so the model sees trends, not just numbers.
    print("🛠️ Creating smart features (Rolling Averages & Lags)...")
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    
    # Lag Features (What happened 24h ago?)
    df['temp_lag_24h'] = df['temperature'].shift(24)
    df['wbt_lag_24h'] = df['wet_bulb'].shift(24)
    
    # Rolling Features (What was the trend over the last 3 hours?)
    df['temp_rolling_3h'] = df['temperature'].rolling(window=3).mean()
    df['humidity_rolling_3h'] = df['humidity'].rolling(window=3).mean()
    
    # Rate of Change (Is it heating up fast?)
    df['temp_change_1h'] = df['temperature'].diff(1)

    # 3. Create Target
    df['target_future_wbt'] = df['wet_bulb'].shift(-24)

    # Cleanup empty rows caused by shifting/rolling
    df_clean = df.dropna().copy()

    # Define Input Features (X) - Now with 10 powerful inputs!
    features = [
        'temperature', 'humidity', 'wet_bulb', 
        'hour', 'day_of_week', 
        'temp_lag_24h', 'wbt_lag_24h', 
        'temp_rolling_3h', 'humidity_rolling_3h', 'temp_change_1h'
    ]
    
    X = df_clean[features]
    y = df_clean['target_future_wbt']

    print(f"📊 Training on {len(X)} rows with {len(features)} features.")

    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. HYPERPARAMETER TUNING (Improvement #2)
    # Instead of guessing, we test multiple settings to find the best one.
    print("🤖 Optimizing Model Settings (This may take 30-60 seconds)...")
    
    param_dist = {
        'n_estimators': [100, 200],      # Try 100 or 200 trees
        'max_depth': [None, 10, 20],     # Try different depths
        'min_samples_leaf': [1, 2, 4]    # Try different leaf sizes
    }
    
    rf = RandomForestRegressor(random_state=42)
    
    # Search for the best combination
    random_search = RandomizedSearchCV(
        estimator=rf, 
        param_distributions=param_dist, 
        n_iter=5,              # Try 5 random combinations
        cv=3,                  # Cross-check 3 times
        verbose=1, 
        n_jobs=-1,             # Use all computer power
        random_state=42
    )
    
    random_search.fit(X_train, y_train)
    
    # Get the winner
    best_model = random_search.best_estimator_
    print(f"✨ Best Settings Found: {random_search.best_params_}")

    # 6. Evaluate
    print("🔮 Evaluating Performance...")
    predictions = best_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    print("\n" + "="*40)
    print("🏆 FINAL ACCURACY REPORT")
    print("="*40)
    print(f"✅ MAE (Avg Error):  {mae:.2f}°C")
    print(f"✅ RMSE (Root Error): {rmse:.2f}°C")
    
    # 7. Save the BEST Model
    print(f"\n💾 Saving optimized model to '{MODEL_FILE}'...")
    joblib.dump(best_model, MODEL_FILE)
    print("✅ SUCCESS! Your AI is now smarter and saved.")

if __name__ == "__main__":
    train_and_save()