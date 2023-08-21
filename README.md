# Resort-Conditions 
 
Resort-Conditions is a simple app that provides information about local Utah ski resorts, including traffic, weather, conditions, camera feeds, and recent tweets. 
 
## Installation 

Before running the application, you need to sign up for the following API keys from their respective sites: 
 
- [AccuWeather API](https://www.accuweather.com) - Sign up to get an API key. 
- [Bing Maps API](https://www.bingmapsportal.com) - Sign up to get an API key. 
- [X Rapid API](https://www.x-rapidapi-key.com) - Sign up to get an API key. 
 
Once you have obtained the API keys, follow these steps: 
 
1. Ensure that all dependencies listed in the  requirements.txt  file are installed on your machine. 
 
2. Create a  .env  file in the project's root directory and add the following keys:

        ACCUWEATHER_API_KEY=
        BING_MAPS_API_KEY=
        X_RAPID_API_KEY=

    You need to sign up for each of these keys from their respective sites and then populate them in their appropriate places in the  .env  file. 
 
3. Run  main.py  to start the application.

## Features 
 
- Traffic status and travel time information. 
- Recent tweets related to the resorts. 
- UDOT roadcam live feed images for real-time views of road conditions. 
- Weather forecasts and conditions for the past, present, and future. 
- Lift status information to know which lifts are operational. 
 
## Technologies Used 
 
- Python 
- Kivy 
- Bing Maps API 
- Various X Rapid APIs for Twitter and ski lift conditions 
 
## License 
 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 