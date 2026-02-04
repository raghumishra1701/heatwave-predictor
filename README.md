# 🔥 Heatwave Predictor: Safety for Outdoor Workers

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-green)
![Twilio](https://img.shields.io/badge/Twilio-SMS-red)
![Status](https://img.shields.io/badge/Status-Live-success)

**A life-saving tool that calculates Wet Bulb Temperature (WBT) to predict heatstroke risks for construction workers and sends instant SMS alerts.**

---

## 🚀 Live Demo
**Try the App here:** 👉 [https://heatwave-predictor.onrender.com](https://heatwave-predictor.onrender.com)

---

## 🧐 The Problem
Standard weather apps only show "Temperature" (e.g., 35°C). They ignore **Humidity**, which is the real killer.
* High Heat + High Humidity = **Wet Bulb Temperature (WBT)**.
* When WBT exceeds 32°C, sweat cannot evaporate, leading to fatal heatstrokes.
* Workers often don't know when to stop working until it's too late.

## 💡 The Solution
The **Heatwave Predictor** is a smart dashboard that:
1.  **Calculates Real-Time Risk:** Uses a specialized algorithm to combine Temp & Humidity into WBT.
2.  **Predicts the Future:** Shows a 6-hour safety forecast so site managers can plan shifts.
3.  **Sends SOS Alerts:** Integrates with **Twilio** to send SMS warnings directly to workers' phones when conditions become "Lethal."

---

## 📸 Screenshots

| **Dashboard Analysis** |
|:----------------------:|
| ![Dashboard]<img width="958" height="955" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/30babfd9-c93c-4a29-a02d-d123f08ff668" /> |
*(Note: Upload your screenshots to the repo to see them here)*

---

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, JavaScript (Mobile Responsive)
* **APIs:**
    * OpenWeatherMap (Real-time weather data)
    * Twilio (SMS Alerts)
* **Deployment:** Render (Cloud Hosting)

---

## ⚙️ Installation & Local Setup
Want to run this on your own machine? Follow these steps:





### 1. Clone the Repository
```bash
git clone https://github.com/raghumishra1701/heatwave-predictor.git

cd heatwave-predictor

