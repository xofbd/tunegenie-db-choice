from datetime import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient

from tune_genie import get_song_data
from constants import COLLECTION, DATABASE
from utils import connect_to_db

load_dotenv()
URL_DB = os.getenv("URL_DB")


def main(date_str):
    print(f"Uploading radio station play data for {date_str}")

    date = datetime.strptime(date_str, "%Y-%m-%d")
    payload = get_song_data(date)

    client = connect_to_db()
    db = client[DATABASE]
    collection = db[COLLECTION]

    collection.insert_many(payload)

    client.close()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
