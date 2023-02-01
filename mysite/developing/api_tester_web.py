import json
import sys
import requests
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

json_path =  str(Path(__file__).parent.parent) + "/clubs.json"

#request POST
def test_post_clubs():
    URL = "http://rodrigobilbeny.pythonanywhere.com/post_clubs"
    clubs_text = "[{\"address_geographic_address\":{\"address\":\"Av. las Condes 10480, Vitacura, Región Metropolitana, Chile\",\"lat\":-33.3822524,\"lng\":-70.533791},\"address_text_text\":\"Av. Las Condes 10480\",\"district_text\":\"Vitacura\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Padel Estoril\",\"place_id_text\":null,\"short_name_text\":\"estoril\",\"url_base_text\":\"https://padelestorilcl.matchpoint.com.es\",\"url_id_number\":null,\"url_path_scraper_text\":\"/Booking/Grid.aspx\",\"web_scraper1_text\":\"tcpmatchpoint-free\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"padel-estoril\",\"Created Date\":\"2022-12-01T14:10:18.955Z\",\"Modified Date\":\"2023-01-25T11:44:45.511Z\",\"_id\":\"1669903818955x480922479948817660\"},{\"address_geographic_address\":{\"address\":\"Alonso de Córdova 4751, Las Condes, Región Metropolitana, Chile\",\"lat\":-33.405559,\"lng\":-70.580692},\"address_text_text\":\"Cerro Colorado 4661\",\"district_text\":\"Las Condes\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Padel Cerro Colorado\",\"place_id_text\":null,\"short_name_text\":\"cerrocolorado\",\"url_base_text\":\"https://padelcerrocolorado.matchpoint.com.es\",\"url_id_number\":null,\"url_path_scraper_text\":\"/Booking/Grid.aspx\",\"web_scraper1_text\":\"tcpmatchpoint-free\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"padel-cerro-colorado\",\"Created Date\":\"2022-12-01T14:12:10.945Z\",\"Modified Date\":\"2023-01-25T11:45:56.694Z\",\"_id\":\"1669903930944x273874201170327460\"},{\"address_geographic_address\":{\"address\":\"Av. las Condes 12560, 7710162 Lo Barnechea, Región Metropolitana, Chile\",\"lat\":-33.3715371,\"lng\":-70.5151749},\"address_text_text\":\"Av. Las Condes 12560\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Club Conecta Las Condes\",\"place_id_text\":null,\"short_name_text\":\"conectalc\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":8,\"url_path_scraper_text\":\"/Pages/17-CLUB_CONECTA_LAS_CONDES\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"club-conecta-las-condes\",\"Created Date\":\"2022-12-01T14:14:48.780Z\",\"Modified Date\":\"2023-01-25T12:07:16.450Z\",\"_id\":\"1669904088780x898504369661313000\"},{\"address_geographic_address\":{\"address\":\"Luis Bascuñán 1858, 7690127 Lo Barnechea, Región Metropolitana, Chile\",\"lat\":-33.355169,\"lng\":-70.5200091},\"address_text_text\":\"Luis Bascuñán 1858\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Club Conecta La Dehesa\",\"place_id_text\":null,\"short_name_text\":\"conectald\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":5,\"url_path_scraper_text\":\"/Pages/15-CLUB_CONECTA_LA_DEHESA_PADEL\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:02:01.228Z\",\"Modified Date\":\"2023-01-25T11:46:28.808Z\",\"_id\":\"1671573721228x274856123451891360\"},{\"address_geographic_address\":null,\"address_text_text\":\"F30-E Puchuncaví\",\"district_text\":\"Puchuncaví\",\"latitude_number\":-32.64215718994758,\"longitude_number\":-71.42365576082673,\"name_text\":\"Club Conecta Maitencillo\",\"place_id_text\":\"ChIJkb-QV5O7iZYRiZXN6SEIj1c\",\"short_name_text\":\"conectam\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":9,\"url_path_scraper_text\":\"/Pages/18-CLUB_CONECTA_MAITENCILLO\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Maitencillo - Cachagua - Zapallar\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:06:36.197Z\",\"Modified Date\":\"2023-01-25T11:46:40.248Z\",\"_id\":\"1671573996197x734401608321506200\"},{\"address_geographic_address\":null,\"address_text_text\":\"Calle Madreselva 17055\",\"district_text\":\"Maipú\",\"latitude_number\":-33.54637229254393,\"longitude_number\":-70.78086659278901,\"name_text\":\"Club Conecta Maipú (Asturias)\",\"place_id_text\":\"ChIJs0P16g7dYpYRclVpUS_IMMM\",\"short_name_text\":\"conectamaipu\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":15,\"url_path_scraper_text\":\"/Pages/16-CLUB_CONECTA_MAIPU\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Poniente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:10:01.113Z\",\"Modified Date\":\"2023-01-25T11:46:50.225Z\",\"_id\":\"1671574201113x740733292243334000\"},{\"address_geographic_address\":{\"address\":\"Av. Diego Portales 640, Arica, Arica y Parinacota, Chile\",\"lat\":-18.4702474,\"lng\":-70.3067767},\"address_text_text\":\"Av. Diego Portales 640\",\"district_text\":\"Arica\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Club Conecta Mall Plaza Arica\",\"place_id_text\":null,\"short_name_text\":\"conectaarica\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":16,\"url_path_scraper_text\":\"/Pages/22-CLUB_CONECTA_MALL_PLAZA_ARICA\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Arica\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:12:08.074Z\",\"Modified Date\":\"2023-01-25T11:47:17.186Z\",\"_id\":\"1671574328074x637398410371450100\"},{\"address_geographic_address\":null,\"address_text_text\":\"San Enrique 14951\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":-33.36351768405138,\"longitude_number\":-70.49323210615626,\"name_text\":\"Padel Arrayan\",\"place_id_text\":\"ChIJGaMnsLTLYpYRyE6Fz6y9jTo\",\"short_name_text\":\"arrayan\",\"url_base_text\":\"https://padelarrayancl.matchpoint.com.es\",\"url_id_number\":null,\"url_path_scraper_text\":\"/Booking/Grid.aspx\",\"web_scraper1_text\":\"tcpmatchpoint-free\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:17:48.076Z\",\"Modified Date\":\"2023-01-25T11:47:30.887Z\",\"_id\":\"1671574668076x697672856529101700\"},{\"address_geographic_address\":{\"address\":\"Av. Américo Vespucio 1501, Cerrillos, Región Metropolitana, Chile\",\"lat\":-33.5171784,\"lng\":-70.7144692},\"address_text_text\":\"Av. Américo Vespucio 1501\",\"district_text\":\"Cerrillos\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Club Conecta Mall Plaza Oeste\",\"place_id_text\":null,\"short_name_text\":\"conectoe\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":17,\"url_path_scraper_text\":\"/Pages/21-CLUB_CONECTA_MALL_PLAZA_OESTE\",\"web_scraper1_text\":\"tcpmatchpoint-fixed\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Poniente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2023-01-24T22:32:00.357Z\",\"Modified Date\":\"2023-01-25T11:47:45.864Z\",\"_id\":\"1674599520357x232630663460140060\"}]"
    data = {'clubs': clubs_text}
    response = requests.post(URL, data=data)
    
    #LOCAL EQUALS WEB
    print(response)
    preliminar_json = json.loads(response.json()["result"])
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)

