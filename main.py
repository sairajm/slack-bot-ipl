import requests
from datetime import datetime, timezone, timedelta
import time


def get_scores_cricbuzz():
    cricbuzz_response = requests.get("https://www.cricbuzz.com/match-api/"
                                     "livematches.json").json()
    matches = cricbuzz_response['matches']
    for match in matches:
        series = matches[match]['series']
        series_name = series['name']
        if "Indian Premier League" in series_name:
            if str(series['type']) in str('IPL'):
                team1 = matches[match]['team1']['name']
                team2 = matches[match]['team2']['name']
                match_start_time = matches[match]['start_time']
                utc_time = datetime.fromtimestamp(int(match_start_time), timezone.utc)
                current_utc_time = time_in_utc()
                if is_it_played_today(utc_time, current_utc_time):
                    if not is_status_not_empty(matches[match]['status']):
                        print("Ongoing game")
                        print(team1, " vs ", team2)
                        scores_and_status = get_game_scores(match, matches)
                        print(scores_and_status[0], " ",scores_and_status[1])


def time_in_utc():
    """
    Calculate time in UTC given current time, takes into account DST.
    :return: Time in UTC.
    """
    now = datetime.now()
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    diff = offset / 60 / 60 * -1

    # If diff is negative then the timezone is behind UTC and diff
    # needs to be added to bring it to UTC
    if diff < 0:
        diff = diff * (-1)
        time_utc = now + timedelta(hours=diff)
        now = time_utc
    else:
        time_utc = now - timedelta(hours=diff)
        now = time_utc

    return now


def is_it_played_today(game_time, current_time):
    if current_time.date().day == game_time.date().day:
        return True
    else:
        return False


def is_status_not_empty(status):

    if status in "":
        return True
    else:
        return False


def get_game_scores(match, matches):
    scores = matches[match]['score']
    batting = scores['batting']['score']
    bowling = scores['bowling']['score']
    game_status = matches[match]['status']
    return batting, bowling, game_status


get_scores_cricbuzz()
