import requests
from datetime import datetime, timedelta

from time_block import TimeBlock

PROXY_ACTIVE = False
API_KEY = ""

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

	while True:
		try:
			if PROXY_ACTIVE:
				response = requests.get("https://api.scrapestack.com/scrape?access_key="+API_KEY+"&render_js=0&url="+calendar_url, headers=headers, verify=False)
			else:
				response = requests.get(calendar_url, headers=headers, verify=False)
			if response.status_code==200:
				break
		except:
			pass

	html=response.text
	try:
		cheat_code=html.split("heatCode='")[1].split("';")[0]
	except:
		cheat_code=0

	session_id=response.cookies.get_dict()["ASP.NET_SessionId"]

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
	}

	while True:
		try:
			if PROXY_ACTIVE:
				response = requests.post("https://api.scrapestack.com/scrape?access_key="+API_KEY+"&render_js=0&url="+id_url,cookies=cookies,headers=headers,json=json_data,verify=False)
			else:
				response = requests.post(id_url,cookies=cookies,headers=headers,json=json_data,verify=False)
			if response.status_code==200:
				break

		except:
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
	}

	if PROXY_ACTIVE:
		response = requests.post("https://api.scrapestack.com/scrape?access_key="+API_KEY+"&render_js=0&url="+API_url,cookies=cookies,headers=headers,json=json_data,verify=False)
	else:
		response = requests.post(API_url,cookies=cookies,headers=headers,json=json_data,verify=False)

	calendar=response.json()

	return calendar



def price_to_int(price):

	if price is None or price == "":
		return 0
	price = price.replace("$","")
	price = price.replace(".","")
	price = price.replace(",",".")

	return int(price)



def is_current_block_available(current_block_time_interval, occupied_blocks):
	for occupied_block in occupied_blocks:
		occupied_block_time_interval = (occupied_block["StrHoraInicio"], occupied_block["StrHoraFin"])
		if occupied_block_time_interval[1] == "00:00":
			occupied_block_time_interval = (occupied_block["StrHoraInicio"], "23:59")
		if not(current_block_time_interval[1] <= occupied_block_time_interval[0] or occupied_block_time_interval[1] <= current_block_time_interval[0]):
			return False
		
	return True



def is_current_block_overlaping_fixed_block(current_block_time_interval, fixed_blocks):
	for fixed_block in fixed_blocks:
		fixed_block_time_interval = (fixed_block["StrHoraInicio"], fixed_block["StrHoraFin"])
		if fixed_block_time_interval[1] == "00:00":
			fixed_block_time_interval = (fixed_block["StrHoraInicio"], "23:59")
		if current_block_time_interval[0] < fixed_block_time_interval[0] and fixed_block_time_interval[0] < current_block_time_interval[1]:
			return True
		if current_block_time_interval[0] < fixed_block_time_interval[1] and fixed_block_time_interval[1] < current_block_time_interval[1]:
			return True
		
	return False



def is_current_block_inside_fixed_block(current_block_time_interval, fixed_blocks):
	for fixed_block in fixed_blocks:
		fixed_block_time_interval = (fixed_block["StrHoraInicio"], fixed_block["StrHoraFin"])
		if fixed_block_time_interval[1] == "00:00":
			fixed_block_time_interval = (fixed_block["StrHoraInicio"], "23:59")
		if fixed_block_time_interval[0] <= current_block_time_interval[0] and current_block_time_interval[1] <= fixed_block_time_interval[1]:
			return True
		
	return False



