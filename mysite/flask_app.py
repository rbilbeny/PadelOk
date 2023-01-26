from flask import Flask
from flask import request
import asyncio
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from search import ClubSearch
from club import Club

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
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time)
    single_club_search.scrape()
    search_result_list = []
    for court in single_club_search.result:
        search_result_list.append(court.__dict__)

    json_courts = json.dumps(search_result_list, indent=4)
    return json_courts




@app.route('/post_multi_scraper1', methods=['POST'])
def handle_request_post_multi_scraper1():
    search_type = request.form.get('search_type')
    clubs_ids_text = request.form.get('clubs_ids')
    search_date = request.form.get('date')
    inital_time = request.form.get('initial_time')
    final_time = request.form.get('final_time')
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    clubs_ids_list = clubs_ids_text.split(", ")
    multisearch_result_list = list()

    for club_id in clubs_ids_list:
        club = Club(line, club_id)
        single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time)
        single_club_search.scrape()
        for court in single_club_search.result:
            multisearch_result_list.append(court.__dict__)

    json_courts = json.dumps(multisearch_result_list, indent=4)
    return json_courts




@app.route('/post_multi_scraper2', methods=['POST'])
def handle_request_post_multi_scraper2():
    search_type = request.form.get('search_type')
    clubs_ids_text = request.form.get('clubs_ids')
    search_date = request.form.get('date')
    inital_time = request.form.get('initial_time')
    final_time = request.form.get('final_time')
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    clubs_ids_list = clubs_ids_text.split(", ")
    multisearch_result_list = list()
    multisearch_result_list = asyncio.get_event_loop().run_until_complete(scrape_all_clubs(search_type, line, clubs_ids_list, search_date, inital_time, final_time))

    json_courts = json.dumps(multisearch_result_list, indent=4)
    return json_courts

async def scrape_all_clubs(search_type, line, clubs_ids_list, search_date, inital_time, final_time):
    multisearch_result_list = list()
    tasks = []
    for club_id in clubs_ids_list:
        task = asyncio.ensure_future(scrape_one_club(search_type, line, club_id, search_date, inital_time, final_time))
        tasks.append(task)
    await asyncio.gather(*tasks)
    for task in tasks:
        for court in task:
            multisearch_result_list.append(court)
    return multisearch_result_list

async def scrape_one_club(search_type, line, club_id, search_date, inital_time, final_time):
    single_result_list = list()
    club = Club(line, club_id)
    single_club_search = ClubSearch(search_type, club, search_date, inital_time, final_time)
    single_club_search.scrape()
    for court in single_club_search.result:
        single_result_list.append(court)
    return single_result_list
