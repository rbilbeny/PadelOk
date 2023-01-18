import json

class Club:
    """
    Creates a Club with it's attributes extracted from the json structured text saved on the app. 
    """

    def __init__(self, clubs_text, id):
        
        clubs_json = json.load(clubs_text)
        index, club = next((i, x) for i, x in enumerate(clubs_json) if x["_id"] == id)
        
        self.name = clubs_json[index]["name_text"]
        self.zone = clubs_json[index]["zone_name_text"]
        self.district = clubs_json[index]["district_text"]
        self.web_scraper = clubs_json[index]["web_scraper_text"]
        self.url_base = clubs_json[index]["name_text"]
        self.url_scraper = clubs_json[index]["name_text"]
        self.url_id = clubs_json[index]["name_text"]
        