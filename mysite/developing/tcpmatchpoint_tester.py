
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from time_block import TimeBlock
from tcpmatchpoint_scraper import scraper
from club import Club


date = "23/2/2022"
club_id = "1677159808890x906999172264078800" #pie andino
#club_id = "1669903818955x480922479948817660" #estoril
inital_search_time = "13:00"
final_search_time = "15:00"
match_duration = 90
result_type = "all_courts"

with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    
club = Club(line, club_id)
single_club_search = scraper(result_type, club, date, inital_search_time, final_search_time, match_duration)

search_result_list = []
for block in single_club_search:
        search_result_list.append(block.__dict__)        
json_courts = {"results": search_result_list}

response = json.dumps(json_courts, indent=4)
print(response)
print("Total courts found: " + str(len(json.loads(response)["results"])))






