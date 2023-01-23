from flask import Flask
from flask import request
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from search import ClubSearch
from club import Club

app = Flask(__name__)


@app.route('/post_clubs', methods=['POST'])
def handle_request_post_clubs():
    input_text = str(request.args.get('clubs'))
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
    club_id  = str(request.args.get('club_id'))
    date = str(request.args.get('date'))
    inital_time = str(request.args.get('initial_time'))
    final_time = str(request.args.get('final_time'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    club = Club(line, club_id)
    single_club_search = ClubSearch(club, date, inital_time, final_time)
    single_club_search.scrape()
    search_result_list = []
    for court in single_club_search.result:
        search_result_list.append(court.__dict__)
    
    json_courts = json.dumps(search_result_list, indent=4)
    return json_courts