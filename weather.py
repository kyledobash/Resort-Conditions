from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
import requests
import os
import logging
import datetime
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

# Dictionary to map location names to their AccuWeather location keys and Twitter handles
resorts = {
    "Brighton": {
        "accuweather_key": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
        "twitter_handle": "brightonresort",
        "location": "Brighton,UT"
    },
    "Snowbird": {
        "accuweather_key": "101347_poi",         # Snowbird Ski Resort, Utah
        "twitter_handle": "snowbird",
        "location": "Snowbird,UT"
    },
    "Snowbasin": {
        "accuweather_key": "101346_poi",         # Snowbasin Ski Resort, Utah
        "twitter_handle": "snowbasinresort",
        "location": "Snowbasin,UT"
    }
}

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

        # # Two-column layout using GridLayout
        # content_layout = GridLayout(cols=2, size_hint=(1, 0.8))
        # self.add_widget(content_layout)

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

        # Fetch traffic info for the specific resort (added)
        self.fetch_traffic_info()

        # Fetch both current conditions and 1-day daily forecasts (as before)
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
        # Fetch traffic info from the user's current location to the specific resort using the Bing Maps API
        bing_maps_api_key = os.getenv("BING_MAPS_API_KEY")
        physical_address = os.getenv("PHYSICAL_ADDRESS")

        # Assuming the PHYSICAL_ADDRESS is a string containing the user's location
        user_location = physical_address
        resort_data = resorts[self.location]

        # Get the resort's location from the resorts dictionary
        resort_location = resort_data.get("location")

        if resort_location is None:
            self.traffic_info_label.text = f"No address data found for {self.location}."
            return

        # Create the route URL with the provided start and end points, and API key
        route_url = "http://dev.virtualearth.net/REST/V1/Routes/Driving"

        try:
            params = {
                "wp.0": user_location,
                "wp.1": resort_location,
                "avoid": "minimizeTolls",
                "key": bing_maps_api_key,
                "incidents": True  # Include traffic incidents in the response
            }
            response = requests.get(route_url, params=params)
            route_data = response.json()

            if "resourceSets" in route_data and route_data["resourceSets"]:
                # Extract traffic info here, e.g., estimated travel time, road conditions, etc.
                travel_time_minutes = route_data["resourceSets"][0]["resources"][0]["travelDurationTraffic"] // 60
                road_conditions = route_data["resourceSets"][0]["resources"][0]["trafficCongestion"]

                # Check for traffic incidents along the route
                if "trafficIncidents" in route_data["resourceSets"][0]["resources"][0]:
                    incidents = route_data["resourceSets"][0]["resources"][0]["trafficIncidents"]
                    
                    # Process and display the incidents data
                    incidents_info_str = "Traffic Incidents:\n"
                    for incident in incidents:
                        incident_type = incident.get("type", "Unknown")
                        description = incident.get("description", "No description")
                        start = incident.get("start", "Unknown")
                        end = incident.get("end", "Unknown")
                        incidents_info_str += f"Incident Type: {incident_type}\n"
                        incidents_info_str += f"Description: {description}\n"
                        incidents_info_str += f"Start Time: {start}\n"
                        incidents_info_str += f"End Time: {end}\n"
                        incidents_info_str += "\n"
                else:
                    incidents_info_str = "No traffic incidents found along the route.\n"

                # Display the traffic info for the specific resort, including any incidents
                traffic_info_str = f"Travel Time to {self.location}: {travel_time_minutes} minutes\n"
                traffic_info_str += f"Road Conditions: {road_conditions.capitalize()}\n"
                traffic_info_str += incidents_info_str
                self.traffic_info_label.text = traffic_info_str
            else:
                self.traffic_info_label.text = f"No route data found for {self.location} using Bing Maps API."
        except requests.exceptions.RequestException as e:
            self.traffic_info_label.text = f"Error fetching traffic data for {self.location}: {e}"


    def fetch_historical_current_data(self):
        location_key = resorts[self.location]["accuweather_key"]

        # Fetch historical current conditions for the past 24 hours from AccuWeather using location key
        historical_current_params = {
            "apikey": ACCUWEATHER_API_KEY,
            "details": True,
            "metric": False,  # Use Fahrenheit for temperature values
            "hours": "24",    # Get historical current conditions for the past 24 hours
        }

        try:
            historical_current_response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}/historical/24", params=historical_current_params)
            historical_current_data = historical_current_response.json()

            if historical_current_data and isinstance(historical_current_data, list):
                # Extract and format historical current conditions data for display
                historical_current_data_str = "Historical Current Conditions (Past 24 Hours):\n"
                for data in historical_current_data:
                    time_str = data.get("LocalObservationDateTime")
                    time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
                    hour_str = time.strftime("%H:%M")  # Extract hour part from time
                    temp = data.get("Temperature", {}).get("Imperial", {}).get("Value")
                    condition = data.get("WeatherText")
                    historical_current_data_str += f"{hour_str} - Temp: {temp}°F - Condition: {condition}\n"
            else:
                historical_current_data_str = f"Historical current conditions data not available for the past 24 hours in {self.location}\n"

            # Display historical current conditions data
            self.historical_data_label.text = historical_current_data_str
        except requests.exceptions.RequestException as e:
            self.weather_label.text = f"Failed to fetch historical current conditions data for {self.location}\n"
            logging.error(f"Error fetching historical current conditions data for {self.location}: {e}")

    def fetch_weather_data(self):
        location_key = resorts[self.location]["accuweather_key"]

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

                # Extract weather data
                current_temp = weather_data.get("Temperature", {}).get("Imperial", {}).get("Value")
                current_condition = weather_data.get("WeatherText")
                humidity = weather_data.get("RelativeHumidity")
                wind_speed = weather_data.get("Wind", {}).get("Speed", {}).get("Imperial", {}).get("Value")
                visibility = weather_data.get("Visibility", {}).get("Imperial", {}).get("Value")

                # Format current weather data for display
                location_data = f"Current Conditions\n"
                location_data += f"Temperature: {current_temp}°F\n"
                location_data += f"Conditions: {current_condition}\n"
                location_data += f"Humidity: {humidity}%\n"
                location_data += f"Wind Speed: {wind_speed} mph\n"
                location_data += f"Visibility: {visibility} miles\n"

                # Display the current weather data
                self.weather_label.text = location_data
            else:
                self.weather_label.text = f"Weather data not available for {self.location}\n"
        except requests.exceptions.RequestException as e:
            self.weather_label.text = f"Failed to fetch weather data for {self.location}\n"
            logging.error(f"Error fetching weather data for {self.location}: {e}")

    def fetch_forecast_data(self):
        location_key = resorts[self.location]["accuweather_key"]

        # Fetch 1-day daily forecast from AccuWeather using location key
        daily_forecast_params = {
            "apikey": ACCUWEATHER_API_KEY,
            "details": True,
        }

        try:
            daily_forecast_response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}", params=daily_forecast_params)
            daily_forecast_data = daily_forecast_response.json()

            if "DailyForecasts" in daily_forecast_data:
                daily_forecast_data = daily_forecast_data["DailyForecasts"][0]

                # Extract daily forecast data
                forecast_temp_min = daily_forecast_data.get("Temperature", {}).get("Minimum", {}).get("Value")
                forecast_temp_max = daily_forecast_data.get("Temperature", {}).get("Maximum", {}).get("Value")
                forecast_day_condition = daily_forecast_data.get("Day", {}).get("IconPhrase")

                # Format daily forecast data for display
                # forecast_data_str = f"Forecast for {daily_forecast_data['Date']}\n"
                forecast_data_str = f"Temperature Min: {forecast_temp_min}°F\n"
                forecast_data_str += f"Temperature Max: {forecast_temp_max}°F\n"
                forecast_data_str += f"Day Conditions: {forecast_day_condition}\n"
            else:
                forecast_data_str = f"Daily forecast data not available for {self.location}\n"

            # Fetch hourly forecast from AccuWeather using location key
            hourly_forecast_params = {
                "apikey": ACCUWEATHER_API_KEY,
                "details": True,
                "metric": False,  # Use Fahrenheit for temperature values
                "hours": "12",    # Get hourly forecasts for the next 24 hours
            }

            hourly_forecast_response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}", params=hourly_forecast_params)
            hourly_forecast_data = hourly_forecast_response.json()

            if hourly_forecast_data and isinstance(hourly_forecast_data, list):
                # Extract and format hourly forecast data for display
                hourly_data_str = "Hourly Forecast:\n"
                for hour in hourly_forecast_data[:5]:
                    time_str = hour.get("DateTime")
                    time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
                    hour_str = time.strftime("%H:%M")  # Extract hour part from time
                    temp = hour.get("Temperature", {}).get("Value")
                    condition = hour.get("IconPhrase")
                    hourly_data_str += f"{hour_str} - Temp: {temp}°F - Condition: {condition}\n"
            else:
                hourly_data_str = f"Hourly forecast data not available for {self.location}\n"

            # Display both daily and hourly forecast data
            self.forecast_label.text = forecast_data_str + "\n" + hourly_data_str
        except requests.exceptions.RequestException as e:
            self.forecast_label.text = f"Error fetching forecast data for {self.location}\n"
            logging.error(f"Error fetching forecast data for {self.location}: {e}")


    def switch_to_main_menu(self, button):
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
        for location, _ in resorts.items():
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager
    

if __name__ == '__main__':
    app = SkiResortWeatherApp()
    app.run()
