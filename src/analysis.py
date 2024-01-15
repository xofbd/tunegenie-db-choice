#!/usr/bin/env python3
import os

from constants import COLLECTION, DATABASE
from utils import connect_to_db

URL_DB = os.getenv("URL_DB")


def calc_number_of_plays(collection):
    """Return the number of songs played"""
    return collection.count_documents({})


def calc_unique_songs(collection):
    """Return the number of unique songs"""
    return len(collection.distinct("song"))


def calc_average_song_play(num_plays, num_songs):
    """Return the average plays per song"""
    return num_plays / num_songs


def calc_top_songs(collection, N):
    """Return results of most played songs"""
    cursor = collection.aggregate([
        {
            "$group":
            {
                "_id": {"song": "$song", "artist": "$artist"},
                "count": {"$count": {}},
            },
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": N
        },
    ])

    print(f"\nTop {N} most played songs")
    for doc in cursor:
        print(f"{doc['_id']['song']} ({doc['_id']['artist']}): {doc['count']}")


def calc_top_artists(collection, N):
    """Return artists with the most plays"""
    cursor = collection.aggregate([
        {"$group": {"_id": "$artist", "count": {"$count": {}}}},
        {"$sort": {"count": -1}},
        {"$limit": N},
    ])

    print(f"\nTop {N} artists with most plays")
    for doc in cursor:
        print(f"{doc['_id']}: {doc['count']}")


def calc_most_distinct_songs(collection, N):
    """Return artists with the most unique/distinct songs played"""
    cursor = collection.aggregate([
        {
            "$group":
            {
                "_id": {"song": "$song", "artist": "$artist"},
                "count": {"$count": {}}
            }
        },
        {
            "$group": {"_id": "$_id.artist", "total": {"$count": {}}}},
        {
            "$sort": {"total": -1}
        },
        {
            "$limit": N
        },
    ])

    print(f"\nTop {N} artists with most distinct songs")
    for doc in cursor:
        print(f"{doc['_id']}: {doc['total']}")


def main():
    client = connect_to_db()
    collection = client[DATABASE][COLLECTION]
    N = 10

    num_plays = calc_number_of_plays(collection)
    num_songs = calc_unique_songs(collection)
    avg_plays = calc_average_song_play(num_plays, num_songs)

    print(f"Number of songs played: {num_plays}")
    print(f"Number of distinct songs played: {num_songs}")
    print(f"Number of plays per song: {avg_plays :0.2f}")
    calc_top_songs(collection, N)
    calc_top_artists(collection, N)
    calc_most_distinct_songs(collection, N)

    client.close()


if __name__ == "__main__":
    main()

