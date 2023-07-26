from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
import requests
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

class ResortScreen(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location

        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        top_layout.add_widget(Label(text=self.location, halign='center', valign='middle'))
        self.add_widget(top_layout)

        # Two-column layout using GridLayout
        grid_layout = GridLayout(cols=2, size_hint=(1, 0.8))
        self.add_widget(grid_layout)

        # Left column for weather data
        left_layout = BoxLayout(orientation='vertical')
        self.weather_label = Label(text="Fetching weather data...")
        left_layout.add_widget(self.weather_label)
        grid_layout.add_widget(left_layout)

        # Right column (empty for now)
        grid_layout.add_widget(BoxLayout())

        self.fetch_weather_data()

        # Bottom row with "Back to Menu" button
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_button = Button(text="Back to Menu")
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)
        self.add_widget(bottom_layout)

    def fetch_weather_data(self):
        location_key = locations[self.location]

        # Fetch current weather data from AccuWeather using location key
        current_params = {
            "apikey": ACCUWEATHER_API_KEY,
            "details": True
        }

        try:
            current_response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}", params=current_params)
            current_data = current_response.json()

            if current_data and isinstance(current_data, list):
                weather_data = current_data[0]
                current_temp = weather_data.get("Temperature", {}).get("Imperial", {}).get("Value")
                current_condition = weather_data.get("WeatherText")

                location_data = f"{self.location}\n"
                location_data += f"Current Temperature: {current_temp}°F\n"
                location_data += f"Current Conditions: {current_condition}\n"
                self.weather_label.text = location_data
            else:
                self.weather_label.text = f"Weather data not available for {self.location}\n"
        except requests.exceptions.RequestException as e:
            self.weather_label.text = f"Failed to fetch weather data for {self.location}\n"
            print(f"Error: {e}")

    def switch_to_main_menu(self, button):
        app = App.get_running_app()
        app.root.current = 'Main Menu'

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create buttons for each resort
        for location, _ in locations.items():
            button = Button(text=location)
            button.bind(on_release=self.switch_to_resort_screen)
            self.add_widget(button)

    def switch_to_resort_screen(self, button):
        app = App.get_running_app()
        app.root.current = button.text

class SkiResortWeatherApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add the main menu screen
        main_menu_screen = Screen(name='Main Menu')
        main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(main_menu_screen)

        # Add resort-specific screens
        for location, _ in locations.items():
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager

if __name__ == '__main__':
    app = SkiResortWeatherApp()
    app.run()
