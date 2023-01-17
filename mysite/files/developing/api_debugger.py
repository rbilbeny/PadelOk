import json

text = "test"
data = {'response': text}
response_json = json.dumps(data)
with open("files/clubs.json", 'w') as updated_clubs:
	updated_clubs.write(response_json)

