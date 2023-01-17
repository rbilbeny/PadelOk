from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/post_clubs', methods=['POST'])
def handle_request_post():
    input_text = str(request.args.get('clubs'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]    
    json_clubs = line
    return {"result" : json_clubs}

@app.route('/get_address', methods=['GET'])
def handle_request_get():
    input_text = str(request.args.get('club_name'))
    with open("/home/rodrigobilbeny/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]


    return {"address" : input_text}

    