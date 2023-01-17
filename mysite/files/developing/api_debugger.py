import json


text = "test"
data = {'clubs_saved': text}
response_json = json.dumps(data)
with open("files/clubs.json", 'w') as updated_clubs:
    updated_clubs.write(response_json)

