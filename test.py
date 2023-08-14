import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('SKI_API_KEY')

# Set the API endpoint URL
url = "https://twitter135.p.rapidapi.com/v2/UserTweets/"

# Set the headers with the API key
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
}

# Set the parameters for the request
params = {
    "id": "18431196",  # Replace with the User ID of the Twitter account
    "count": 10
}

# Make the request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    # Print the error message
    print("Error:", response.status_code, response.text)