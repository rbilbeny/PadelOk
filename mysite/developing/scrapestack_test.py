import requests
import json
import re
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'Security'))
from padelok_secure import SCRAPESTACK_KEY

PROXY_ACTIVE = True
API_KEY = SCRAPESTACK_KEY
MAX_TRIES = 8

headers = {
	"accept": 'application/json, text/plain, */*',
	"accept-encoding": 'gzip, deflate, br',
	"accept-language": 'es-CL',
	"app-id": 'easycancha',
	"app-os": 'web',
	"country": 'CL',
	"referer":f'https://www.easycancha.com/book/clubs/924/filter',
	"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
	"x-requested-with": 'XMLHttpRequest'
	}

url = "https://www.easycancha.com/api/sports/7/clubs/924/timeslots?date=2023-04-18&time=18:13:39&timespan=90"

params = {
					"access_key": API_KEY,
					"url": url,
					"keep_headers": 1,
					"proxy_location": "cl",
                    "premium_proxy" : 0
				}
print(params)
response = requests.get("https://api.scrapestack.com/scrape", params=params, headers=headers, verify=False)
print(response.text)
#response = requests.get(url, headers=headers, verify=False)
#print(response.text)

params = {
    "interval": '5min',
    "function": 'TIME_SERIES_INTRADAY',
    "symbol": 'MSFT',
    "datatype": 'json',
    "output_size": 'compact'
  },
params = {
					"access_key": API_KEY,
					"url": url,
					"keep_headers": 1,
					"proxy_location": "cl",
                    "premium_proxy" : 0
				}
headers = {
    'X-RapidAPI-Key': 'SIGN-UP-FOR-KEY',
    'X-RapidAPI-Host': 'alpha-vantage.p.rapidapi.com'
  }
