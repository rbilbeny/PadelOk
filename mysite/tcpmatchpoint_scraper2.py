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

login_data = {
    				'email': 'rodrigobilbeny@gmail.com',
    				'password': 'yzy1QUY-nrv.khp!jbz'
				}

def login(base_url):
	session = requests.Session()
	while True:
		try:
			url = base_url + "/Login.aspx"	
			response = session.post(url, data=login_data)
			if response.status_code==200:
				break
		except:
			pass
	
	session_id=response.cookies.get_dict()["ASP.NET_SessionId"]
	
	return session_id



def get_session(calendar_url):

	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Language': 'en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	}
	url = calendar_url
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
				response = requests.get("https://api.scrapestack.com/scrape", params=params,  headers=headers, verify=False)
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

	html=response.text
	try:
		cheat_code=html.split("heatCode='")[1].split("';")[0]
	except:
		try:
			cheat_code=html.split("pKey='")[1].split("';")[0]
		except:
			cheat_code=""	

	try:
		session_id=response.cookies.get_dict()["ASP.NET_SessionId"]
	except: 
		session_id=""	

	return session_id,cheat_code



def get_id(id_url,session_id,cheat_code):

	cookies = {
		'ASP.NET_SessionId': session_id,
		'i18next': 'es-CL',
		'MPOpcionCookie': 'necesarios',
	}

	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Type': 'application/json; charset=UTF-8',
		'Pragma': 'no-cache',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}

	json_data = {
		'p': cheat_code,
		'key': cheat_code
	}

	url = id_url
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
				response = requests.post("https://api.scrapestack.com/scrape", params=params, headers=headers, cookies=cookies, json=json_data, verify=False)
			else:
				response = requests.post(url,cookies=cookies,headers=headers,json=json_data,verify=False)
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

	id=response.json()["d"][0]["Id"]

	return id



def get_calendar(API_url,calendar_url,session_id,cheat_code,id,date):

	cookies = {
	'ASP.NET_SessionId': session_id,
	'i18next': 'es-CL',
	'MPOpcionCookie': 'necesarios',
	}

	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Content-Type': 'application/json; charset=UTF-8',
		'Pragma': 'no-cache',
		'Referer': calendar_url,
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
		'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
	}

	json_data = {
		'idCuadro': id,
		'fecha': date,
		'p': cheat_code,
		'key': cheat_code
	}
	url = API_url
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
				response = requests.post("https://api.scrapestack.com/scrape", params=params, headers=headers, cookies=cookies, json=json_data, verify=False)
			else:	
				response = requests.post(url,cookies=cookies,headers=headers,json=json_data,verify=False)
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

	calendar=response.json()

	return calendar



def price_to_int(price):

	if price is None or price == "":
		return 0
	price = price.replace("$","")
	price = price.replace(".","")
	price = price.split(",")[0]

	return int(price)



def get_court_size(court_name):
	lower_court_name = court_name.lower()
	pattern = "single"
	if re.search(pattern, lower_court_name):
		return "Single"
	else:
		return "Double"



def is_current_block_available(current_block_time_interval, occupied_blocks):
	for occupied_block in occupied_blocks:
		initial_occupied_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(occupied_block["StrHoraInicio"], "%H:%M").time())
		final_occupied_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(occupied_block["StrHoraFin"], "%H:%M").time())
		if final_occupied_time  < initial_occupied_time:
			final_occupied_time  = final_occupied_time  + timedelta(days=1)	
		occupied_block_time_interval = (initial_occupied_time, final_occupied_time)

		if not(current_block_time_interval[1] <= occupied_block_time_interval[0] or occupied_block_time_interval[1] <= current_block_time_interval[0]):
			return False
		
	return True



def is_current_block_overlaping_fixed_block(current_block_time_interval, fixed_blocks):
	for fixed_block in fixed_blocks:
		initial_fixed_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(fixed_block["StrHoraInicio"], "%H:%M").time())
		final_fixed_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(fixed_block["StrHoraFin"], "%H:%M").time())
		if final_fixed_time  < initial_fixed_time:
			final_fixed_time  = final_fixed_time  + timedelta(days=1)	
		fixed_block_time_interval = (initial_fixed_time, final_fixed_time)
		
		if current_block_time_interval[0] < fixed_block_time_interval[0] and fixed_block_time_interval[0] < current_block_time_interval[1]:
			return True
		if current_block_time_interval[0] < fixed_block_time_interval[1] and fixed_block_time_interval[1] < current_block_time_interval[1]:
			return True
		
	return False



def matching_fixed_block(current_block_time_interval, fixed_blocks):
	for fixed_block in fixed_blocks:
		initial_fixed_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(fixed_block["StrHoraInicio"], "%H:%M").time())
		final_fixed_time = datetime.combine(current_block_time_interval[0].date(), datetime.strptime(fixed_block["StrHoraFin"], "%H:%M").time())
		if final_fixed_time  < initial_fixed_time:
			final_fixed_time  = final_fixed_time  + timedelta(days=1)	
		fixed_block_time_interval = (initial_fixed_time, final_fixed_time)

		if fixed_block_time_interval[0] == current_block_time_interval[0] and current_block_time_interval[1] == fixed_block_time_interval[1]:
			try:
				block_price = price_to_int(fixed_block["TextoAdicional"])	
			except:
				block_price = 0
			return (True, fixed_block_time_interval[0], fixed_block_time_interval[1], block_price)
	return (False, "", "", "")



