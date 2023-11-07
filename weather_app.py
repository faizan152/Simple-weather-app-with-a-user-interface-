import requests
import tkinter as tk
import threading
from encryption import generate_key, encrypt_api_key, decrypt_api_key

# Function to get the API key securely
def get_api_key(encrypted_api_key, secret_key):
    # Check if the API key is already decrypted
    if 'api_key' in locals():
        return api_key

    # If not, generate the secret key and decrypt the API key
    api_key = decrypt_api_key(encrypted_api_key, secret_key)

    return api_key

# Generate a secret key (store this securely)
secret_key = generate_key()

# Encrypt your API key using the secret_key
api_key = ""  # Replace with your actual API key
encrypted_api_key = encrypt_api_key(api_key, secret_key)

API_KEY = get_api_key(encrypted_api_key, secret_key)  # Retrieve the decrypted API key

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Tkinter GUI setup
root = tk.Tk()
root.title("Weather App")

root.geometry("800x600")

label = tk.Label(root, text="Enter a city name:")
label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

weather_label = tk.Label(root, text="...")
weather_label.pack()

def fetch_weather():
    city = city_entry.get()

    def fetch_weather_thread():
        print(f"Fetching weather for {city}...")  # Debugging output
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            weather = data['weather'][0]['description']
            weather_data = f"Weather in {city}: {weather}\nTemperature: {temperature}°F"
        else:
            weather_data = "Error: Unable to retrieve weather data."
        print(f"Received weather data: {weather_data}")  # Debugging output
        weather_label.config(text=weather_data)

    # Start a new thread for fetching weather
    weather_thread = threading.Thread(target=fetch_weather_thread)
    weather_thread.start()

fetch_button = tk.Button(root, text="Fetch Weather", command=fetch_weather)
fetch_button.pack()

root.mainloop()

