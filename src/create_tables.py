#!/usr/bin/env python3
import os
import sqlite3

URL_DB = os.getenv("URL_DB")


def create_songs(conn):
    stmt = """
    CREATE TABLE songs (
        sid INTEGER PRIMARY KEY,
        artist TEXT REFERENCES artists(artist),
        sslg TEXT,
        song TEXT,
        songlink TEXT,
        videolink TEXT,
        albumslink TEXT
    );
    """
    conn.execute(stmt)


def create_artists(conn):
    stmt = """
    CREATE TABLE artists (
        aslg TEXT,
        artist TEXT PRIMARY KEY,
        artistlink TEXT,
        concertslink TEXT,
        topttrackslink TEXT,
        campaignlink TEXT
    );
    """
    conn.execute(stmt)


def create_plays(conn):
    stmt = """
    CREATE TABLE plays (
        play_id INTEGER PRIMARY KEY,
        sid INTEGER REFERENCES songs(sid),
        played_at TEXT,
        played_at_display TEXT
    );
    """
    conn.execute(stmt)


def main():
    conn = sqlite3.connect(URL_DB)
    with conn:
        create_songs(conn)
        create_artists(conn)
        create_plays(conn)


if __name__ == "__main__":
    main()
