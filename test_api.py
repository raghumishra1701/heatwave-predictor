import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_endpoint(endpoint, city):
    print(f"\n🚀 TESTING: {endpoint} for {city}...")
    try:
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, params={"city": city})
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(response.text)     
    except Exception as e:
        print(f"❌ ERROR: Is app.py running? ({e})")

if __name__ == "__main__":
    test_endpoint("current", "Mumbai")
    test_endpoint("safety", "London")
    test_endpoint("predict", "Delhi")