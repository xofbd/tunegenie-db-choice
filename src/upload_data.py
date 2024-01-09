from datetime import datetime
from dotenv import load_dotenv
from tune_genie import get_song_data

load_dotenv()

payload = get_song_data(datetime(2023, 12, 10))
print(payload)
