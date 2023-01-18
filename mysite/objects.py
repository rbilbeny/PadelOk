import json
from tcpmatchpoint_scraper import scraper as tcp_scraper

class Club:
    """
    Creates a Club with it's attributes extracted from the json structured text saved on the app.
    This json is equivalent to the database on a bigger project. 
    """

    def __init__(self, clubs_text, id):
        
        clubs_json = json.loads(clubs_text)
        index, club = next((i, x) for i, x in enumerate(clubs_json) if x["_id"] == id)
        
        self.name = clubs_json[index]["name_text"]
        self.zone = clubs_json[index]["zone_name_text"]
        self.district = clubs_json[index]["district_text"]
        self.web_scraper = clubs_json[index]["web_scraper1_text"]
        self.url_base = clubs_json[index]["url_base_text"]
        self.url_path_scraper = clubs_json[index]["url_path_scraper_text"]
        self.url_id = clubs_json[index]["url_id_number"]

class LocationSearch:
    """
    Creates a Search that defines the scope of the court web scrapping based on a broad location, and performs it
    """

    def __init__(self, location_list, location_type, initial_date, final_date, inital_time, final_time):
        
        if location_type == "zones":
            self.location_attr = "zone_name_text"
        elif location_type == "districts":
            self.location_attr = "district_text"

        self.locations = location_list
        self.initial_date = initial_date
        self.final_date = final_date
        self.initial_time = inital_time
        self.final_time = final_time
        self.result = list()


class ClubSearch:
    """
    Creates a Search that defines the scope of the court web scrapping for 1 club, and performs it
    """

    def __init__(self, clubs_text, club_id, initial_date, final_date, inital_time, final_time):
        
        self.club = Club(clubs_text, club_id)
        self.initial_date = initial_date
        self.final_date = final_date
        self.initial_time = inital_time
        self.final_time = final_time
        self.result = list()

    def scrape(self):
        if self.club.web_scraper == "tcpmatchpoint":
            tcp_scraper(self.club, '19/1/2023')
        else:
            return    


class Court:
    """
    Creates an object that represents the available court to play found during scraping
    """

    def __init__(self, club_id, date, initial_time, final_time, court_name, court_value):
        
        self.club_id = club_id
        self.date = date
        self.initial_time = initial_time
        self.final_time = final_time
        self.court_name = court_name
        self.court_value = court_value



        
         



        