def test_club_search():
    URL = "http://rodrigobilbeny.pythonanywhere.com/get_single_scraper"
    params = {"search_type" : "one_court_per_time_block", "club_id" : "1669903818955x480922479948817660", "date" : "1/2/2023", "initial_time" : "07:00", "final_time" : "00:00", "match_duration" : 120}
    response = requests.get(URL, params=params)
    
    #LOCAL EQUALS WEB
    print(response)
    print(json.dumps(response.json(), indent=4))
    print("Total courts found: " + str(len(response.json())))

def test_multi_search1(): 
    lista_text = "1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200"
    URL = "http://rodrigobilbeny.pythonanywhere.com/post_multi_scraper1"
    data = {"search_type" : "all_courts", "clubs_ids" : lista_text, "date" : "27/1/2023", "initial_time" : "17:00", "final_time" : "19:00"}
    start_time = time.time()
    response = requests.post(URL, data=data)
    duration = time.time() - start_time
    clubs_list = lista_text.split(", ")
    total_clubs = len(clubs_list)
    

    #LOCAL EQUALS WEB
    print(response)
    print(json.dumps(response.json(), indent=4))
    print("Total courts found: " + str(len(response.json())))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds")    


def test_multi_search2(): 
    lista_text = "1669903818955x480922479948817660, 1669903930944x273874201170327460, 1669904088780x898504369661313000, 1671573721228x274856123451891360, 1671574668076x697672856529101700, 1671574796639x371045720000991360, 1671575069499x815302630011782700, 1671575146642x673635785389879200"
    URL = "http://rodrigobilbeny.pythonanywhere.com/post_multi_scraper2"
    data = {"search_type" : "all_courts", "clubs_ids" : lista_text, "date" : "27/1/2023", "initial_time" : "17:00", "final_time" : "19:00"}
    start_time = time.time()
    response = requests.post(URL, data=data)
    duration = time.time() - start_time
    clubs_list = lista_text.split(", ")
    total_clubs = len(clubs_list)
    

    #LOCAL EQUALS WEB
    print(response)
    print(json.dumps(response.json(), indent=4))
    print("Total courts found: " + str(len(response.json())))
    print(f"Scraped courts from {total_clubs} clubs in {duration} seconds")

test_multi_search2()

