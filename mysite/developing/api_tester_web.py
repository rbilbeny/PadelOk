import requests
import json

#request POST
def test_post_clubs():
    URL = "http://rodrigobilbeny.pythonanywhere.com/post_clubs"
    clubs_text = "[{\"address_geographic_address\":{\"address\":\"Alonso de Córdova 4751, Las Condes, Región Metropolitana, Chile\",\"lat\":-33.405559,\"lng\":-70.580692},\"address_text_text\":\"Cerro Colorado 4661\",\"calendar_url_text\":\"/Booking/Grid.aspx\",\"district_text\":\"Las Condes\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Padel Cerro Colorado\",\"place_id_text\":null,\"short_name_text\":\"cerrocolorado\",\"url_api_text\":\"https://padelcerrocolorado.matchpoint.com.es\",\"web_id_number\":null,\"web_scraper_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":\"padel-cerro-colorado\",\"Created Date\":\"2022-12-01T14:12:10.945Z\",\"Modified Date\":\"2023-01-17T23:08:40.862Z\",\"_id\":\"1669903930944x273874201170327460\"},{\"address_geographic_address\":{\"address\":\"Paul Harris 9388, Las Condes, Región Metropolitana, Chile\",\"lat\":-33.3909321,\"lng\":-70.5369678},\"address_text_text\":\"Paul Harris 9388\",\"calendar_url_text\":\"/Booking/Grid.aspx\",\"district_text\":\"Las Condes\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Padel Cerro Calan\",\"place_id_text\":null,\"short_name_text\":\"cerrocalan\",\"url_api_text\":\"https://padelcerrocalancl.matchpoint.com.es\",\"web_id_number\":null,\"web_scraper_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2022-12-20T22:27:22.087Z\",\"Modified Date\":\"2023-01-17T23:08:31.491Z\",\"_id\":\"1671575242087x935644432011197400\"},{\"address_geographic_address\":{\"address\":\"Cam. San Francisco de Asis 199, Lo Barnechea, Región Metropolitana, Chile\",\"lat\":-33.3702279,\"lng\":-70.5180103},\"address_text_text\":\"San Francisco de Asis 199\",\"calendar_url_text\":\"/Booking/Grid.aspx\",\"district_text\":\"Lo Barnechea\",\"latitude_number\":null,\"longitude_number\":null,\"name_text\":\"Más Padel (Club Pato Cornejo)\",\"place_id_text\":null,\"short_name_text\":\"patocor\",\"url_api_text\":\"http://www.maspadel.cl\",\"web_id_number\":null,\"web_scraper_text\":\"tcpmatchpoint\",\"zone_custom_zones\":{},\"zone_name_text\":\"Santiago Oriente\",\"Created By\":{},\"Slug\":null,\"Created Date\":\"2023-01-05T16:48:41.331Z\",\"Modified Date\":\"2023-01-17T23:08:22.834Z\",\"_id\":\"1672937321331x524913942331468560\"}]"
    payload = {"clubs" : clubs_text}
    response = requests.post(URL, params=payload)
    
    #LOCAL EQUALS WEB
    print(response)
    preliminar_json = json.loads(response.json()["result"])
    beautiful_json = json.dumps(preliminar_json, indent=4)
    print(beautiful_json)

test_post_clubs()

