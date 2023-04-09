import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from type2_scraper import scraper
from club import Club2

date = "2023-04-11"
club_id = "1677078312761x183019328151117000" #Zarhi Pade
club_id = "1672937071915x276360887553703800" #youtopia
initial_search_time_str = "07:00"
final_search_time_str = "15:00"
match_duration = 90

with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    
club = Club2(club_id)
print(club.name)
print(club.url_id)
single_club_search = scraper(club, date, initial_search_time_str, final_search_time_str)


search_result_list = []
for block in single_club_search:
        search_result_list.append(block.__dict__)        
json_courts = {"results": search_result_list}

response = json.dumps(json_courts, indent=4)
print(response)
print("Total courts found: " + str(len(json.loads(response)["results"])))
