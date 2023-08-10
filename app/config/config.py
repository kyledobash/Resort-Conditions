# config.py

# Dictionary to map location names to their AccuWeather location keys and Twitter handles
resorts = {
    "Brighton": {
        "accuweather_key": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
        "twitter_handle": "brightonresort",
        "location": "Brighton,UT",
        "resort_slug": "brighton",
        "roadcam_webpage_url": "http://cottonwoodcanyons.udot.utah.gov/canyon-road-information/",
        "roadcam_img_src_urls": [
            "http://www.udottraffic.utah.gov/AnimatedGifs/100033.gif",
            "http://udottraffic.utah.gov/1_devices/aux14605.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16212.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16213.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16215.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16216.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux18040.jpeg",
            "http://udottraffic.utah.gov/1_devices/SR-190%20MP%2015%2095%20SL.gif",
        ],
        "has_youtube_live_feeds": True,
        "youtube_live_feed_urls": [
            "https://www.youtube.com/watch?v=iq-CT8UQzgo",
            "https://www.youtube.com/watch?v=YDyBL3bXOwA",
        ],
        "has_iframe_live_feeds": False,
        "iframe_live_feed_urls": [],
    },
    "Snowbird": {
        "accuweather_key": "101347_poi",         # Snowbird Ski Resort, Utah
        "twitter_handle": "snowbird",
        "location": "Snowbird,UT",
        "resort_slug": "snowbird",
        "roadcam_webpage_url": "http://cottonwoodcanyons.udot.utah.gov/canyon-road-information/",
        "roadcam_img_src_urls": [
            "http://www.udottraffic.utah.gov/AnimatedGifs/100032.gif",
            "http://udottraffic.utah.gov/1_devices/aux14604.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16265.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16267.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16269.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux16270.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux17227.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux17226.jpeg"
        ],
        "has_youtube_live_feeds": False,
        "youtube_live_feed_urls": [],
        "has_iframe_live_feeds": True,
        "iframe_live_feed_urls": [

        ],
    },
    "Snowbasin": {
        "accuweather_key": "101346_poi",         # Snowbasin Ski Resort, Utah
        "twitter_handle": "snowbasinresort",
        "location": "Snowbasin,UT",
        "resort_slug": "snowbasin",
        "roadcam_webpage_url": "http://udottraffic.utah.gov/",
        "roadcam_img_src_urls": [
            "http://udottraffic.utah.gov/1_devices/RWIS%20SR-167%20TrappersLoop.gif",
            "http://udottraffic.utah.gov/1_devices/SR-226-all.gif",
            "http://udottraffic.utah.gov/1_devices/I-84-mp-92.jpeg",
            "http://udottraffic.utah.gov/1_devices/aux17617.jpeg"
        ],
        "has_youtube_live_feeds": False,
        "youtube_live_feed_urls": [],
        "has_iframe_live_feeds": True,
        "iframe_live_feed_urls": [
            
        ],
    }
}
