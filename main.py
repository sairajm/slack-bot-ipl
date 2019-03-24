import requests
from datetime import datetime, timezone

def get_scores_cricbuzz():
    cricbuzz_response = requests.get("https://www.cricbuzz.com/match-api/livematches.json").json()
    matches = cricbuzz_response['matches']
    for match in matches:
        series = matches[match]['series']
        series_name = series['name']
        if "Indian Premier League" in series_name:
            if str(series['type']) in str('IPL'):
                team1 = matches[match]['team1']['name']
                team2 = matches[match]['team2']['name']
                print(team1, " vs ", team2)
                match_start_time = matches[match]['start_time']
                utc_time = datetime.fromtimestamp(int(match_start_time), timezone.utc)
                print(utc_time)

get_scores_cricbuzz()
