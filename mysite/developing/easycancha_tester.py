
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from easycancha_scraper2 import scraper
from club import Club2


date = "2023-03-07"
club_id = "1673413421696x591168331745853400" #Zarhi Padel
initial_search_time_str = "13:00"
final_search_time_str = "15:00"    
    
club = Club2(club_id)
single_club_search = scraper(club, date, initial_search_time_str, final_search_time_str)



response = json.dumps(single_club_search , indent=4)
print(response)
#print("Total courts found: " + str(len(json.loads(response)["results"])))






