import json
import local_flask_app
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from objects import Club, ClubSearch, Court, LocationSearch

json_path =  str(Path(__file__).parent.parent) + "/clubs.json"


#request POST
def test_post_clubs():
    clubs_text = "[{\"address_geographic_address\":{\"address\":\"Av. las Condes 10480, Vitacura, Región Metropolitana, Chile\",\"lat\":-33.3822524,\"lng\":-70.533791},\"address_text_text\":\"Av. Las Condes 10480\",\"district_text\":\"Vitacura\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Padel Estoril\",\"place_id_text\":null,\"short_name_text\":\"estoril\",\"url_base_text\":\"https://padelestorilcl.matchpoint.com.es\",\"url_id_number\":null,\"url_path_scraper_text\":\"/Booking/Grid.aspx\",\"web_scraper1_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"padel-estoril\",\"Created Date\":\"2022-12-01T14:10:18.955Z\",\"Modified Date\":\"2023-01-18T01:07:03.184Z\",\"_id\":\"1669903818955x480922479948817660\"},{\"address_geographic_address\":{\"address\":\"Av. las Condes 12560, 7710162 Lo Barnechea, Región Metropolitana, Chile\",\"lat\":-33.3715371,\"lng\":-70.5151749},\"address_text_text\":\"Av. Las Condes 12560\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Club Conecta Las Condes\",\"place_id_text\":null,\"short_name_text\":\"conectalc\",\"url_base_text\":\"https://www.clubconecta.cl\",\"url_id_number\":16,\"url_path_scraper_text\":\"/Pages/17-CLUB_CONECTA_LAS_CONDES\",\"web_scraper1_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"club-conecta-las-condes\",\"Created Date\":\"2022-12-01T14:14:48.780Z\",\"Modified Date\":\"2023-01-18T01:05:38.038Z\",\"_id\":\"1669904088780x898504369661313000\"},{\"address_geographic_address\":{\"address\":\"Cam. San Francisco de Asis 199, Lo Barnechea, Región Metropolitana, Chile\",\"lat\":-33.3702279,\"lng\":-70.5180103},\"address_text_text\":\"San Francisco de Asis 199\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Más Padel (Club Pato Cornejo)\",\"place_id_text\":null,\"short_name_text\":\"patocor\",\"url_base_text\":\"http://www.maspadel.cl\",\"url_id_number\":null,\"url_path_scraper_text\":\"/Booking/Grid.aspx\",\"web_scraper1_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2023-01-05T16:48:41.331Z\",\"Modified Date\":\"2023-01-18T20:41:45.606Z\",\"_id\":\"1672937321331x524913942331468560\"}]"
    response = local_flask_app.handle_request_post_clubs(clubs_text)
    print(response)
    preliminar_json = json.loads(response["result"])
    
    #LOCAL EQUALS WEB
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)

def test_club_builder(): 
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    test_club = Club(line,"1672937321331x524913942331468560")
    print("name is " + test_club.name)
    print("district is " + test_club.district) 
    print("zone is " + test_club.zone) 
    print("urlbase is " + test_club.url_base) 
    print("urlid is " + str(test_club.url_id)) 
    print("urlpath is " + test_club.url_path_scraper) 
    print("scraper is " + test_club.web_scraper)   
    
def test_club_search(): 
    with open(json_path, 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    single_club_search = ClubSearch(line, "1672937321331x524913942331468560", "", "", "", "")
    single_club_search.scrape()

test_club_builder()
test_club_search()