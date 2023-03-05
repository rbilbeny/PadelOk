import requests
import json
import re
from datetime import datetime, timedelta

from time_block import TimeBlock2


def get_calendar(sport_id, club_url_id, date, match_duration):

	url = f"https://www.easycancha.com/api/sports/{sport_id}/clubs/{club_url_id}/timeslots?date={date}&timespan={match_duration}"
	#print(url)
	while True:
		try:
			response = requests.get(url)
			if response.status_code==200:
				break
		except:
			pass

	return response.json()	



def get_court_size(court_name):
	lower_court_name = court_name.lower()
	pattern = "single"
	if re.search(pattern, lower_court_name):
		return "Single"
	else:
		return "Double"



def is_block_already_listed(current_block_initial_time, current_block_final_time, court_name, current_block_match_duration, block_list):
	for block_in_list in block_list:
		block_in_list_initial_time = datetime.strptime(block_in_list.initial_time, "%Y-%m-%dT%H:%M:%S.%fZ")
		block_in_list_final_time = datetime.strptime(block_in_list.final_time, "%Y-%m-%dT%H:%M:%S.%fZ")

		if block_in_list_initial_time == current_block_initial_time and block_in_list_final_time == current_block_final_time \
		and block_in_list.court_name == court_name and block_in_list.match_duration == current_block_match_duration:
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
				if is_block_already_listed(block_initial_time, block_final_time, court_name, match_duration, block_list):
					continue
				#print("Exact same block it's not already in the list")
				block_price = time_slot["priceInfo"]["amount"]
				new_block = TimeBlock2(club.id, block_initial_time, block_final_time, court_name, match_duration, block_price, get_court_size(court_name))	
				block_list.append(new_block)
			
	return block_list

