import pandas as pd
import math

# --- CONFIGURATION ---
INPUT_FILE = "mumbai_weather_history.csv"  # The messy file
OUTPUT_FILE = "mumbai_weather_cleaned.csv" # The clean file

# --- WET BULB FORMULA ---
def calculate_wet_bulb(row):
    # Skip calculation if data is still missing
    if pd.isna(row['temperature']) or pd.isna(row['humidity']):
        return None
        
    T = row['temperature']
    rh = row['humidity']
    
    try:
        tw = (T * math.atan(0.151977 * (rh + 8.313659)**0.5) +
              math.atan(T + rh) -
              math.atan(rh - 1.676331) +
              0.00391838 * (rh**1.5) * math.atan(0.023101 * rh) -
              4.686035)
        return round(tw, 2)
    except:
        return None

def clean_and_process():
    print(f"📂 Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print("❌ Error: File not found. Make sure the CSV name is correct.")
        return

    # 1. Check Initial State
    print(f"   Original Rows: {len(df)}")
    print(f"   Missing Values:\n{df.isnull().sum()}\n")

    # 2. Remove Duplicates
    # Sometimes downloading twice creates duplicate rows
    df = df.drop_duplicates()
    print(f"✅ Removed duplicates. Rows remaining: {len(df)}")

    # 3. Handle Missing Values
    # For weather, we use 'Forward Fill' (ffill). 
    # Logic: If 10:00 AM is missing, assume it's same as 9:00 AM.
    df = df.ffill() 
    print("✅ Filled missing values using forward-fill.")

    # 4. Validate Data Ranges
    # Remove "impossible" weather (e.g., 200°C or -500% humidity)
    # Valid Temp: -50 to 60°C | Valid Hum: 0 to 100%
    initial_count = len(df)
    df = df[
        (df['temperature'] >= -50) & (df['temperature'] <= 60) &
        (df['humidity'] >= 0) & (df['humidity'] <= 100)
    ]
    removed = initial_count - len(df)
    print(f"✅ Removed {removed} rows with impossible values (errors).")

    # 5. Add Wet Bulb Column
    print("🧮 Calculating Wet Bulb Temperature...")
    df['wet_bulb'] = df.apply(calculate_wet_bulb, axis=1)

    # 6. Save Cleaned Data
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n🎉 SUCCESS! Cleaned data saved to: {OUTPUT_FILE}")
    print(df.head())

if __name__ == "__main__":
    clean_and_process()