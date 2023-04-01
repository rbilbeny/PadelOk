import json
import sys
import requests
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'Security'))
from padelok_secure import PADELOK_BUBBLE_KEY

sys.path.append(str(Path(__file__).parent.parent))
json_path =  str(Path(__file__).parent.parent) + "/clubs.json"

#TESTING ALL CLUB'S UPLOAD
def test_post_clubs():
    URL = "https://rodrigobilbeny.pythonanywhere.com/post_clubs"
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    data = {'clubs': line}
    headers = {"Authorization": f"Bearer {PADELOK_BUBBLE_KEY}"}
    response = requests.post(URL, data=data, headers=headers)
    print(response)
    preliminar_json = json.loads(response.json()["result"])
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)



#TESTING SINGLE CLUB SCRAPING
# Version2, today in production 
def test_club_search2():
    URL = "https://rodrigobilbeny.pythonanywhere.com/get_single_scraper2"
    params = {"club_id" : "1669903818955x480922479948817660", "date" : "2023-03-22"}
    headers = {"Authorization": f"Bearer {PADELOK_BUBBLE_KEY}"}
    response = requests.get(URL, params=params, headers=headers)
    print(response)
    print(json.dumps(response.json(), indent=4))
    print("Total courts found: " + str(len(response.json()["results"])))



 #TESTING MULTIPLE CLUB SCRAPING   
# Version2, today in production
def test_multi_search2(): 
    list_text = "1671576206465x538441803752625100, 1671576282580x294847038090804800, 1671576483233x664693423202648700, 1671576690252x405747028704388300"
    URL = "https://rodrigobilbeny.pythonanywhere.com/post_multi_scraper2"
    data = {"clubs_ids" : list_text, "date" : "2023-03-25"}
    headers = {"Authorization": f"Bearer {PADELOK_BUBBLE_KEY}"}
    start_time = time.time()
    response = requests.post(URL, data=data, headers=headers)
    duration = time.time() - start_time
    clubs_list = list_text.split(", ")
    total_clubs = len(clubs_list)
    print(response)
    print(json.dumps(response.json(), indent=4))
    print("Total courts found: " + str(len(response.json()["results"])))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds")



#currently being tested:
test_multi_search2()
