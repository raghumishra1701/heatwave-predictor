import requests

def get_current_weather(lat, lon, api_key):
    """
    Fetches current temperature (Celsius) and humidity (%) 
    for a specific latitude/longitude.
    """
    # The URL for OpenWeatherMap's current weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        # Send the request to the internet
        response = requests.get(url)
        response.raise_for_status()  # Check for errors (like bad API key)
        
        # Convert the JSON response into a Python dictionary
        data = response.json()
        
        # Extract the specific numbers we need
        temp_c = data['main']['temp']       # Temperature in Celsius
        humidity = data['main']['humidity'] # Relative Humidity %
        location_name = data['name']        # The neighborhood/city name
        
        return temp_c, humidity, location_name

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None, None

# --- TEST AREA ---
if __name__ == "__main__":
    # 1. REPLACE THIS with your NEW generated key
    MY_API_KEY = "d589ccc13fbb0eb3dcc24373eb4afef7"
    
    # 2. Coordinates for a test location (e.g., Dharavi Slum, Mumbai)
    # You can find these on Google Maps by right-clicking a spot
    TEST_LAT = 19.0402
    TEST_LON = 72.8508
    
    print("Fetching weather data...")
    temp, hum, loc = get_current_weather(TEST_LAT, TEST_LON, MY_API_KEY)
    
    if temp is not None:
        print(f"----------------------------")
        print(f"Location: {loc}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {hum}%")
        print(f"----------------------------")
    else:
        print("Failed to get weather data.")