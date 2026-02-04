import pandas as pd
import numpy as np
import joblib
import requests
import math
from datetime import datetime, timedelta

# --- CONFIGURATION ---
MODEL_FILE = "weather_model.pkl"
API_KEY = "d589ccc13fbb0eb3dcc24373eb4afef7" # Your Key
CITY = "Mumbai"

# --- WET BULB CALCULATION (Helper) ---
def calculate_wet_bulb(T, rh):
    try:
        tw = (T * math.atan(0.151977 * (rh + 8.313659)**0.5) +
              math.atan(T + rh) -
              math.atan(rh - 1.676331) +
              0.00391838 * (rh**1.5) * math.atan(0.023101 * rh) -
              4.686035)
        return round(tw, 2)
    except:
        return 0

def predict_next_12_hours():
    print(f"🚀 STARTING 12-HOUR FORECAST FOR {CITY.upper()}...")

    # 1. Load the Trained Model
    print(f"📂 Loading AI Model from {MODEL_FILE}...")
    try:
        model = joblib.load(MODEL_FILE)
    except FileNotFoundError:
        print("❌ Error: 'weather_model.pkl' not found. Train your model first!")
        return

    # 2. Get Current Weather (The Starting Point)
    print("☁️ Fetching live weather data...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    if response.get('cod') != 200:
        print("❌ Error fetching API data.")
        return

    current_temp = response['main']['temp']
    current_humidity = response['main']['humidity']
    current_wbt = calculate_wet_bulb(current_temp, current_humidity)
    
    print(f"   Current Status: {current_temp}°C | {current_humidity}% Humidity | {current_wbt}°C Wet Bulb")

    # 3. Generate Inputs for Next 12 Hours
    # The model expects: ['temperature', 'humidity', 'wet_bulb', 'hour', 'day_of_week', 'temp_lag_24h', 'wbt_lag_24h']
    
    future_data = []
    current_time = datetime.now()

    print("🔮 Generating predictions...")
    
    for i in range(1, 13):
        # Calculate Future Time
        future_time = current_time + timedelta(hours=i)
        
        # --- ESTIMATE FUTURE INPUTS (Hackathon Logic) ---
        # Realistically, we'd use a forecast API here. 
        # For this demo, we simulate a slight cooling trend if it's night.
        
        # Simple Logic: If it's night (18:00 - 06:00), temp drops 0.5°C per hour.
        is_night = future_time.hour < 6 or future_time.hour > 18
        temp_change = -0.5 if is_night else 0.5
        
        estimated_temp = current_temp + (temp_change * i) # Simulating temp change
        estimated_humidity = current_humidity # Keeping humidity constant for simplicity
        estimated_wbt = calculate_wet_bulb(estimated_temp, estimated_humidity)

        # Create the row of features
        row = {
            'temperature': estimated_temp,
            'humidity': estimated_humidity,
            'wet_bulb': estimated_wbt,       # The "current" WBT for that hour
            'hour': future_time.hour,
            'day_of_week': future_time.weekday(),
            
            # For "Lag" (History), we just use the current start values as a proxy
            # (Since we don't have yesterday's live data in memory)
            'temp_lag_24h': current_temp,   
            'wbt_lag_24h': current_wbt
        }
        
        # Save timestamp for display
        row['timestamp'] = future_time.strftime("%I:%M %p") 
        future_data.append(row)

    # Convert to DataFrame
    df_future = pd.DataFrame(future_data)

    # 4. Predict Using the AI
    # Select only the columns the model was trained on
    features = ['temperature', 'humidity', 'wet_bulb', 'hour', 'day_of_week', 'temp_lag_24h', 'wbt_lag_24h']
    
    # Make Prediction
    predictions = model.predict(df_future[features])

    # 5. Display Results
    print("\n" + "="*50)
    print(f"📊 12-HOUR WET BULB FORECAST ({datetime.now().date()})")
    print("="*50)
    print(f"{'TIME':<12} | {'PREDICTED WBT':<15} | {'STATUS'}")
    print("-" * 50)

    results = []
    for i, pred_wbt in enumerate(predictions):
        time_label = df_future.iloc[i]['timestamp']
        val = round(pred_wbt, 2)
        
        # Determine Safety Status
        if val < 28: status = "🟢 Safe"
        elif val < 30: status = "🟡 Caution"
        elif val < 32: status = "🟠 Danger"
        else: status = "🔴 LETHAL"

        print(f"{time_label:<12} | {val:>5.2f}°C          | {status}")
        
        results.append({"time": time_label, "wbt": val, "status": status})

    return results

if __name__ == "__main__":
    predict_next_12_hours()