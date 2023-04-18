import json
import sys
import time
from pathlib import Path

import local_flask_app

sys.path.append(str(Path(__file__).parent.parent))
json_path =  str(Path(__file__).parent.parent) + "/clubs.json"

#TESTING ALL CLUB'S UPLOAD
def test_post_clubs():
    clubs_text = "" #This text contains an array of club ids, separated by commas
    response = local_flask_app.handle_request_post_clubs(clubs_text)
    print(response)
    preliminar_json = json.loads(response["result"])
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)



#TESTING SINGLE CLUB SCRAPING
# Version2, today in production    
def test_club_search2():
    response = local_flask_app.handle_request_get_single_scraper2("1672937071915x276360887553703800", "2023-04-22", "", "")
    print(json.dumps(response, indent=4))
    print("Total courts found: " + str(len(response["results"])))



 #TESTING MULTIPLE CLUB SCRAPING 
 # Version2, today in production    
def test_multi_search2():
    list_text = "1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200, 1671575242087x935644432011197400, 1671575436576x912922488390485900, 1671575576733x939740595137469000, 1671575703240x964951687272276500, 1671575899691x174113495399525380, 1671575966750x889989581817634000, 1671576404514x979354888909678200, 1671576585532x934079551292597900, 1672937071915x276360887553703800, 1672937321331x524913942331468560, 1673304980276x955532294115819500, 1673413421696x591168331745853400, 1673445939619x571277648445580560, 1673446354677x607823441479734800, 1673466908942x370412396042780700, 1674148309003x590988461942767600, 1677077836592x120441959369631760, 1677078312761x183019328151117000"
    start_time = time.time()
    response = local_flask_app.handle_request_post_multi_scraper2(list_text, "2023-03-07", "", "")
    duration = time.time() - start_time
    clubs_list = list_text.split(", ")
    total_clubs = len(clubs_list)
    print(json.dumps(response, indent=4))
    print("Total courts found: " + str(len(response["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds") 



#currently being tested:
test_club_search2()

