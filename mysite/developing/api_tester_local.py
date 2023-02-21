import json
import sys
import time
import requests
from pathlib import Path

import local_flask_app

sys.path.append(str(Path(__file__).parent.parent))
from club import Club

json_path =  str(Path(__file__).parent.parent) + "/clubs.json"


#request POST
def test_post_clubs():
    clubs_text = ""
    response = local_flask_app.handle_request_post_clubs(clubs_text)
    print(response)
    preliminar_json = json.loads(response["result"])
    
    #LOCAL EQUALS WEB
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)

def test_club_builder(): 
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    test_club = Club(line,"1674599520357x232630663460140060")
    print("id is " + test_club.id)
    print("name is " + test_club.name)
    print("district is " + test_club.district) 
    print("zone is " + test_club.zone) 
    print("urlbase is " + test_club.url_base) 
    print("urlid is " + str(test_club.url_id)) 
    print("urlpath is " + test_club.url_path_scraper) 
    print("scraper is " + test_club.web_scraper)   
    
def test_club_search(): 
    response = local_flask_app.handle_request_get_single_scraper("all_courts", "1671575436576x912922488390485900", "21/2/2023", "22:00", "00:00", 90)
    
    #LOCAL EQUALS WEB
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))

def test_multi_search1(): 
    lista_text = "1673490570675x792741118020681700, 1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200"
    start_time = time.time()
    response = local_flask_app.handle_request_post_multi_scraper1("one_court_per_time_block", lista_text, "17/2/2023", "11:00", "24:00", 90)
    duration = time.time() - start_time
    clubs_list = lista_text.split(", ")
    total_clubs = len(clubs_list)
    
    
    #LOCAL EQUALS WEB
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 

def test_club_search_easy():
    date = "2023-01-28"
    timespam = str(60)
    time = "05:00:00"
    sport_id = str(7)
    club_id = str(381) 
    url = f"https://www.easycancha.com/api/sports/{sport_id}/clubs/{club_id}/timeslots?date={date}&time={time}&timespan={timespam}"
    response = requests.get(url)

    #LOCAL EQUALS WEB
    print(url)
    print(json.dumps(response.json(), indent=4))
   

#test_club_search()
test_club_search()

