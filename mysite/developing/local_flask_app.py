import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from search import ClubSearch
from multisearch import MultiSearch
from club import Club

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
# Version1, today in production 
def handle_request_get_single_scraper(search_type, club_id, date, inital_time, final_time, match_duration): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, date, inital_time, final_time, match_duration)
    single_club_search.scrape()   
    search_result_list = []
    search_error_list = []
    for block in single_club_search.result:
        search_result_list.append(block.__dict__)
    if single_club_search.error != None:
        search_error_list.append({"error_message": single_club_search.error})
    json_courts = {"results": search_result_list, "errors": search_error_list}
    response = json.dumps(json_courts, indent=4)
    return response

# Version2, future development 
def handle_request_get_single_scraper2(club_id, date, initial_time_str, final_time_str): 
    club_ids = [club_id]
    single_club_search = MultiSearch(club_ids, date, initial_time_str, final_time_str)
    search_results = single_club_search.scrape()   
    return search_results



#SCRAPES MULTIPLE CLUB ENDPOINT
# Version1, today in production 
def handle_request_post_multi_scraper1(search_type, clubs_ids, date, inital_time, final_time, match_duration): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    search_date = date
    clubs_ids_list = clubs_ids.split(", ")
    multisearch_result_list = list()
    search_error_list = []
    for club_id in clubs_ids_list:
        club = Club(line, club_id)
        single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time, match_duration)
        single_club_search.scrape()
        for block in single_club_search.result:
            multisearch_result_list.append(block.__dict__) 
        if single_club_search.error != None:
            search_error_list.append({"error_message": single_club_search.error})    
    json_courts = {"results": multisearch_result_list, "errors": search_error_list}
    response = json.dumps(json_courts, indent=4)
    return response

# Version2, future development
def handle_request_post_multi_scraper2(clubs_ids, date, initial_time_str, final_time_str): 
    clubs_ids_list = clubs_ids.split(", ")
    multi_club_search = MultiSearch(clubs_ids_list, date, initial_time_str, final_time_str)
    search_results = multi_club_search.scrape()
    return search_results


