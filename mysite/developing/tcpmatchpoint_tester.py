
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from time_block import TimeBlock
from tcpmatchpoint_scraper import scraper
from club import Club


date = "23/2/2022"
club_id = "1674148309003x590988461942767600"
inital_search_time = "08:00"
final_search_time = "23:00"
match_duration = 60
result_type = "all_courts"

with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    
club = Club(line, club_id)
search_result = scraper(result_type, club, date, inital_search_time, final_search_time, match_duration)

print(search_result)
print("Total courts found: " + str(len(json.loads(search_result)["results"])))






