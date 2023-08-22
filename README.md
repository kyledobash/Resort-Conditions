# Resort-Conditions

Resort-Conditions is a simple and efficient app designed to provide you with all the information you need for a successful day on the slopes. No need to check 5 or 6 different apps or websites – all the information you need is conveniently consolidated in one place.

Resort-Conditions displays essential details about local Utah ski resorts, including traffic updates, weather forecasts, current conditions, camera feeds, and recent tweets, to ensure you are prepared to make it to the mountain and back safely.

Simplify your pre-snowboarding routine and save time with Resort-Conditions. Get the information you need quickly and easily, so you can focus on enjoying your time on the mountain.

## Installation

Before running the application, make sure you have set up a Python virtual environment and installed the necessary dependencies. Here's how:

1. Set up a Python virtual environment by running the following command:

    (skip this step if your machine already has a python virtual environment)

    shell 
    python3 -m venv env

2. Activate the virtual environment. The command will vary depending on your operating system:

    - For Windows:

    shell 
        env\Scripts\activate

    - For macOS and Linux:

    shell 
        source env/bin/activate

3. Install the required dependencies by running the following command:

    shell 
        pip install -r requirements.txt

4. Create a `.env` file in the project's root directory and add the following keys:

    ACCUWEATHER_API_KEY= 
    BING_MAPS_API_KEY= 
    X_RAPID_API_KEY=

    You need to sign up for each of these keys from their respective sites and then populate them in their appropriate places in the `.env` file.

    - [AccuWeather API](https://developer.accuweather.com/) - Sign up to get an API key. 
    - [Bing Maps API](https://www.bingmapsportal.com) - Sign up to get an API key. 
    - [X Rapid API](https://rapidapi.com/) - Sign up to get an API key. 

    After signing up for the X Rapid API key, you also need to subscribe to the following RapidAPI APIs on the RapidAPI web portal: 
 
    - [Ski Resorts and Conditions API](https://rapidapi.com/random-shapes-random-shapes-default/api/ski-resorts-and-conditions/) - Subscribe to this API to ensure requests with your RapidAPI key will work. 
    - [Twitter API](https://rapidapi.com/Glavier/api/twitter135/) - Subscribe to this API to ensure requests with your RapidAPI key will work. 
    
    By subscribing to these RapidAPI APIs, you will have access to the necessary endpoints for ski resort information and Twitter data. 

5. Run `main.py` to start the application.

## Features

- Traffic status and travel time information.
- Recent tweets related to the resorts.
- UDOT roadcam live feed images for real-time views of road conditions.
- Weather forecasts and conditions for the past, present, and future.
- Lift status information to know which lifts are operational.
- Snow conditions/Base Measurements.

## Technologies Used

- Python
- Kivy
- geolocation
- Bing Maps API
- AccuWeather API
- [twitter135 X Rapid API](https://rapidapi.com/Glavier/api/twitter135)
- [ski-resorts-and-conditions X Rapid API](https://rapidapi.com/random-shapes-random-shapes-default/api/ski-resorts-and-conditions/)

## Main Menu

![Main Menu](app/images/main_menu.gif)

This GIF showcases the main menu of the Resort-Conditions app.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.