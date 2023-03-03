import requests
import json
from datetime import datetime, timedelta

from time_block import TimeBlock


def get_calendar(sport_id, club_url_id, date, match_duration):

	url = f"https://www.easycancha.com/api/sports/{sport_id}/clubs/{club_url_id}/timeslots?date={date}&timespan={match_duration}"
	print(url)
	while True:
		try:
			response = requests.get(url)
			if response.status_code==200:
				break
		except:
			pass

	return response.json()			



def is_initial_time_already_listed(initial_time, block_list):
	for block_in_list in block_list:
		if block_in_list.initial_time == initial_time:
			return True
	return False



def is_block_already_listed(block_initial_time, block_final_time, court_name, block_list):
	for block_in_list in block_list:
		if block_in_list.initial_time == block_initial_time and block_in_list.final_time == block_final_time and block_in_list.court_name == court_name:
			return True
	return False



def scraper(result_type, club, date, inital_search_time, final_search_time, match_duration):

	#Defines the response variable, a list of TimeBlock objects. Handles the case where final_search_time is 00:00, which means that the search should be done until next day
	block_list = list()

	initial_search_time_date = datetime.strptime(inital_search_time, '%H:%M')
	if final_search_time == "00:00":
		final_search_time_date = datetime.strptime(final_search_time, '%H:%M')+ timedelta(days=1)
	else:
		final_search_time_date = datetime.strptime(final_search_time, '%H:%M')

	
	#First step is to get the calendar for the given date. If nothing is found for a duration of 90 minutes, it will try with 60 minutes.
	formatted_date = str(datetime.strptime(date, '%d/%m/%Y').date())
	
	if match_duration == 90:
		calendar = get_calendar(str(7), club.url_id, formatted_date, str(90)) #7 is the internal sport ID for Padel at EasyCancha
		if not calendar["alternative_timeslots"]:
			calendar = get_calendar(str(7), club.url_id, formatted_date, str(60)) #7 is the internal sport ID for Padel at EasyCancha
			if not calendar["alternative_timeslots"]:
				return []
	elif match_duration == 60:
		calendar = get_calendar(str(7), club.url_id, formatted_date, str(60)) #7 is the internal sport ID for Padel at EasyCancha
	#print(calendar)
	#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)

	# Extracts some basic information for the club as a whole. Availabilty is evaluated at the court level.
	club_ = calendar["alternative_timeslots"][0]["summary"][0]["clubName"]
	print(club_)
	
	for alternative_slot in calendar["alternative_timeslots"]:
		block_initial_time = alternative_slot["hour"][:5]
		block_final_time = (datetime.strptime(block_initial_time, "%H:%M")+timedelta(minutes=match_duration)).strftime("%H:%M")
		#print(block_initial_time, block_final_time)
		for time_slot in alternative_slot["timeslots"]:
			court_name = time_slot["courtText"]
			block_price = time_slot["priceInfo"]["amount"]
			#print(court_name, block_price)
			if datetime.strptime(block_initial_time, "%H:%M") < initial_search_time_date or datetime.strptime(block_final_time, "%H:%M") > final_search_time_date:
				continue
			#print("Block is inside the search time")
			if result_type == "one_court_per_time_block" and is_initial_time_already_listed(block_initial_time, block_list):
				continue
			#print("Initial time it's not already in the list")
			if is_block_already_listed(block_initial_time, block_final_time, court_name, block_list):
				continue
			#print("Exact same block it's not already in the list")
			new_block = TimeBlock(club.id, date, block_initial_time, block_final_time, court_name, block_price)
			new_block.save_block_duration_text()		
			block_list.append(new_block)

	return block_list		


	
	
	
	

	