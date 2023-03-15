# fantasy_api.py
import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()
LEAGUE_ID = os.getenv('FANTASY_LEAGUE_ID', default='44276')
YEAR = os.getenv('FANTASY_YEAR', default='2023')
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

    except Exception as e:
        print("Error with MFL API", e)
    return franchise_data

def getLeagueStandings():
    standings_data = {}

    try:
        response = requests.get(f"{BASE_URL('leagueStandings')}")
        json_data = json.loads(response.text)

        for franchise in json_data['leagueStandings']['franchise']:
            standings_data[franchise['id']] = { "avgpf": franchise['avgpf'], "h2hpct": franchise['h2hpct'] }

    except Exception as e:
        print("Error with MFL API", e)

    return standings_data

def getWeeklyResults():
    weekly_results = {}
    weeks = range(1, 18)

    try:
        for week in weeks:
            print(f"processing week {week}")
            response = requests.get(f"{BASE_URL('weeklyResults')}&W={week}")
            json_data = json.loads(response.text)

            for matchup in json_data['weeklyResults']['matchup']:
                for franchise in matchup['franchise']:
                    ## assume the week hasn't been finished
                    if 'score' not in franchise:
                        print(f"week {week} wasnt quite ready, returning results")
                        weekly_results['week'] = week - 1
                        return weekly_results

                    franchise_id = franchise['id']
                    testScore = float(franchise['score'])

                    if franchise_id in weekly_results:
                        if testScore > weekly_results[franchise_id]['highScore']:
                            weekly_results[franchise_id]['highScore'] = testScore

                        if testScore < weekly_results[franchise_id]['lowScore']:
                            weekly_results[franchise_id]['lowScore'] = testScore
                    else:
                        weekly_results[franchise_id] = {
                            'highScore': testScore,
                            'lowScore': testScore
                        }

    except Exception as e:
        print("Error with MFL API", e)

    return weekly_results

def getPowerRankings():
    leagueStats = []

    franchiseInfo = get_league()
    franchiseStandings = getLeagueStandings()
    weeklyResults = getWeeklyResults()

    ## combine franchise info, stats, and weeklyResults
    for key, value in franchiseInfo.items():
        leagueStats.append({
            "name": value,
            **franchiseStandings[key],
            **weeklyResults[key]
        })

    ## The OIL Power Rating
    ## ((avg score x 6) + [(high score + low score) x 2] +[ (winning % x 200) x 2])/10
    for teamStats in leagueStats:
        teamStats['powerScore'] = ((float(teamStats['avgpf']) * 6)
            + ((float(teamStats['highScore']) + float(teamStats['lowScore'])) * 2)
            + (float(teamStats['h2hpct']) * 200))/10

    leagueStats = sorted(leagueStats, key=lambda k: k['powerScore'], reverse=True)

    discordOutput = f"POWER RANKINGS THROUGH WEEK {weeklyResults['week']}\n"
    for i, team in enumerate(leagueStats, start=1):
        discordOutput += f"{i}. {team['name']}, Power Score - {round(team['powerScore'], 2)}\n"

    return discordOutput
