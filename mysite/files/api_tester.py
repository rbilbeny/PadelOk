import requests
import json

URL = "http://rodrigobilbeny.pythonanywhere.com"
payload = {"input" : "list of clubs"}

response = requests.get(URL, params=payload)

print(response.json())
