import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta
import sys

# --- CONFIGURATION ---
CITY_NAME = "Mumbai"
LATITUDE = 19.0760
LONGITUDE = 72.8777
FILENAME = "mumbai_weather_history.csv"

def download_historical_weather():
    print(f"--- 📉 STARTING DOWNLOAD FOR {CITY_NAME.upper()} ---")

    # 1. Setup Client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # 2. Calculate Dates (Past 365 Days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    
    print(f"📅 Time Range: {start_date} to {end_date}")

    # 3. Define the Request
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m"],
        "timezone": "auto"
    }

    try:
        # 4. Fetch Data
        print("⏳ Connecting to Open-Meteo Archive API...")
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        print(f"✅ Data received!")

        # 5. Parse Hourly Data
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

        # Create DataFrame
        hourly_data = {"datetime": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end   = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq  = pd.Timedelta(seconds=hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature"] = hourly_temperature_2m
        hourly_data["humidity"] = hourly_relative_humidity_2m
        hourly_data["location"] = CITY_NAME

        df = pd.DataFrame(data=hourly_data)
        
        # Round values
        df["temperature"] = df["temperature"].round(2)
        df["humidity"] = df["humidity"].round(2)

        # 6. Save to CSV
        print(f"💾 Saving {len(df)} rows to '{FILENAME}'...")
        df.to_csv(FILENAME, index=False)
        print(f"\n✅ SUCCESS! File saved: {FILENAME}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    download_historical_weather()