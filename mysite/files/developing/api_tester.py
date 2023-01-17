import requests
import json

URL = "http://rodrigobilbeny.pythonanywhere.com"
payload = {"clubs" : "list of clubs"}

response = requests.post(URL, params=payload)
print(response)
print(response.json())
