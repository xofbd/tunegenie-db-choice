from constants import DATABASE
from utils import connect_to_db


def main():
    """Drop MongoDB by deleting all collections"""
    client = connect_to_db()
    db = client[DATABASE]

    for collection in db.list_collection_names():
        db[collection].drop()

    print(f"Database {DATABASE} has been cleared")
    client.close()

if __name__ == "__main__":
    main()
