
import json
import sys
from pathlib import Path
from datetime import datetime
import requests



#YOU CAN SIMPLY IGNORE THIS PART
sys.path.append(str(Path(__file__).parent.parent))
from club import Club2
date = "2023-03-17"
club_id = "1672937071915x276360887553703800" #Youtopia
initial_search_time_str = "13:00"
final_search_time_str = "15:00"     
club = Club2(club_id)
#single_club_search = scraper(club, date, initial_search_time_str, final_search_time_str)

match_duration = 60
print(club.name)

headers = {
		'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'es-CL',
		'app-id': 'easycancha',
		'app-os': 'web',
        'country': 'CL',
        'refer': f'https://www.easycancha.com/book/clubs/{club.url_id}/sports',
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
	}

url = f"https://www.easycancha.com/api/clubs/{club.url_id}/sports/7"
response = requests.get(url=url, headers=headers)
print("first response:", response)
print(response.headers["Set-Cookie"])
key_AWSALB = response.headers["Set-Cookie"].split("AWSALB=")[1].split(";")[0]
key_AWSALBCORS = response.headers["Set-Cookie"].split("AWSALBCORS=")[1].split(";")[0]
print(key_AWSALB)
print(key_AWSALBCORS)

cookies = {
        '_ga' : 'GA1.2.522998898.1678186556',
        '_gid' : 'GA1.2.859991214.1678186556',
        '_gat_gtag_UA_85706904_1': '1',
        'appId' : 'easycancha',
        'appOs': 'web',
        'acceptLanguage':'es-CL',
        '_fbp': 'fb.1.1678186556474.708355354',
        'country': 'CL',
        'AWSALB': key_AWSALB,
        'AWSALBCORS': key_AWSALBCORS,
}

cookie = f"_ga=GA1.2.522998898.1678186556; _gid=GA1.2.859991214.1678186556; appId=easycancha; appOs=web; acceptLanguage=es-CL; _fbp=fb.1.1678186556474.708355354; country=CL; _gat_gtag_UA_85706904_1=1; AWSALB={key_AWSALB}; AWSALBCORS={key_AWSALBCORS}"


headers = {
		'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'es-CL',
		'app-id': 'easycancha',
		'app-os': 'web',
        'cookie' : cookie,
        'country': 'CL',
        'refer': f'https://www.easycancha.com/book/clubs/{club.url_id}/filter',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fech-site': 'same-origin',
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        'x-requested-with': 'XMLHttpRequest'
	}

now = datetime.now().strftime('%H:%M:%S')
url_easy = f"https://www.easycancha.com/api/sports/7/clubs/924/timeslots?date={date}&time={now}timespan={match_duration}"

API_KEY = input("API KEY, please")
response = requests.get(url=f"http://api.scrapestack.com/scrape?access_key={API_KEY}&url={url_easy}&render_js=0&proxy_location=cl&keep_headers=1", cookies=cookies, headers=headers, verify=False)
print(response)
print(response.text)
# response = json.dumps(response, indent=4)
# print(response)
# #print("Total courts found: " + str(len(json.loads(response)["results"])))


