import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv  # <--- NEW IMPORT

# 1. Load the secrets from the .env file
load_dotenv()

from utils import get_weather, calculate_wet_bulb, get_danger_info

app = Flask(__name__)
CORS(app)

# 2. Get the keys securely
API_KEY = os.getenv("WEATHER_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

# --- HELPER: SEND SMS ---
def send_sms_alert(to_number, city, wbt):
    try:
        # Check if keys exist before trying
        if not TWILIO_SID or not TWILIO_TOKEN:
            return "❌ Error: Twilio keys are missing in .env file!"

        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        msg_body = f"🔥 HEATWAVE ALERT: {city} is at {wbt}°C Wet Bulb Temp. DANGEROUS conditions. Seek shade."
        
        message = client.messages.create(
            body=msg_body,
            from_=TWILIO_PHONE,
            to=to_number
        )
        return f"✅ SMS Sent successfully to {to_number}!"
    except Exception as e:
        print(f"Twilio Error: {e}")
        return f"❌ SMS Failed. (Check server logs)"

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/current', methods=['GET'])
def api_current():
    city = request.args.get('city')
    temp, humidity, country = get_weather(city, API_KEY)
    if temp is None: return jsonify({"error": "City not found"}), 404
    return jsonify({"location": f"{city.upper()}, {country}", "temperature": temp, "humidity": humidity})

@app.route('/api/safety', methods=['GET'])
def api_safety():
    city = request.args.get('city')
    temp, humidity, _ = get_weather(city, API_KEY)
    if temp is None: return jsonify({"error": "City not found"}), 404
    wbt = calculate_wet_bulb(temp, humidity)
    css, status, advice = get_danger_info(wbt)
    return jsonify({"wet_bulb": wbt, "status": status, "advice": advice, "color_code": css})

@app.route('/api/predict', methods=['GET'])
def api_predict():
    city = request.args.get('city')
    temp, humidity, _ = get_weather(city, API_KEY)
    if temp is None: return jsonify({"error": "City not found"}), 404
    
    current_wbt = calculate_wet_bulb(temp, humidity)
    forecast = []
    simulated_wbt = current_wbt
    current_time = datetime.now()

    # Generate 6-Hour Forecast
    for i in range(1, 7):
        future_time = current_time + timedelta(hours=i)
        hour = future_time.hour
        
        if 6 <= hour < 14: change = 0.5
        elif 14 <= hour < 17: change = 0.1
        else: change = -0.3
            
        simulated_wbt += change
        css, status, _ = get_danger_info(simulated_wbt)

        forecast.append({
            "timestamp": future_time.strftime("%I:%M %p"),
            "predicted_wbt": round(simulated_wbt, 2),
            "safety_status": status,
            "css": css
        })

    return jsonify({"city": city, "forecast_12h": forecast})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    phone = data.get('phone')
    city = data.get('city')
    
    temp, humidity, _ = get_weather(city, API_KEY)
    if not temp: return jsonify({"message": "City not found."})
    
    wbt = calculate_wet_bulb(temp, humidity)
    
    # FOR DEMO: Force SMS if wbt > 20
    if wbt > 20: 
        result = send_sms_alert(phone, city, wbt)
    else:
        result = "Condition is Safe. No SMS needed."
        
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)