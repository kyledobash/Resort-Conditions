import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def fetch_traffic_info():
    # Fetch traffic info from the user's current location to each resort using the Bing Maps API
    bing_maps_api_key = os.getenv("BING_MAPS_API_KEY")
    physical_address = os.getenv("PHYSICAL_ADDRESS")

    # Assuming the PHYSICAL_ADDRESS is a string containing the user's location
    user_location = physical_address

    for resort, resort_data in resorts.items():
        # Get the resort's address from the resorts dictionary
        resort_address = resort_data.get("address")

        # Skip resorts without address information
        if resort_address is None:
            continue

        # Create the route URL with the provided start and end points, and API key
        route_url = f"http://dev.virtualearth.net/REST/V1/Routes/Driving"

        try:
            params = {
                "wp.0": user_location,
                "wp.1": resort_address,
                "avoid": "minimizeTolls",
                "key": bing_maps_api_key,
            }
            response = requests.get(route_url, params=params)
            route_data = response.json()

            if "resourceSets" in route_data and route_data["resourceSets"]:
                # Extract traffic info here, e.g., estimated travel time, road conditions, etc.
                travel_time_minutes = route_data["resourceSets"][0]["resources"][0]["travelDurationTraffic"] // 60
                road_conditions = route_data["resourceSets"][0]["resources"][0]["trafficCongestion"]

                # Display the traffic info for the specific resort
                print(f"Resort: {resort}")
                print(f"Estimated Travel Time: {travel_time_minutes} minutes")
                print(f"Road Conditions: {road_conditions.capitalize()}")
                print()
            else:
                print(f"No route data found for {resort} using Bing Maps API.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching traffic data for {resort}: {e}")


if __name__ == '__main__':
    # Your resorts dictionary here
    resorts = {
        "Brighton": {
            "address": "Brighton, UT"
        },
        "Snowbird": {
            "address": "Snowbird, UT"
        },
        "Snowbasin": {
            "address": "Snowbasin, UT"
        }
    }

    fetch_traffic_info()
