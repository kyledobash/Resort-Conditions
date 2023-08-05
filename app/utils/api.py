# app/utils/api.py
import os
import requests
import datetime
from PIL import Image
from io import BytesIO


def fetch_traffic_info(user_location, resort_location):
    # Fetch traffic info from the user's current location to the specific resort using the Bing Maps API
    bing_maps_api_key = os.getenv("BING_MAPS_API_KEY")

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
            traffic_info_str = f"Travel Time to {resort_location}: {travel_time_minutes} minutes\n"
            traffic_info_str += f"Road Conditions: {road_conditions.capitalize()}\n"
            traffic_info_str += incidents_info_str
            return traffic_info_str
        else:
            return f"No route data found for {resort_location} using Bing Maps API."
    except requests.exceptions.RequestException as e:
        return f"Error fetching traffic data for {resort_location}: {e}"

def fetch_historical_current_data(location_key):
    # Fetch historical current conditions for the past 24 hours from AccuWeather using location key
    ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

    historical_current_params = {
        "apikey": ACCUWEATHER_API_KEY,
        "details": True,
        "metric": False,
        "hours": "24",
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
                formatted_time = time.strftime("%b %d %H:%M")  # Format: Month Day Hour:Minute
                temp = data.get("Temperature", {}).get("Imperial", {}).get("Value")
                condition = data.get("WeatherText")
                historical_current_data_str += f"{formatted_time} - Temp: {temp}°F - Condition: {condition}\n"
            return historical_current_data_str
        else:
            return f"Historical current conditions data not available for the past 24 hours in {location_key}"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch historical current conditions data for {location_key}: {e}"

def fetch_weather_data(location_key):
    # Fetch current weather data from AccuWeather using location key
    ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

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
            return location_data
        else:
            return f"Weather data not available for {location_key}"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch weather data for {location_key}: {e}"

def fetch_forecast_data(location_key):
    # Fetch 1-day daily forecast from AccuWeather using location key
    ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

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
            forecast_data_str = f"Temperature Min: {forecast_temp_min}°F\n"
            forecast_data_str += f"Temperature Max: {forecast_temp_max}°F\n"
            forecast_data_str += f"Day Conditions: {forecast_day_condition}\n"
            return forecast_data_str
        else:
            return f"Daily forecast data not available for {location_key}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching forecast data for {location_key}: {e}"
    
def fetch_hourly_forecast_data(location_key):
    # Fetch next 12-hour hourly forecast from AccuWeather using location key
    ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

    hourly_forecast_params = {
        "apikey": ACCUWEATHER_API_KEY,
        "details": True,
    }

    try:
        hourly_forecast_response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}", params=hourly_forecast_params)
        hourly_forecast_data = hourly_forecast_response.json()

        if isinstance(hourly_forecast_data, list) and len(hourly_forecast_data) >= 5:
            # Extract and format the next 5 hourly forecast data for display
            forecast_data_str = "Next 5-hour Hourly Forecast:\n"
            for i in range(5):
                data = hourly_forecast_data[i]
                time_str = data.get("DateTime")
                time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
                hour_str = time.strftime("%H:%M")  # Extract hour part from time
                temp = data.get("Temperature", {}).get("Value")
                condition = data.get("IconPhrase")
                forecast_data_str += f"{hour_str} - Temp: {temp}°F - Condition: {condition}\n"
            return forecast_data_str
        else:
            return f"Hourly forecast data not available for {location_key}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching hourly forecast data for {location_key}: {e}"

def fetch_resort_data(resort_slug):
    # Fetch resort data from X Rapid Ski API using the given resort_slug
    RAPIDAPI_KEY = os.getenv("SKI_API_KEY")

    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'ski-resorts-and-conditions.p.rapidapi.com'
    }

    url = f'https://ski-resorts-and-conditions.p.rapidapi.com/v1/resort/{resort_slug}'

    try:
        response = requests.get(url, headers=headers)
        resort_data = response.json()

        if 'data' in resort_data:
            return resort_data['data']
        else:
            return None  # Resort data not available
    except requests.exceptions.RequestException:
        return None  # Error fetching resort data
    
def fetch_roadcam_images(resort_name, roadcams):
    print(f"Fetching roadcam images for {resort_name}...")
    
    for idx, roadcam_url in enumerate(roadcams, start=1):
        response = requests.get(roadcam_url)
        
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            
            image_filename = f"{resort_name.lower()}_roadcam_{idx}.jpg"
            image_path = os.path.join("roadcam_images", image_filename)
            image.save(image_path)
            print(f"  Roadcam {idx} image saved: {image_path}")
        else:
            print(f"  Error fetching roadcam {idx} image")
