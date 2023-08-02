from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
import os
import logging
from dotenv import load_dotenv

# Import necessary functions from app.utils.api.py
from app.utils.api import fetch_weather_data, fetch_forecast_data, fetch_traffic_info, fetch_historical_current_data
from app.config.config import resorts

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

class ResortScreen(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location

        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        resort_name_label = Label(text=f"[color=FFD700][b]{self.location}[/b][/color]", halign='center', valign='middle', markup=True)
        top_layout.add_widget(resort_name_label)
        self.add_widget(top_layout)

        # Two-column layout using GridLayout
        content_layout = GridLayout(cols=2, size_hint=(1, 0.8))
        scroll_view = ScrollView()
        scroll_view.add_widget(content_layout)
        self.add_widget(scroll_view)

        # Left column for weather data and forecast
        left_layout = BoxLayout(orientation='vertical')
        self.weather_label = Label(text="Fetching weather data...")
        left_layout.add_widget(self.weather_label)

        # New label for historical current data
        self.historical_data_label = Label(text="Fetching historical current data...")
        left_layout.add_widget(self.historical_data_label)

        self.forecast_label = Label(text="Fetching forecast data...", markup=True)
        left_layout.add_widget(self.forecast_label)

        content_layout.add_widget(left_layout)

        # Right column for Twitter embedded timeline
        right_layout = BoxLayout(orientation='vertical')
        # Right column for traffic info (added)
        self.traffic_info_label = Label(text="Fetching traffic info...")
        right_layout.add_widget(self.traffic_info_label)
        content_layout.add_widget(right_layout)

    def fetch_data(self):
        # Fetch all the required data for the specific resort (traffic info, historical current data, weather data, forecast data)
        self.fetch_traffic_info()
        self.fetch_historical_current_data()
        self.fetch_weather_data()
        self.fetch_forecast_data()

        # Bottom row with "Back to Menu" button (as before)
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_button = Button(text="Back to Menu")
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)
        self.add_widget(bottom_layout)

    def fetch_traffic_info(self):
        # Use the API method to fetch traffic info
        resort_location = resorts[self.location]["location"]
        user_location = os.getenv("PHYSICAL_ADDRESS")  # Use the PHYSICAL_ADDRESS from config.py as the user's location
        traffic_info = fetch_traffic_info(user_location, resort_location)
        self.traffic_info_label.text = traffic_info

    def fetch_historical_current_data(self):
        # Use the API method to fetch historical current data
        historical_current_data = fetch_historical_current_data(self.location)
        self.historical_data_label.text = historical_current_data

    def fetch_weather_data(self):
        # Use the API method to fetch weather data
        weather_data = fetch_weather_data(self.location)
        self.weather_label.text = weather_data

    def fetch_forecast_data(self):
        # Use the API method to fetch forecast data
        forecast_data = fetch_forecast_data(self.location)
        self.forecast_label.text = forecast_data

    def switch_to_main_menu(self):
        app = App.get_running_app()
        app.root.current = 'Main Menu'

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create buttons for each resort
        for location, _ in resorts.items():
            button = Button(text=location)
            button.bind(on_release=self.switch_to_resort_screen)
            button.resort_location = resorts[location]['location']
            self.add_widget(button)

    def switch_to_resort_screen(self, button):
        app = App.get_running_app()

        # Get the instance of ResortScreen from the ScreenManager
        resort_screen = app.root.get_screen(button.text).children[0]

        # Fetch the data for the specific resort screen
        resort_screen.fetch_data()

        # Switch to the specific resort screen
        app.root.current = button.text

class SkiResortWeatherApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add the main menu screen
        main_menu_screen = Screen(name='Main Menu')
        main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(main_menu_screen)

        # Add resort-specific screens
        for location, _ in resorts.items():
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager
    

if __name__ == '__main__':
    app = SkiResortWeatherApp()
    app.run()
