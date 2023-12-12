from datetime import datetime

from tune_genie import get_song_data


payload = get_song_data(datetime(2023, 12, 10))
print(payload)
