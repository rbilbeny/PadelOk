import json
from pathlib import Path

class Club2:
    """
    Creates a Club with it's attributes extracted from the json structured text saved on the app.
    This json is equivalent to the database on a bigger project. 
    """

    def __init__(self, club_id):
        

        with open(f"{str(Path(__file__).parent)}/clubs.json", 'r') as clubs:
            lines = clubs.readlines()
            line = lines[0]

        clubs_json = json.loads(line)
        index, club = next((i, x) for i, x in enumerate(clubs_json) if x["_id"] == club_id)
        
        self.name = clubs_json[index]["name_text"]
        self.id = clubs_json[index]["_id"]
        self.zone = clubs_json[index]["zone_name_text"]
        self.district = clubs_json[index]["district_text"]
        self.web_scraper = clubs_json[index]["web_scraper_name_text"]
        self.url_base = clubs_json[index]["url_base_text"]
        self.url_path_scraper = clubs_json[index]["url_path_scraper_text"]
        self.url_id = clubs_json[index]["url_id_number"]
        self.scraper_available = clubs_json[index]["url_id_number"]