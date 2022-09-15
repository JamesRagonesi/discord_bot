# fantasy_api.py
import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()
LEAGUE_ID = os.getenv('FANTASY_LEAGUE_ID')
YEAR = os.getenv('FANTASY_YEAR')
API_KEY = os.getenv('FANTASY_API_KEY')

# Make a really gross URL string
BASE_URL = lambda type : "https://www47.myfantasyleague.com/" + YEAR + "/export?TYPE=" + type + "&L=" + LEAGUE_ID + "&APIKEY=" + API_KEY + "&JSON=1"

# Get Teams
def get_league():
    franchise_data = {}
    try:
        response = requests.get(f"{BASE_URL('league')}")
        json_data = json.loads(response.text)

        for franchise in json_data['league']['franchises']['franchise']:
            franchise_data[franchise['id']] = franchise['name']

    finally:
        print("oh well")
    return franchise_data


def getLeagueStandings():
    standings_data = {}

    try:
        response = requests.get(f"{BASE_URL('leagueStandings')}")
        json_data = json.loads(response.text)

        for franchise in json_data['leagueStandings']['franchise']:
            standings_data[franchise['id']] = { "pf": franchise['avgpf'], "h2hpct": franchise['h2hpct'] }

    except Exception as e:
        print("Error with MFL API", e)

    return standings_data

def getPowerRankings():
    leagueStats = []

    franchiseInfo = get_league()
    franchiseStandings = getLeagueStandings()

    ## combine franchise info and stats
    for key, value in franchiseInfo.items():
        franchiseStanding = franchiseStandings[key]
        leagueStats.append({
            "name": value,
            **franchiseStandings[key]
        })

    for teamStats in leagueStats:
        teamStats['powerScore'] = float(teamStats['pf']) * .5
        teamStats['powerScore'] += float(teamStats['h2hpct']) * .5

    leagueStats = sorted(leagueStats, key=lambda k: k['powerScore'], reverse=True)

    discordOutput = 'POWER RANKINGS\n'
    for i, team in enumerate(leagueStats, start=1):
        discordOutput += f"{i}. {team['name']}, Power Score - {team['powerScore']}\n"

    return discordOutput
