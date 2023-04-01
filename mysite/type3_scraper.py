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

PROXY_ACTIVE = False
API_KEY = SCRAPESTACK_KEY
MAX_TRIES = 8


def get_calendar(sport_id, date):


	url = "https://reservas.clublocanas.cl/api/s/AgendaSelNew"
	data = {
		"Fecha": date,
		"IdActividad": sport_id
	}

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
				response = requests.post("https://api.scrapestack.com/scrape", params=params, data=data, verify=False)
			else:
				data = {
					"Fecha": date,
					"IdActividad": sport_id
				}
				response = requests.post(url, data=data, verify=False)
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
	


def check_next_block(current_time_block, available_blocks, delta):
	#Checks if the current time block is available
	for block in available_blocks:
		if block[0] == current_time_block[0] + timedelta(minutes=delta) and block[1] == current_time_block[1]:
			return True
	return False



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
	calendar = get_calendar(str(5), formatted_date)
	#print(calendar)
	#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)

	rows = calendar["Filas"]
	available_blocks = list()
	for row in rows:
		initial_time = row["Horario"]
		courts = row["Canchas"]
		for court in courts:
			if court["Disponible"] == 1:
				available_block = (datetime.strptime(initial_time, '%Y-%m-%dT%H:%M:%S'), court["col"])
				available_blocks.append(available_block)
				print(available_block)

	for block in available_blocks:
		if check_next_block(block, available_blocks, 30):
			block_list.append(TimeBlock2(club.id, block[0], block[0] + timedelta(minutes=60), block[1], 60, 0, get_court_size(block[1])))
			if check_next_block(block, available_blocks, 60):
				block_list.append(TimeBlock2(club.id, block[0], block[0] + timedelta(minutes=90), block[1], 90, 0, get_court_size(block[1])))
				if check_next_block(block, available_blocks, 90):
					block_list.append(TimeBlock2(club.id, block[0], block[0] + timedelta(minutes=120), block[1], 120, 0, get_court_size(block[1])))

	return block_list				
				
				

