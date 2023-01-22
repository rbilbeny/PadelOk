from datetime import datetime, timedelta 

from club import Club
from tcpmatchpoint_scraper import scraper as tcp_scraper


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
            start_date = datetime.strptime(self.initial_date, "%d/%m/%Y")
            end_date = datetime.strptime(self.final_date, "%d/%m/%Y")
            delta = timedelta(days=1)
            current_date = start_date
            while current_date <= end_date:
                self.result.extend(tcp_scraper(self.club, current_date.strftime("%d/%m/%Y"), self.initial_time, self.final_time))
                current_date += delta

            sorted_result = sorted(self.result, key=lambda x: (x['date'], x['court_name'], x['initial_time']), 
                      key=lambda x: (x['club_id'], x['date'], x['court_name'], x['initial_time']),
                      reverse=[False, False, False, False]) 

            self.result = sorted_result       

        else:
            return    




        
         



        