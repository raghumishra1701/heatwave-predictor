import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
INPUT_FILE = "mumbai_weather_cleaned.csv"

def run_forecast():
    print(f"📂 Loading data from {INPUT_FILE}...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print("❌ Error: File not found. Run 'clean_data.py' first!")
        return

    # 2. Prepare Data for Prophet
    print("🤖 Preparing data (Removing Timezones)...")
    
    # --- THE FIX IS HERE ---
    # Convert text to datetime, then REMOVE the timezone info (.dt.tz_localize(None))
    df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)

    # Rename columns to what Prophet needs ('ds' and 'y')
    prophet_df = df[['datetime', 'wet_bulb']].rename(columns={
        'datetime': 'ds', 
        'wet_bulb': 'y'
    })

    # 3. Setup & Train Model
    print("🧠 Training the AI model...")
    m = Prophet(daily_seasonality=True, yearly_seasonality=True)
    m.fit(prophet_df)

    # 4. Predict Future (Next 24 Hours)
    print("🔮 Forecasting the next 24 hours...")
    future = m.make_future_dataframe(periods=24, freq='h') 
    forecast = m.predict(future)

    # 5. Show Results
    next_24_hours = forecast.tail(24)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    print("\n" + "="*40)
    print("🔮 FORECAST: NEXT 24 HOURS (Wet Bulb)")
    print("="*40)
    print(next_24_hours)

    # 6. Plot the Graph
    print("\n📊 Opening graph window...")
    fig1 = m.plot(forecast)
    plt.title("Heatwave Forecast (Wet Bulb Temperature)")
    plt.xlabel("Date")
    plt.ylabel("Wet Bulb Temp (°C)")
    plt.show()

if __name__ == "__main__":
    run_forecast()