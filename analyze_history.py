import pandas as pd
import math

# --- CONFIGURATION ---
INPUT_FILE = "mumbai_weather_history.csv"

# --- WET BULB FORMULA (Stull 2011) ---
def calculate_wet_bulb(row):
    T = row['temperature']
    rh = row['humidity']
    
    tw = (T * math.atan(0.151977 * (rh + 8.313659)**0.5) +
          math.atan(T + rh) -
          math.atan(rh - 1.676331) +
          0.00391838 * (rh**1.5) * math.atan(0.023101 * rh) -
          4.686035)
    return round(tw, 2)

def get_danger_category(wbt):
    if wbt < 28: return "🟢 Safe"
    elif 28 <= wbt < 30: return "🟡 Caution"
    elif 30 <= wbt < 32: return "🟠 Danger"
    else: return "🔴 LETHAL"

# --- MAIN ANALYSIS ---
print(f"📂 Loading {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# 1. Calculate Wet Bulb for EVERY row
print("🧮 Calculating Wet Bulb for 8,000+ hours...")
df['wet_bulb'] = df.apply(calculate_wet_bulb, axis=1)

# 2. Assign Danger Labels
df['status'] = df['wet_bulb'].apply(get_danger_category)

# 3. generate Summary Report
print("\n" + "="*40)
print("📊 YEARLY HEAT SAFETY REPORT: MUMBAI")
print("="*40)

# Count how many hours fell into each category
summary = df['status'].value_counts()
print(summary)

print("\n" + "-"*40)
print("🔥 TOP 5 MOST DANGEROUS HOURS LAST YEAR")
print("-"*40)

# Sort by hottest Wet Bulb and show top 5
dangerous_hours = df.sort_values(by='wet_bulb', ascending=False).head(5)
print(dangerous_hours[['datetime', 'temperature', 'humidity', 'wet_bulb', 'status']])

print("\n✅ Analysis Complete!")