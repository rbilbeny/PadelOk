from flask import Flask
from flask import request
#import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    input_text = str(request.args.get('clubs'))
    #uploaded_json = {'clubs': input_text}
    #filecontent = json.dumps(uploaded_json)
    with open("/home/rodrigobilbeny/mysite/files/clubs.json", 'w') as updated_clubs:
        updated_clubs.write(input_text)

    return {"result" : "succeed"}