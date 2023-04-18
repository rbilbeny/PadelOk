import requests
import json
import re
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta

from time_block import TimeBlock2

sys.path.append(str(Path(__file__).parent.parent.parent / 'Security'))
from padelok_secure import SCRAPESTACK_KEY

PROXY_ACTIVE = True
API_KEY = SCRAPESTACK_KEY
MAX_TRIES = 8


def get_calendar(sport_id, club_url_id, date, match_duration):

	headers = {
		"accept": 'application/json, text/plain, */*',
		"accept-encoding": 'gzip, deflate, br',
		"accept-language": 'es-CL',
		"app-id": 'easycancha',
		"app-os": 'web',
		"country": 'CL',
		"referer":f'https://www.easycancha.com/book/clubs/{club_url_id}/filter',
		"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
		"x-requested-with": 'XMLHttpRequest'
		}

	now = datetime.now().strftime("%H:%M:%S")
	url = f"https://www.easycancha.com/api/sports/{sport_id}/clubs/{club_url_id}/timeslots?date={date}&time={now}&timespan={match_duration}"
	#print(url)

	tries = 0
	while True:
		try:
			if PROXY_ACTIVE:
				params = {
					"access_key": API_KEY,
					"url": url,
					"keep_headers": 1,
					"proxy_location": "cl"
				}
				response = requests.get("https://api.scrapestack.com/scrape", params=params, headers=headers, verify=False)
			else:
				response = requests.get(url, headers=headers, verify=False)
			if response.status_code==200:
				break
			else:
				tries = tries + 1
				if tries > MAX_TRIES:
					break
				time.sleep(0.1)

		except:
			tries = tries + 1
			if tries > MAX_TRIES:
				break
			time.sleep(0.1)
			pass

	return response.json()	



def get_court_size(court_name):
	lower_court_name = court_name.lower()
	pattern = "single"
	if re.search(pattern, lower_court_name):
		return "Single"
	else:
		return "Double"



def scraper(club, date, initial_search_time_str, final_search_time_str):
	
	date = datetime.strptime(date, "%Y-%m-%d")
	#Defines the response variable, a list of TimeBlock objects. Handles the case where final_search_time is 00:00, which means that the search should be done until next day
	block_list = list()

	#If you want to limit the search time interval, you can do it here. If not, the search will be done for the whole day and the next day.
	if initial_search_time_str != "":
		initial_search_time = datetime.combine(date, datetime.strptime(initial_search_time_str, "%H:%M").time())
	else: 
		initial_search_time = date
	if final_search_time_str != "":
		final_search_time = datetime.combine(date, datetime.strptime(final_search_time_str, "%H:%M").time())
	else:
		final_search_time = date + timedelta(days=2)

	#If the final_search_time is past midnight, the final time is set to the same time the next day.
	if final_search_time < initial_search_time:
		final_search_time  = final_search_time  + timedelta(days=1)			

	#print("initial_search_time:", initial_search_time)	
	#print("final_search_time:", final_search_time)		

	#Set the variables for the loop
	formatted_date = str(date.date())	
	match_durations = [60, 90, 120]

	for match_duration in match_durations:
		
		#print("match_duration:", match_duration)
		calendar = get_calendar(str(7), club.url_id, formatted_date, str(match_duration)) #7 is the internal sport ID for Padel at EasyCancha
		#print(calendar)
		#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
		#print(calendar_)

		# Extracts some basic information for the club as a whole. Availabilty is evaluated at the court level.
		try: 
			club_ = calendar["alternative_timeslots"][0]["summary"][0]["clubName"]
			#print(club_)
		except:
			continue	

		for alternative_slot in calendar["alternative_timeslots"]:
			block_initial_time = datetime.combine(date, datetime.strptime(alternative_slot["hour"][:5], "%H:%M").time())
			block_final_time = datetime.combine(date, datetime.strptime(alternative_slot["hour"][:5], "%H:%M").time()) + timedelta(minutes=match_duration)
			#print(block_initial_time, block_final_time)
			if block_initial_time < initial_search_time or block_final_time > final_search_time:
				continue
			#print("Block is inside the search time")
			for time_slot in alternative_slot["timeslots"]:	
				court_name = time_slot["courtText"]
				#print(court_name, block_price)
				block_price = time_slot["priceInfo"]["amount"]
				new_block = TimeBlock2(club.id, block_initial_time, block_final_time, court_name, match_duration, block_price, get_court_size(court_name))	
				block_list.append(new_block)
			
	return block_list

