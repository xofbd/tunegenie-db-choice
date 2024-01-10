import os

from pymongo import MongoClient

URL_DB = os.getenv("URL_DB")


def connect_to_db():
    """Return client object connected to MongoDB"""
    if URL_DB is None:
        raise ValueError("URL_DB env variable is not set")

    return MongoClient(URL_DB)
