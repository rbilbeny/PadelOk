from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():  # put application's code here
    text = str(request.args.get('clubs'))
    data = {'clubs_saved': text}
    response_json = json.dumps(data)
    with open("files/clubs.json", 'w') as updated_clubs:
        updated_clubs.write(response_json)

    return response_json    