import requests
import json
from datetime import datetime, timedelta

from court import Court

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
	
	cheat_code=html.split("heatCode='")[1].split("';")[0]
	
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
		
def scraper(club, date, inital_time, final_time):

	court_list = list()
	
	calendar_url = club.url_base + club.url_path_scraper
	print(calendar_url)
	id_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadros"
	API_url = club.url_base + "/booking/srvc.aspx/ObtenerCuadro"
	
	session_id,cheat_code = get_session(calendar_url)
	
	if club.url_id is None:
		id = get_id(id_url,session_id,cheat_code)
		print("id obtenido")	
	else:
		id = club.url_id
		print("id forzado")

	print("id es: "+ str(id))
	calendar = get_calendar(API_url, calendar_url, session_id, cheat_code, id, date)
	#print(calendar)
	calendar_ = json.dumps(calendar, indent=4, sort_keys=True)
	#print(calendar_)

	club_ = calendar["d"]["Nombre"]
	print(club_)
	courts = calendar["d"]["Columnas"]
	
	if courts[0]["IdModalidadFijaParaReservas"] != 3:
		for court in courts:
			available_time_blocks = court["HorariosFijos"]
			for available_time_block in available_time_blocks:
				block_initial_time = available_time_block["StrHoraInicio"]
				block_final_time = available_time_block["StrHoraFin"]
				court_name = court["TextoPrincipal"]
				block_price = price_to_int(available_time_block["TextoAdicional"])
				if (inital_time <= block_initial_time) and (final_time >= block_final_time):
					court_list.append(Court(club.id, date, block_initial_time, block_final_time, court_name, block_price))

	elif courts[0]["IdModalidadFijaParaReservas"] == 3:
		club_initial_time = datetime.strptime(calendar["d"]["StrHoraInicio"], "%H:%M")
		club_final_time = datetime.strptime(calendar["d"]["StrHoraFin"], "%H:%M")
		interval = timedelta(minutes=30)

		for court in courts:
			occupied_courts = court["Ocupaciones"]
			current_time = club_initial_time
			while current_time <= (club_final_time-2*interval):
				current_block = (current_time.strftime("%H:%M"), (current_time + 2*interval).strftime("%H:%M"))
				current_block_available = True
				for occupied_court in occupied_courts:
					occupied_block = (occupied_court["StrHoraInicio"], occupied_court["StrHoraFin"])
					if occupied_block[0] <= current_block[0] and occupied_block[1] >= current_block[1]:
						current_block_available = False
						break
					if occupied_block[0] > current_block[0] and occupied_block[0] < current_block[1]:
						current_block_available = False
						break
					if occupied_block[1] > current_block[0] and occupied_block[0] < current_block[0]:
						current_block_available = False
						break	
				if current_block_available==False:
					current_time += interval
					continue
				elif current_block_available==True:
					block_initial_time = current_block[0]
					block_final_time = current_block[1]
					court_name = court["TextoPrincipal"]
					block_price = 0
					if (inital_time <= block_initial_time) and (final_time >= block_final_time):
						court_list.append(Court(club.id, date, block_initial_time, block_final_time, court_name, block_price))
				current_time += interval
				
	return court_list
