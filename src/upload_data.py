from datetime import datetime
import os
from pathlib import Path
import sqlite3

from dotenv import load_dotenv

from tune_genie import get_song_data

load_dotenv()
URL_DB = os.getenv("URL_DB")


def create_records(payload):
    records_songs = []
    records_artists = []
    records_plays = []

    for data in payload:
        records_songs.append(parse_data(data, "songs"))
        records_artists.append(parse_data(data, "artists"))
        records_plays.append(parse_data(data, "plays"))

    return {
        "songs": records_songs,
        "artists": records_artists,
        "plays": records_plays,
    }


def parse_data(data, table):
    records = []
    with (Path("sql") / f"{table}-fields.txt").open("r") as f:
        fields = [line.strip() for line in f]

    return tuple((data[field] for field in fields))


def insert_records(records):
    conn = sqlite3.connect(URL_DB)
    cursor = conn.cursor()
    try:
        cursor.executemany(
            """
            INSERT INTO songs
            (sid, artist, sslg, song, songlink, videolink, albumslink)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            records["songs"]
        )
    except sqlite3.IntegrityError:
        pass

    try:
        cursor.executemany(
            """
            INSERT INTO artists
            (aslg, artist, artistlink, concertslink, topttrackslink, campaignlink)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            records["artists"],
        )
    except sqlite3.IntegrityError:
        pass

    cursor.executemany(
        """
        INSERT INTO plays
        (sid, played_at, played_at_display)
        VALUES (?, ?, ?)
         """,
        records["plays"],
    )

    conn.commit()
    conn.close()


def main(date):
    payload = get_song_data(datetime.strptime(date, "%Y-%m-%d"))
    records = create_records(payload)
    insert_records(records)


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
