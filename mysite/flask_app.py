from flask import Flask
from flask import request
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from search import ClubSearch, ClubSearch2
from club import Club, Club2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

@app.route('/post_clubs', methods=['POST'])
def handle_request_post_clubs():
    input_text = str(request.form.get('clubs'))
    input_text = input_text.replace('\\', "")
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    json_clubs = line
    return {"result" : json_clubs}




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

    #LOCAL EQUALS WEB
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




@app.route('/get_single_scraper2', methods=['GET'])
def handle_request_get_single_scraper2():
    club_id  = str(request.args.get('club_id'))
    search_date = str(request.args.get('date'))
    initial_time = str(request.args.get('initial_time', ""))
    final_time = str(request.args.get('final_time', ""))

    search_date = datetime.strptime(search_date, "%Y-%m-%d")

    club = Club2(club_id)
    single_club_search = ClubSearch2(club, search_date)
    single_club_search.scrape(initial_time, final_time)   
    search_result_list = []
    search_error_list = []
    for block in single_club_search.result:
        search_result_list.append(block.__dict__)
    if single_club_search.error != None:
        search_error_list.append({"error_message": single_club_search.error})
    json_courts = {"results": search_result_list, "errors": search_error_list}
    response = json.dumps(json_courts, indent=4)
    return response




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

    #LOCAL EQUALS WEB
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




@app.route('/post_multi_scraper2', methods=['POST'])
def handle_request_post_multi_scraper2():
    search_type = request.form.get('search_type')
    clubs_ids_text = request.form.get('clubs_ids')
    search_date = request.form.get('date')
    inital_time = request.form.get('initial_time')
    final_time = request.form.get('final_time')
    match_duration = int(request.form.get('match_duration'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    clubs_ids_list = clubs_ids_text.split(", ")
    multisearch_result_list = list()
    multisearch_result_list = asyncio.get_event_loop().run_until_complete(scrape_all_clubs(search_type, line, clubs_ids_list, search_date, inital_time, final_time, match_duration))

    json_courts = json.dumps(multisearch_result_list, indent=4)
    return json_courts

async def scrape_all_clubs(search_type, line, clubs_ids_list, search_date, inital_time, final_time, match_duration):
    multisearch_result_list = list()
    tasks = []
    for club_id in clubs_ids_list:
        task = asyncio.ensure_future(scrape_one_club(search_type, line, club_id, search_date, inital_time, final_time, match_duration))
        tasks.append(task)
    await asyncio.gather(*tasks)
    for task in tasks:
        for court in task:
            multisearch_result_list.append(court)
    return multisearch_result_list

async def scrape_one_club(search_type, line, club_id, search_date, inital_time, final_time, match_duration):
    single_result_list = list()
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time, match_duration)
    single_club_search.scrape()
    for court in single_club_search.result:
        single_result_list.append(court)
    return single_result_list
