import requests
import json
from datetime import datetime, timedelta

from time_block import TimeBlock


def get_calendar(club_url_id, sport_id, date):

	url = f"https://playtomic.io/api/v1/availability?user_id=me&tenant_id={club_url_id}&sport_id={sport_id}&local_start_min={date}T00:00:00&local_start_max={date}T23:59:59"
	print(url)
	while True:
		try:
			response = requests.get(url)
			if response.status_code==200:
				break
		except:
			pass

	return response.json()			



def get_resources(club_url_base, club_url_id, sport_id, date):

	url = club_url_base + club_url_id + "?q=" + sport_id + "~" + date + "~~~"
	print(url)
	while True:
		try:
			response = requests.get(url)
			if response.status_code==200:
				break
		except:
			pass

	html = response.text
	resources_text = html.split(',"resources":[')[1].split('],"')[0]
	resources_text  = "[" + resources_text + "]"
	return 	resources_text	



def get_court_properties(resource_id, resources):
	
	index, court = next((i, x) for i, x in enumerate(resources) if x["resource_id"] == resource_id)
	return (resources[index]["name"], resources[index]["properties"]["resource_size"])



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



def price_to_int(price):

	if price is None or price == "":
		return 0
	price = price.replace("$","")
	price = price.replace(".","")
	price = price.replace(",",".")
	price = price.replace("CLP","")

	return int(price)



def scraper(result_type, club, date, inital_search_time, final_search_time, match_duration):

	#Defines the response variable, a list of TimeBlock objects. Handles the case where final_search_time is 00:00, which means that the search should be done until next day
	block_list = list()

	initial_search_time_date = datetime.strptime(inital_search_time, '%H:%M')
	if final_search_time == "00:00":
		final_search_time_date = datetime.strptime(final_search_time, '%H:%M')+ timedelta(days=1)
	else:
		final_search_time_date = datetime.strptime(final_search_time, '%H:%M')

	#Fromatting the date to the Playtomic format
	formatted_date = str(datetime.strptime(date, '%d/%m/%Y').date())
	
	#First we get the court_names from the club's resources, scraped from the main page
	resources = get_resources(club.url_base, club.url_path_scraper, "PADEL", formatted_date)
	#print(courts)
	#courts_ = json.dumps(json.loads(courts), indent=4, sort_keys=True)
	#print(courts_)


	#Then we get the availability for the club, scraped from the availability API
	calendar = get_calendar(club.url_path_scraper, "PADEL", formatted_date) #PADEL is the internal sport ID for Padel at Playtomic
	#print(calendar)
	#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)
	

	for court in calendar:
		if formatted_date != court["start_date"]:
			continue
		print("resource_id: ", court["resource_id"])
		print("court_name: ", get_court_properties(court["resource_id"], json.loads(resources))[0])
		print("court_size: ", get_court_properties(court["resource_id"], json.loads(resources))[1])
		print("date: ", court["start_date"])
		for time_slot in court["slots"]:
			print("initial_time: ", time_slot["start_time"])
			print("duration: ", time_slot["duration"])
			print("price: ", price_to_int(time_slot["price"]))


	print("END DEBUGGING")	

	

	# # Extracts some basic information for the club as a whole. Availabilty is evaluated at the court level.
	# club_ = calendar["alternative_timeslots"][0]["summary"][0]["clubName"]
	# print(club_)
	
	# for alternative_slot in calendar["alternative_timeslots"]:
	# 	block_initial_time = alternative_slot["hour"][:5]
	# 	block_final_time = (datetime.strptime(block_initial_time, "%H:%M")+timedelta(minutes=match_duration)).strftime("%H:%M")
	# 	print(block_initial_time, block_final_time)
	# 	for time_slot in alternative_slot["timeslots"]:
	# 		court_name = time_slot["courtText"]
	# 		block_price = time_slot["priceInfo"]["amount"]
	# 		print(court_name, block_price)
	# 		if datetime.strptime(block_initial_time, "%H:%M") < initial_search_time_date or datetime.strptime(block_final_time, "%H:%M") > final_search_time_date:
	# 			continue
	# 		print("Block is inside the search time")
	# 		if result_type == "one_court_per_time_block" and is_initial_time_already_listed(block_initial_time, block_list):
	# 			continue
	# 		print("Initial time it's not already in the list")
	# 		if is_block_already_listed(block_initial_time, block_final_time, court_name, block_list):
	# 			continue
	# 		print("Exact same block it's not already in the list")
	# 		new_block = TimeBlock(club.id, date, block_initial_time, block_final_time, court_name, block_price)
	# 		new_block.save_block_duration_text()		
	# 		block_list.append(new_block)

	# return block_list		


	
	
	
	

	