# fantasy_api.py
import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()
LEAGUE_ID = os.getenv('FANTASY_LEAGUE_ID')
YEAR = os.getenv('FANTASY_YEAR')
API_KEY = os.getenv('FANTASY_API_KEY')
TYPE = 'league'

# Make a really gross URL string
BASE_URL = "https://www47.myfantasyleague.com/" + YEAR + "/export?TYPE=" + TYPE + "&L=" + LEAGUE_ID + "&APIKEY=" + API_KEY + "&JSON=1"


# Get Teams
def get_league():
    franchise_array = []
    try:
        response = requests.get(f"{BASE_URL}")
        json_data = json.loads(response.text)
        for franchise in json_data['league']['franchises']['franchise']:
            franchise_array.append(franchise['name'])
    finally:
        print("oh well")
    return franchise_array


get_league()
