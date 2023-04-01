
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from type1_scraper import scraper
from club import Club2


date = "2023-03-07"
club_id = "1677078312761x183019328151117000" #Zarhi Pade
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






