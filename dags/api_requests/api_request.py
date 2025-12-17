import requests
import json
import random

USE_LIVE_API = False 

API_KEY = "API_KEY"

def fetch_weather_data(city): 
    """
    Fungsi tunggal yang pintar memilih jalur:
    - Jika USE_LIVE_API = True  -> Tembak Weatherstack benaran.
    - Jika USE_LIVE_API = False -> Kembalikan data palsu (random).
    """
    
    if USE_LIVE_API:
        # --- JALUR ONLINE ---
        print(f"🌍 [LIVE] Request ke API Asli untuk: {city}...")
        try:
            url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error API: {e}")
            return None
    
    else:
        # --- JALUR OFFLINE (MOCK) ---
        print(f"🛠️ [MOCK] Generate data dummy untuk: {city}...")
        # Data palsu tapi strukturnya SAMA PERSIS dengan aslinya
        return {
            "request": {"type": "City", "query": f"{city}, Indonesia"},
            "location": {
                "name": city, 
                "country": "Indonesia", 
                "region": "Mock Region",
                "localtime": "2025-12-17 12:00",
                "utc_offset": "7.0"
            },
            "current": {
                "temperature": random.randint(20, 34), # Suhu acak
                "weather_descriptions": ["Partly Cloudy"],
                "wind_speed": random.randint(5, 20),
                "humidity": random.randint(60, 90),
                "feelslike": random.randint(22, 36)
            }
        }

# Block Test (Jalan kalau file ini di-run sendirian)
if __name__ == "__main__":
    print(fetch_weather_data("Jakarta"))