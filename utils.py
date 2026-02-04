import requests
import math

# --- 1. MATH: Calculate Wet Bulb ---
def calculate_wet_bulb(T, rh):
    """Calculates Wet Bulb Temperature using Stull's formula."""
    try:
        tw = (T * math.atan(0.151977 * (rh + 8.313659)**0.5) +
              math.atan(T + rh) -
              math.atan(rh - 1.676331) +
              0.00391838 * (rh**1.5) * math.atan(0.023101 * rh) -
              4.686035)
        return round(tw, 2)
    except:
        return 0

# --- 2. LOGIC: Safety Check ---
def get_danger_info(wbt):
    """Returns status, CSS class, and advice based on Wet Bulb Temp."""
    if wbt < 28:
        return "safe", "SAFE", "Standard Conditions. Drink water normally."
    elif 28 <= wbt < 30:
        return "caution", "CAUTION", "High Risk. Take frequent water breaks."
    elif 30 <= wbt < 32:
        return "danger", "DANGER", "Stop strenuous work. Seek shade immediately."
    else:
        return "lethal", "EXTREME DANGER", "LETHAL HEAT. STOP WORK & EVACUATE."

# --- 3. API: Fetch Weather ---
def get_weather(city_name, api_key):
    """Fetches current weather from OpenWeatherMap."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['main']['temp'], data['main']['humidity'], data['sys']['country']
    except Exception as e:
        print(f"API Error: {e}")
        return None, None, None