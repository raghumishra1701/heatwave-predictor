import math

def calculate_wet_bulb_temp(temp, humidity):
    """Calculates Wet Bulb Temperature using Stull's Formula."""
    # Stull's Formula (2011)
    tw = (temp * math.atan(0.151977 * (humidity + 8.313659)**0.5) +
          math.atan(temp + humidity) -
          math.atan(humidity - 1.676331) +
          0.00391838 * (humidity**1.5) * math.atan(0.023101 * humidity) -
          4.686035)
    return round(tw, 2)

def get_danger_level(wbt):
    """Returns the safety warning color and message."""
    if wbt < 28.0:
        return "🟢 SAFE", "Standard Conditions"
    elif 28.0 <= wbt < 30.0:
        return "🟡 CAUTION", "High Risk for Labor"
    elif 30.0 <= wbt < 32.0:
        return "🟠 DANGER", "Extreme Heat Stress"
    else:
        return "🔴 DEADLY", "LETHAL CONDITIONS"

# --- THE TEST SCENARIOS ---
scenarios = [
    {"name": "Mumbai Summer", "temp": 38, "hum": 70},
    {"name": "Delhi Heatwave", "temp": 45, "hum": 40},
    {"name": "Coastal Area",   "temp": 32, "hum": 90},
    {"name": "Pleasant Day",   "temp": 25, "hum": 50}
]

print(f"{'SCENARIO':<20} | {'TEMP':<5} | {'HUM':<4} | {'WET BULB':<10} | {'STATUS'}")
print("-" * 75)

for s in scenarios:
    wb = calculate_wet_bulb_temp(s["temp"], s["hum"])
    icon, status = get_danger_level(wb)
    
    # Print formatted row
    print(f"{s['name']:<20} | {s['temp']}°C | {s['hum']}%  | {wb}°C     | {icon} {status}")