import json
import sys
import time
from pathlib import Path
from datetime import datetime

import local_flask_app

sys.path.append(str(Path(__file__).parent.parent))
from club import Club, Club2
from easycancha_scraper2 import scraper as scrapereasy
from tcpmatchpoint_scraper2 import scraper as scrapertcp

json_path =  str(Path(__file__).parent.parent) + "/clubs.json"


#TESTING CLUB BUILDER
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



#TESTING ALL CLUB'S UPLOAD
def test_post_clubs():
    clubs_text = "" #This text contains an array of club ids, separated by commas
    response = local_flask_app.handle_request_post_clubs(clubs_text)
    print(response)
    preliminar_json = json.loads(response["result"])
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)



#TESTING SINGLE CLUB SCRAPING
# Version1, today in production    
def test_club_search(): 
    response = local_flask_app.handle_request_get_single_scraper("all_courts", "1671573721228x274856123451891360", "28/2/2023", "18:00", "23:30", 60)
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))

# Version2, future development  
def test_club_search2(): 
    response = local_flask_app.handle_request_get_single_scraper2("1671575899691x174113495399525380", "2023-03-04", "14:00", "17:00")
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))



 #TESTING MULTIPLE CLUB SCRAPING 
 # Version1, today in production    
def test_multi_search1(): 
    list_text = "1671577853813x106374013286446580, 1671577915340x390973186142454140, 1672937689649x192587306672282980, 1672937866698x632993144245844400, 1672938013033x655033704969171700, 1672938517230x520189294743913300, 1672938875045x216412821943450240, 1672939093380x996690018588664400, 1672939566137x142975334652431840, 1672939657838x479880029407924600"
    start_time = time.time()
    response = local_flask_app.handle_request_post_multi_scraper1("one_court_per_time_block", list_text, "4/3/2023", "11:00", "24:00", 90)
    duration = time.time() - start_time
    clubs_list = list_text.split(", ")
    total_clubs = len(clubs_list)
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 

# Version2, future development  
def test_multi_search2():
    list_text = "1673490570675x792741118020681700, 1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200"
    start_time = time.time()
    response = local_flask_app.handle_request_post_multi_scraper2(list_text, "2023-03-04", "11:00", "14:00")
    duration = time.time() - start_time
    clubs_list = list_text.split(", ")
    total_clubs = len(clubs_list)
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 



 #TESTING FAST MULTIPLE CLUB SCRAPING
 # easycancha 
def fast_scraping_easy(): 
    list_text = "1671575703240x964951687272276500, 1671575966750x889989581817634000, 1671576206465x538441803752625100, 1671576282580x294847038090804800, 1671576404514x979354888909678200, 1671577124465x129551573075054720, 1671577382320x690922928253442800, 1671577853813x106374013286446580, 1671577915340x390973186142454140, 1672937071915x276360887553703800, 1673304980276x955532294115819500, 1673335870797x235878954487513100, 1673413421696x591168331745853400, 1673445354542x952299567131924500, 1673445939619x571277648445580560, 1673446354677x607823441479734800, 1676563874438x975822131499273000, 1677078312761x183019328151117000"
    start_time = time.time()
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    clubs_ids_list = list_text.split(", ")
    clubs = []
    for club_id in clubs_ids_list:
        club = Club2(club_id)
        clubs.append(club)

    date = datetime.strptime("2023-03-04", "%Y-%m-%d")
    response = scrapereasy(clubs, date, "", "")
    duration = time.time() - start_time
    total_clubs = len(clubs_ids_list)
    multisearch_result_list = []
    for block in response:
        multisearch_result_list.append(block.__dict__)
    json_courts = {"results": multisearch_result_list}
    response = json.dumps(json_courts, indent=4)
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 

 # tcpmatchpoint
def fast_scraping_tcp(): 
    list_text = "1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671573996197x734401608321506200, 1671574328074x637398410371450100, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200, 1671575242087x935644432011197400, 1671575436576x912922488390485900"
    start_time = time.time()
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    clubs_ids_list = list_text.split(", ")
    clubs = []
    for club_id in clubs_ids_list:
        club = Club2(club_id)
        clubs.append(club)

    date = datetime.strptime("2023-03-04", "%Y-%m-%d")
    response = scrapertcp(clubs, date, "", "")
    duration = time.time() - start_time
    total_clubs = len(clubs_ids_list)
    multisearch_result_list = []
    for block in response:
        multisearch_result_list.append(block.__dict__)
    json_courts = {"results": multisearch_result_list}
    response = json.dumps(json_courts, indent=4)
    print(response)
    print("Total courts found: " + str(len(json.loads(response)["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 
    
#currently being tested:
fast_scraping_tcp()

