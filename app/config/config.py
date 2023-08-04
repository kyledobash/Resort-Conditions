# config.py

# Dictionary to map location names to their AccuWeather location keys and Twitter handles
resorts = {
    "Brighton": {
        "accuweather_key": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
        "twitter_handle": "brightonresort",
        "location": "Brighton,UT",
        "resort_slug": "brighton",
        "roadcams": [
            "http://www.udottraffic.utah.gov/AnimatedGifs/100033.gif",
            "https://udottraffic.utah.gov/1_devices/aux14605.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16212.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16213.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16215.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16216.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux18040.jpeg",
            "http://udottraffic.utah.gov/1_devices/SR-190%20MP%2015%2095%20SL.gif",
        ]
    },
    "Snowbird": {
        "accuweather_key": "101347_poi",         # Snowbird Ski Resort, Utah
        "twitter_handle": "snowbird",
        "location": "Snowbird,UT",
        "resort_slug": "snowbird",
        "roadcams": [
            "http://www.udottraffic.utah.gov/AnimatedGifs/100032.gif",
            "https://udottraffic.utah.gov/1_devices/aux14604.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16265.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16267.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16269.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux16270.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux17227.jpeg",
            "https://udottraffic.utah.gov/1_devices/aux17226.jpeg"
        ]
    },
    "Snowbasin": {
        "accuweather_key": "101346_poi",         # Snowbasin Ski Resort, Utah
        "twitter_handle": "snowbasinresort",
        "location": "Snowbasin,UT",
        "resort_slug": "snowbasin",
        "roadcams": [
            "http://udottraffic.utah.gov/1_devices/RWIS%20SR-167%20TrappersLoop.gif",
            "http://url-to-roadcam2.gif"
        ]
    }
}
