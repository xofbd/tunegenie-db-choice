#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime, timedelta
import json
import os
import sys
import time
from urllib.parse import urlencode

import requests

SLEEP_DURATION_DEFAULT = 5
URL = "https://api.tunegenie.com/v2/brand/nowplaying/"
API_ID = os.getenv("API_ID")
STATION = os.getenv("STATION")
LIMIT = 99


def get_song_data(start_time, sleep_duration=SLEEP_DURATION_DEFAULT):
    """Download song data from a given day"""
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    response = call_api(start_time_str)

    if not response.ok:
        raise IOError(
            f"Could not make request for {start_time} due to {response.reason}",
            file=sys.stderr
        )

    payload = response.json()

    if is_same_day(payload[0], start_time):
        last_played_at = str_to_datetime(payload[0]["played_at"])
        start_time_new = last_played_at + timedelta(days=0, seconds=1)
        time.sleep(sleep_duration)
        return payload + get_song_data(start_time_new, sleep_duration=sleep_duration)
    else:
        payload = evict_wrong_date(payload, start_time)
        return payload


def call_api(start_time_str):
    """Return request response from using API for a given day"""
    params = {
        "apiid": API_ID,
        "b": STATION,
        "since": start_time_str,
        "count": LIMIT,
    }

    print(f"Making request with {start_time_str}")
    params_str = urlencode(params, safe=":")

    return requests.get(URL, params=params_str)


def is_same_day(song, target_date):
    """Return True if song play time occured on the same day"""
    play_time = str_to_datetime(song["played_at"])

    return target_date.date() == play_time.date()


def evict_wrong_date(payload, target_date):
    """Remove entries in payload that are not in the target date"""
    return [song for song in payload if is_same_day(song, target_date)]


def str_to_datetime(date_string):
    """Convert date string into datetime object"""
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def parse_args():
    parser = ArgumentParser(
        description="Download all songs played for a given day using TuneGenie."
    )
    parser.add_argument(
        "date",
        help="date to download song data using YYYY-MM-DD format, e.g., 2023-01-01",
        type=lambda x: datetime.strptime(x, "%Y-%m-%d"),
    )
    parser.add_argument(
        "--sleep",
        help="Number of seconds to pause before making another API request",
        default=SLEEP_DURATION_DEFAULT,
        type=int
    )

    return parser.parse_args()


def cli():
    args = parse_args()
    payload = get_song_data(args.date, sleep_duration=args.sleep)

    sys.stdout.write(json.dumps(payload))


if __name__ == "__main__":
    cli()
