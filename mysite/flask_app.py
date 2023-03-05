from flask import Flask, request
import json
import sys
from datetime import datetime
from time import sleep
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from search import ClubSearch
from multisearch import MultiSearch
from club import Club

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

#RECEIVES CLUB DATABASE ENDPOINT
@app.route('/post_clubs', methods=['POST'])
def handle_request_post_clubs():
    input_text = str(request.form.get('clubs'))
    input_text = input_text.replace('\\', "")
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]
    json_clubs = line
    return {"result" : json_clubs}



#SCRAPES ONE CLUB ENDPOINT
# Version1, today in production 
@app.route('/get_single_scraper', methods=['GET'])
def handle_request_get_single_scraper():
    search_type = str(request.args.get('search_type'))
    club_id  = str(request.args.get('club_id'))
    search_date = str(request.args.get('date'))
    inital_time = str(request.args.get('initial_time'))
    final_time = str(request.args.get('final_time'))
    match_duration = int(request.args.get('match_duration'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time, match_duration)
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
@app.route('/get_single_scraper2', methods=['GET'])
def handle_request_get_single_scraper2():
    club_id  = str(request.args.get('club_id'))
    date = str(request.args.get('date'))
    initial_time_str = str(request.args.get('initial_time', ""))
    final_time_str = str(request.args.get('final_time', ""))
    club_ids = [club_id]
    single_club_search = MultiSearch(club_ids, date, initial_time_str, final_time_str)
    try:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
            searches_data = json.loads(lines)
    except:
        searches_data = []
    searches = []
    for search_dict in searches_data:
        search = MultiSearch(**search_dict)
        searches.append(search)
    searches.append(single_club_search)
    searches_data = [search.__dict__ for search in searches]
    searches_json = json.dumps(searches_data)
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'w') as searches:
        searches.write(searches_json)
    sleep(2)
    while True:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
        searches_data = json.loads(lines)
        for search_dict in searches_data:
            if search_dict["id"] == single_club_search.id:
                search = MultiSearch(**search_dict)
                break
        if search.status == "finished":
            break
        sleep(1)         
    search_results = {"results": search.results, "errors": search.errors}       
    return search_results



#SCRAPES MULTIPLE CLUB ENDPOINT
# Version1, today in production 
@app.route('/post_multi_scraper1', methods=['POST'])
def handle_request_post_multi_scraper1():
    search_type = request.form.get('search_type')
    clubs_ids_text = request.form.get('clubs_ids')
    search_date = request.form.get('date')
    inital_time = request.form.get('initial_time')
    final_time = request.form.get('final_time')
    match_duration = int(request.form.get('match_duration'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    clubs_ids_list = clubs_ids_text.split(", ")
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
@app.route('/post_multi_scraper2', methods=['POST'])
def handle_request_post_multi_scraper2():
    clubs_ids_text = request.form.get('clubs_ids')
    date = request.form.get('date')
    initial_time_str = request.form.get('initial_time', "")
    final_time_str = request.form.get('final_time', "") 
    clubs_ids_list = clubs_ids_text.split(", ")
    multi_club_search = MultiSearch(clubs_ids_list, date, initial_time_str, final_time_str)
    try:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
            searches_data = json.loads(lines)
    except:
        searches_data = []
    searches = []
    for search_dict in searches_data:
        search = MultiSearch(**search_dict)
        searches.append(search)
    searches.append(multi_club_search)
    searches_data = [search.__dict__ for search in searches]
    searches_json = json.dumps(searches_data)
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'w') as searches:
        searches.write(searches_json)
    sleep(2)
    while True:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
        searches_data = json.loads(lines)
        for search_dict in searches_data:
            if search_dict["id"] == multi_club_search.id:
                search = MultiSearch(**search_dict)
                break
        if search.status == "finished":
            break
        sleep(1)         
    search_results = {"results": search.results, "errors": search.errors}
    return search_results    
