import requests
import sys

def get_weather_safe(city_name, api_key):
    # 1. Setup the URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    try:
        print(f"Attempting to fetch weather for {city_name}...")
        
        # 2. Make the Request (with a timeout!)
        # 'timeout=5' stops the code from freezing forever if the server is slow.
        response = requests.get(url, params=params, timeout=10)
        
        # 3. Check for HTTP Errors (4xx or 5xx)
        # This line forces Python to jump to the 'except HTTPError' block 
        # if the status code is bad (like 404 or 401).
        response.raise_for_status()
        
        # 4. If we get here, the request was successful!
        data = response.json()
        return data['main']['temp'], data['main']['humidity']

    # --- ERROR HANDLING BLOCKS ---
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: No Internet Connection.")
        print("   -> Please check your WiFi or data connection.")

    except requests.exceptions.Timeout:
        print("❌ Error: Request Timed Out.")
        print("   -> The server took too long to respond. Try again later.")

    except requests.exceptions.HTTPError as http_err:
        # We catch the error, but we need to check WHICH code it is to be helpful.
        status = response.status_code
        
        if status == 401:
            print("❌ Error: Authorization Failed (401).")
            print("   -> Your API Key is invalid or not active yet.")
        elif status == 404:
            print(f"❌ Error: City Not Found (404).")
            print(f"   -> Check the spelling of '{city_name}'.")
        elif status == 429:
            print("❌ Error: Rate Limit Exceeded (429).")
            print("   -> You have made too many requests. Wait a while.")
        elif status >= 500:
            print("❌ Error: Server Error.")
            print("   -> OpenWeatherMap is having issues. Try again later.")
        else:
            print(f"❌ Error: Something went wrong ({http_err})")

    except requests.exceptions.RequestException as e:
        # This catches ANY other request-related error we missed above
        print(f"❌ Error: An unexpected error occurred: {e}")

    except KeyError:
        # This happens if the data structure changes (e.g., 'main' is missing)
        print("❌ Error: Unexpected Data Format.")
        print("   -> The API response didn't look like we expected.")

    return None, None

# --- TEST ZONE ---
if __name__ == "__main__":
    # Replace with your key to test
    MY_KEY = "d589ccc13fbb0eb3dcc24373eb4afef7"
    
    # Test 1: Valid City
    temp, hum = get_weather_safe("Mumbai", MY_KEY)
    if temp:
        print(f"✅ Success! It is {temp}°C in Mumbai.")
    
    print("-" * 30)
    
    # Test 2: Invalid City (Triggers 404)
    get_weather_safe("Atlantis_Fake_City", MY_KEY)