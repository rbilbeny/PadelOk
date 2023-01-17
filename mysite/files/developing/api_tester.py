import requests
import json

URL = "http://rodrigobilbeny.pythonanywhere.com"
payload = {"clubs" : "laloramachina"}

response = requests.post(URL, params=payload)
print(response)
print(response.json())
