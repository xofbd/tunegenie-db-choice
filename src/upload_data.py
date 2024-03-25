from datetime import datetime
import os
from pathlib import Path
import sqlite3

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, insert

from tune_genie import get_song_data

load_dotenv()
URL_DB = os.getenv("URL_DB")


def create_dfs(payload):
    """Return data frames for each table given the payload from the API"""
    df = pd.DataFrame(payload)
    dfs = []
    tables = ("plays", "songs", "artists")
    unique_fields = {"songs": "sid", "artists": "artist"}

    for table in tables:
        with (Path("sql") / f"{table}-fields.txt").open("r") as f:
            fields = [line.strip() for line in f]
        dfs.append(df[fields].drop_duplicates(subset=unique_fields.get(table)))

    return zip(tables, dfs)


def insert_records(df, table, conn):
    """Insert records from data frame into the database"""
    if table == "plays":
        df.to_sql(table, conn, if_exists="append", index=False)
    else:
        # Writing each row individually to be able to catch integrity violations.
        # There might be a better way to do this.
        rows = (pd.DataFrame([row]) for row in df.itertuples(index=False))
        for row in rows:
            try:
                row.to_sql(table, conn, if_exists="append", index=False)
            except sqlite3.IntegrityError:
                pass

def main(date):
    conn = sqlite3.connect(URL_DB)
    payload = get_song_data(datetime.strptime(date, "%Y-%m-%d"))
    dfs = create_dfs(payload)
    for table, df in dfs:
        insert_records(df, table, conn)


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