def scraper(club, date, initial_search_time_str, final_search_time_str):

	date = datetime.strptime(date, "%Y-%m-%d")
	#Defines the response variable, a list of TimeBlock objects
	block_list = list()

	#Buils the URLs requiered for this particular scraper 
	calendar_url = club.url_base + club.url_path_scraper
	#print(calendar_url)
	id_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadros"
	API_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadro"

	#Fisrt scrapping step, gets the session id and the cheat code
	if club.id == "1677159808890x906999172264078800": #This is the only club that requires a login, we will keep it this way until we find a better solution
		session_id = login(club.url_base)
		cheat_code = "eNEe29kXfZByQCnYpO1N2CNLhOvbqVUuJiGKU/HyckTglvloaKL4JA==" #Can't find out how to get this one, i've got it from the frontend
	else:	
		session_id,cheat_code = get_session(calendar_url)

	#Second scrapping step, gets the id of the club. Sometimes the URL holds multiple clubs and in those cases this method doesn't work.
	#For each of those cases, the id is forced to be the one specified in the club object, obtained previously through trial and error, manually. 
	if club.url_id is None:
		id = get_id(id_url,session_id,cheat_code)
		#print("id obtenido")
	else:
		id = club.url_id
		#print("id forzado")
	#print("id: "+ str(id))

	#Third scrapping step, gets the calendar of the club for the specified date, which contains all the information needed to evaluate availability.
	calendar = get_calendar(API_url, calendar_url, session_id, cheat_code, id, date.strftime('%d/%m/%Y'))
	#print(calendar)
	#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)

	# Extracts some basic information for the club as a whole. Availabilty is evaluated at the court level.
	club_ = calendar["d"]["Nombre"]
	#print(club_)
	courts = calendar["d"]["Columnas"]
	club_initial_search_time = datetime.combine(date, datetime.strptime(calendar["d"]["StrHoraInicio"], "%H:%M").time())
	club_final_search_time = datetime.combine(date, datetime.strptime(calendar["d"]["StrHoraFin"], "%H:%M").time())
	#If the final_search_time is past midnight, the final time is set to the same time the next day.
	if club_final_search_time < club_initial_search_time:
		club_final_search_time  = club_final_search_time  + timedelta(days=1)		

	#If you want to limit the search time interval, you can do it here.
	if initial_search_time_str != "":
		initial_search_time = datetime.combine(date, datetime.strptime(initial_search_time_str, "%H:%M").time())
	if final_search_time_str != "":
		final_search_time = datetime.combine(date, datetime.strptime(final_search_time_str, "%H:%M").time())	
	#If the final_search_time is past midnight, the final time is set to the same time the next day.
	if initial_search_time_str != "" and final_search_time_str != "" and final_search_time < initial_search_time:
		final_search_time  = final_search_time  + timedelta(days=1)		

	if (initial_search_time_str != "" and initial_search_time < club_initial_search_time) or initial_search_time_str == "":
		initial_search_time = club_initial_search_time
	if (final_search_time_str != "" and final_search_time > club_final_search_time) or final_search_time_str == "":
		final_search_time = club_final_search_time		


	#print("initial_search_time:", initial_search_time)	
	#print("final_search_time:", final_search_time)		
	
	#Prepares the search time interval and match durations to be used in the search
	search_resolution = timedelta(minutes=30)
	match_durations = [60, 90, 120]

	for court in courts:
		court_name = court["TextoPrincipal"]
		fixed_time_blocks = court["HorariosFijos"]
		occupied_time_blocks = court["Ocupaciones"]
		#print("court_name:", court_name)
		
		for match_duration in match_durations:
			
			#print("match_duration:", match_duration, "minutes")
			current_time = initial_search_time

			while current_time <= final_search_time - timedelta(minutes=match_duration):
				
				current_block = (current_time, current_time + timedelta(minutes=match_duration))	
				
				if not(is_current_block_available(current_block, occupied_time_blocks)):
					current_time += search_resolution
					continue
				#print("current_block it's available:", current_block)
				if is_current_block_overlaping_fixed_block(current_block, fixed_time_blocks):
					current_time += search_resolution
					continue
				#print("it's not overlaping")		
				is_matching = matching_fixed_block(current_block, fixed_time_blocks)
				if is_matching[0]:
					block_initial_time = is_matching[1]
					block_final_time = is_matching[2]
					matching_block_price = is_matching[3]
					#print("it's inside fixed block")
				else:	
					block_initial_time = current_block[0]
					block_final_time = current_block[1]
				try :
					block_price = matching_block_price
					matching_block_price = 0
				except:
					block_price = 0

				new_block = TimeBlock2(club.id, block_initial_time, block_final_time, court_name, match_duration, block_price, get_court_size(court_name))	
				block_list.append(new_block)
							
				current_time += search_resolution

	return block_list		


	