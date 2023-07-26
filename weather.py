import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

# Dictionary to map location names to their AccuWeather location keys
locations = {
    "Brighton": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
    "Snowbird": "101347_poi",         # Snowbird Ski Resort, Utah
    "Snowbasin": "101346_poi"         # Snowbasin Ski Resort, Utah
}

class SkiResortWeatherApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        # Create a label for the title
        title_label = Label(text="Ski Resort Weather", halign="center")
        main_layout.add_widget(title_label)

        # Create a scroll view to hold the weather data
        scroll_view = ScrollView()
        main_layout.add_widget(scroll_view)

        # Create a layout to hold the weather data labels
        weather_layout = BoxLayout(orientation="vertical", spacing=10, padding=(10, 10, 10, 10))
        scroll_view.add_widget(weather_layout)

        self.result_labels = {}  # Dictionary to hold the weather data labels

        for location, location_key in locations.items():
            label = Label(text="Fetching weather data...", halign="left")
            weather_layout.add_widget(label)
            self.result_labels[location] = label

        self.fetch_weather_data()
        return main_layout

    def fetch_weather_data(self):
        for location, location_key in locations.items():
            print(f"Fetching weather data for {location} (location key: {location_key})")

            # Fetch current weather data from AccuWeather using location key
            url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={ACCUWEATHER_API_KEY}"

            try:
                current_response = requests.get(url)
                current_data = current_response.json()

                if current_data and isinstance(current_data, list):
                    weather_data = current_data[0]
                    current_temp = weather_data.get("Temperature", {}).get("Imperial", {}).get("Value")
                    current_condition = weather_data.get("WeatherText")

                    location_data = f"{location}\n"
                    location_data += f"Current Temperature: {current_temp}°F\n"
                    location_data += f"Current Conditions: {current_condition}\n"
                    self.result_labels[location].text = location_data
                else:
                    self.result_labels[location].text = f"Weather data not available for {location}\n"
            except requests.exceptions.RequestException as e:
                self.result_labels[location].text = f"Failed to fetch weather data for {location}\n"
                print(f"Error: {e}")

# Run the application
if __name__ == "__main__":
    app = SkiResortWeatherApp()
    app.run()
