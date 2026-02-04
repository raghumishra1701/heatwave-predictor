import requests
import math

# --- CONFIGURATION ---
# Replace this with your working key!
API_KEY = "d589ccc13fbb0eb3dcc24373eb4afef7"

def get_weather(city_name):
    """Fetches Temp (C) and Humidity (%) safely."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['main']['temp'], data['main']['humidity']
    except Exception as e:
        print(f"❌ Error fetching data for {city_name}: {e}")
        return None, None

def calculate_wet_bulb_temp(temp, humidity):
    """
    Calculates Wet Bulb Temperature using Stull's Formula.
    """
    tw = (temp * math.atan(0.151977 * (humidity + 8.313659)**0.5) +
          math.atan(temp + humidity) -
          math.atan(humidity - 1.676331) +
          0.00391838 * (humidity**1.5) * math.atan(0.023101 * humidity) -
          4.686035)
          
    return round(tw, 2)

def get_danger_level(wbt):
    """
    Determines safety level based on physiological limits.
    Returns: (Icon, Status Label, Actionable Advice)
    """
    if wbt < 28.0:
        return (
            "🟢 SAFE", 
            "Standard Conditions", 
            "Drink water normally."
        )
    elif 28.0 <= wbt < 30.0:
        return (
            "🟡 CAUTION", 
            "High Risk for Labor", 
            "Take water breaks every 30 mins."
        )
    elif 30.0 <= wbt < 32.0:
        return (
            "🟠 DANGER", 
            "Extreme Heat Stress", 
            "STOP strenuous work. Find shade."
        )
    else:  # wbt >= 32.0
        return (
            "🔴 DEADLY", 
            "LETHAL CONDITIONS", 
            "EVACUATE SITE IMMEDIATELY."
        )

# --- MAIN APP LOOP ---
if __name__ == "__main__":
    print("--- 🏗️  CONSTRUCTION SITE HEAT PREDICTOR  🏗️ ---")
    
    cities_to_check = ["Mumbai", "Delhi", "Chennai", "Kolkata"]
    
    for city in cities_to_check:
        print(f"\nAnalyzing {city}...")
        
        # 1. Get Live Data
        temp, humidity = get_weather(city)
        
        if temp is not None:
            # 2. Calculate Wet Bulb
            wbt = calculate_wet_bulb_temp(temp, humidity)
            
            # 3. Get Warning (Now unpacking 3 items instead of 2!)
            icon, status, advice = get_danger_level(wbt)
            
            # 4. Print Report
            print(f"   Temp: {temp}°C  |  Humidity: {humidity}%")
            print(f"   🌊 Wet Bulb Temp: {wbt}°C")
            print(f"   ⚠️  STATUS: {icon} ({status})")
            print(f"   📢 ADVICE: {advice}")
            