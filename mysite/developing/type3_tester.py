
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from type3_scraper import scraper
from club import Club2

club = Club2("1672936950392x954995232070283900")


date = "2023-04-02"
single_club_search = scraper(club, date, "", "")

search_result_list = []
for block in single_club_search:
        search_result_list.append(block.__dict__)        
json_courts = {"results": search_result_list}

response = json.dumps(json_courts, indent=4)
print(response)
print("Total courts found: " + str(len(json.loads(response)["results"])))


