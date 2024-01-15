import os
import sqlite3

URL_DB = os.getenv("URL_DB")


def calc_unique_songs(cursor):
    result = cursor.execute(
        """
        SELECT COUNT(DISTINCT sid)
        FROM songs;
        """
    )
    print(f"Number of distinct songs: {result.fetchone()[0]}")


def calc_average_song_plays(cursor):
    result = cursor.execute(
        """
        SELECT 1.0 * COUNT(*) / COUNT(DISTINCT sid)
        FROM plays;
        """
    )
    print(f"Number of plays per song: {result.fetchone()[0] :0.2f}")


def calc_top_songs(cursor):
    result = cursor.execute(
        """
        SELECT MAX(song), MAX(artist), COUNT(*) AS num_plays
        FROM plays
        JOIN songs USING(sid)
        GROUP BY sid
        ORDER BY num_plays DESC
        LIMIT 10;
        """
    )
    print("\nTop 10 most played songs")
    for row in result:
        print(f"{row[0]} ({row[1]}): {row[2]}")


def calc_top_artists(cursor):
    result = cursor.execute(
        """
        SELECT artist, COUNT(*) AS num_plays
        FROM plays
        JOIN songs USING(sid)
        JOIN artists USING(artist)
        GROUP BY artist
        ORDER BY COUNT(*) DESC
        LIMIT 10;
        """
    )
    print("\nTop 10 artists with most plays")
    for row in result:
        print(f"{row[0]}: {row[1]}")


def calc_most_distinct_songs(cursor):
    result = cursor.execute(
        """
        SELECT artist, COUNT(*) AS num_songs
        FROM songs
        GROUP BY artist
        ORDER BY COUNT(*) DESC
        LIMIT 10;
        """
    )
    print("\nTop 10 artists with most distinct songs")
    for row in result:
        print(f"{row[0]}: {row[1]}")


def main():
    conn = sqlite3.connect(URL_DB)
    cursor = conn.cursor()

    calc_unique_songs(cursor)
    calc_average_song_plays(cursor)
    calc_top_songs(cursor)
    calc_top_artists(cursor)
    calc_most_distinct_songs(cursor)


if __name__ == "__main__":
    main()

