from flask import Flask, request
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from multisearch import MultiSearch

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
# Version2, today in production 
@app.route('/get_single_scraper2', methods=['GET'])
def handle_request_get_single_scraper2():
    club_id  = str(request.args.get('club_id'))
    date = str(request.args.get('date'))
    initial_time_str = str(request.args.get('initial_time', ""))
    final_time_str = str(request.args.get('final_time', ""))
    club_ids = [club_id]
    single_club_search = MultiSearch(club_ids, date, initial_time_str, final_time_str)
    search_results = single_club_search.scrape()     
    return search_results



#SCRAPES MULTIPLE CLUB ENDPOINT
# Version2, today in production
@app.route('/post_multi_scraper2', methods=['POST'])
def handle_request_post_multi_scraper2():
    clubs_ids_text = request.form.get('clubs_ids')
    date = request.form.get('date')
    initial_time_str = request.form.get('initial_time', "")
    final_time_str = request.form.get('final_time', "") 
    clubs_ids_list = clubs_ids_text.split(", ")
    multi_club_search = MultiSearch(clubs_ids_list, date, initial_time_str, final_time_str)
    search_results = multi_club_search.scrape()      
    return search_results