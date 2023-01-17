from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():  # put application's code here
    text = str(request.args.get('input'))
    data = {'response': text}
    response_json = json.dumps(data)
    return response_json