def matching_fixed_block(current_block_time_interval, fixed_blocks):
	for fixed_block in fixed_blocks:
		fixed_block_time_interval = (fixed_block["StrHoraInicio"], fixed_block["StrHoraFin"])
		if fixed_block_time_interval[1] == "00:00":
			fixed_block_time_interval = (fixed_block["StrHoraInicio"], "23:59")
		if fixed_block_time_interval[0] <= current_block_time_interval[0] and current_block_time_interval[1] <= fixed_block_time_interval[1]:
			try:
				block_price = price_to_int(fixed_block["TextoAdicional"])	
			except:
				block_price = 0
			return (fixed_block_time_interval[0], fixed_block_time_interval[1], block_price)
	return ("","")



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

	#Defines the response variable, a list of TimeBlock objects
	block_list = list()

	#Buils the URLs requiered for this particular scraper 
	calendar_url = club.url_base + club.url_path_scraper
	print(calendar_url)
	id_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadros"
	API_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadro"

	#Fisrt scrapping step, gets the session id and the cheat code
	session_id,cheat_code = get_session(calendar_url)

	#Second scrapping step, gets the id of the club. Sometimes the URL holds multiple clubs and in those cases this method doesn't work.
	#For each of those cases, the id is forced to be the one specified in the club object, obtained previously through trial and error, manually. 
	if club.url_id is None:
		id = get_id(id_url,session_id,cheat_code)
		print("id obtenido")
	else:
		id = club.url_id
		print("id forzado")
	print("id es: "+ str(id))

	#Third scrapping step, gets the calendar of the club for the specified date, which contains all the information needed to evaluate availability.
	calendar = get_calendar(API_url, calendar_url, session_id, cheat_code, id, date)
	#print(calendar)
	#calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)

	# Extracts some basic information for the club as a whole. Availabilty is evaluated at the court level.
	club_ = calendar["d"]["Nombre"]
	print(club_)
	courts = calendar["d"]["Columnas"]
	initial_club_time = datetime.strptime(calendar["d"]["StrHoraInicio"], "%H:%M")
	final_club_time = datetime.strptime(calendar["d"]["StrHoraFin"], "%H:%M")

	#If the club closes past midnight, the final time is set to the same time the next day.
	if final_club_time < initial_club_time:
		final_club_time= datetime.strptime(calendar["d"]["StrHoraFin"], "%H:%M")+timedelta(days=1)	
	
	#Prepares the search time interval to be used in the search. If the search time interval is outside the club's opening hours, it is adjusted to the club's opening hours.
	search_resolution = timedelta(minutes=30)
	if initial_club_time > datetime.strptime(inital_search_time, "%H:%M"):
		inital_search_time = initial_club_time.strftime("%H:%M")
	if 	final_club_time < datetime.strptime(final_search_time, "%H:%M"):
		final_search_time = final_club_time.strftime("%H:%M")

	#print("initial_search_time:", inital_search_time)	
	#print("final_search_time:",final_search_time)	

	for court in courts:
		court_name = court["TextoPrincipal"]
		fixed_time_blocks = court["HorariosFijos"]
		occupied_time_blocks = court["Ocupaciones"]
		current_time = datetime.strptime(inital_search_time, "%H:%M")

		while current_time <= (datetime.strptime(final_search_time, "%H:%M") - timedelta(minutes=match_duration) + timedelta(minutes=1)):
			current_block = (current_time.strftime("%H:%M"), (current_time + timedelta(minutes=match_duration)).strftime("%H:%M"))
			if current_block[1] == "00:00":
				current_block = (current_block[0], "23:59")	
			#print("current_block:", current_block)	
			if not(is_current_block_available(current_block, occupied_time_blocks)):
				current_time += search_resolution
				continue
			#print("it's available")
			if is_current_block_overlaping_fixed_block(current_block, fixed_time_blocks):
				current_time += search_resolution
				continue
			#print("it's not overlaping")		
			if is_current_block_inside_fixed_block(current_block, fixed_time_blocks):
				matching_block = matching_fixed_block(current_block, fixed_time_blocks)
				block_initial_time = matching_block[0]
				block_final_time = matching_block[1]
				matching_block_price = matching_block[2]
				#print("it's inside fixed block")
			else:	
				block_initial_time = current_block[0]
				block_final_time = current_block[1]
			if result_type == "one_court_per_time_block" and is_initial_time_already_listed(block_initial_time, block_list):
				current_time += search_resolution
				continue
			#print("Initial time it's not already in the list")
			if is_block_already_listed(block_initial_time, block_final_time, court_name, block_list):
				current_time += search_resolution
				continue
			#print("Exact same block it's not already in the list")
			try :
				block_price = matching_block_price
			except:
				block_price = 0
			if block_final_time == "23:59":
					block_final_time = "00:00"
			new_block = TimeBlock(club.id, date, block_initial_time, block_final_time, court_name, block_price)
			new_block.save_block_duration_text()		
			block_list.append(new_block)
						
			current_time += search_resolution

	return block_list		

