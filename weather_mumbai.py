import requests  # Import the library that lets us "talk" to the internet
import config    # Import the separate file we just created with the key

# --- SETUP ---
# Coordinates for Mumbai (using Lat/Lon is more accurate than just "Mumbai")
LAT = 19.0760
LON = 72.8777

# We access the key securely from the config file, not by typing it here.
# If you share this code, you only share this file, not the config.py file!
api_key = config.API_KEY

def fetch_mumbai_weather():
    # 1. Define the URL
    # We use f-strings (f"...") to insert our variables into the web address
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={api_key}&units=metric"
    
    try:
        # 2. Make the Request
        # We ask the server: "GET me the data for this URL"
        print("Connecting to OpenWeatherMap...")
        response = requests.get(url)
        
        # 3. Check for Errors
        # If the server sends back a "404" (Not Found) or "401" (Unauthorized), this stops the code.
        response.raise_for_status()
        
        # 4. Parse the JSON
        # The server sends back a text string that looks like a dictionary. 
        # .json() converts it into a real Python dictionary we can use.
        data = response.json()
        
        # 5. Extract the Data
        # The data is nested. We look inside the 'main' box to find temp and humidity.
        # JSON Structure: { "main": { "temp": 32.5, "humidity": 80 }, ... }
        current_temp = data['main']['temp']
        current_humidity = data['main']['humidity']
        city_name = data['name']
        
        # 6. Display Results
        print("\n--- WEATHER REPORT ---")
        print(f"Location: {city_name}")
        print(f"Temperature: {current_temp}°C")
        print(f"Humidity:    {current_humidity}%")
        print("----------------------")
        
        return current_temp, current_humidity

    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error: {err}") 
        # This usually happens if your API Key is wrong or not active yet.
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Check your internet connection.")
        
    except KeyError:
        print("❌ Data Error: The format of the data changed or fields are missing.")

# --- RUN THE CODE ---
if __name__ == "__main__":
    fetch_mumbai_weather()