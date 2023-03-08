import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from multisearch import MultiSearch

#RECEIVES CLUB DATABASE ENDPOINT
def handle_request_post_clubs(input_text):
    input_text = input_text.replace('\\', "")
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]    
    json_clubs = line
    return {"result" : json_clubs}



#SCRAPES ONE CLUB ENDPOINT
# Version2, today in production
def handle_request_get_single_scraper2(club_id, date, initial_time_str, final_time_str): 
    club_ids = [club_id]
    single_club_search = MultiSearch(club_ids, date, initial_time_str, final_time_str)
    search_results = single_club_search.scrape()   
    return search_results



#SCRAPES MULTIPLE CLUB ENDPOINT
# Version2, today in production
def handle_request_post_multi_scraper2(clubs_ids, date, initial_time_str, final_time_str): 
    clubs_ids_list = clubs_ids.split(", ")
    multi_club_search = MultiSearch(clubs_ids_list, date, initial_time_str, final_time_str)
    search_results = multi_club_search.scrape()
    return search_results


