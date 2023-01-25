import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from search import ClubSearch
from club import Club


def handle_request_post_clubs(input_text):
    input_text = input_text.replace('\\', "")
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]    
    
    #LOCAL EQUALS WEB
    json_clubs = line
    return {"result" : json_clubs}




def handle_request_get_single_scraper(search_type, club_id, date, inital_time, final_time): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    #LOCAL EQUALS WEB
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, date, inital_time, final_time)
    single_club_search.scrape()
    search_result_list = []
    for court in single_club_search.result:
        search_result_list.append(court.__dict__)

    json_courts = json.dumps(search_result_list, indent=4)
    return json_courts


def handle_request_post_multi_scraper1(search_type, clubs_ids, date, inital_time, final_time): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    #LOCAL EQUALS WEB
    search_date = date
    clubs_ids_list = clubs_ids.split(", ")
    multisearch_result_list = list()

    for club_id in clubs_ids_list:
        club = Club(line, club_id)
        single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time)
        single_club_search.scrape()
        for court in single_club_search.result:
            multisearch_result_list.append(court.__dict__)  

    json_courts = json.dumps(multisearch_result_list, indent=4)
    return json_courts

