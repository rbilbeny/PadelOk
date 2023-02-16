from tcpmatchpoint_scraper import scraper as tcp_scraper

class ClubSearch:
    """
    Creates a Search that defines the scope of the court web scrapping for 1 club, and performs it
    """

    def __init__(self, search_type, club, date, inital_time, final_time, match_duration):
        
        self.search_type = search_type
        self.club = club
        self.date = date
        self.initial_time = inital_time
        if final_time == "24:00" or final_time == "00:00":
            self.final_time = "23:59"
        else: 
            self.final_time = final_time
        self.match_duration = match_duration
        self.result = list()
        self.error = None

    def scrape(self):
        if self.club.web_scraper == "tcpmatchpoint-fixed" or self.club.web_scraper == "tcpmatchpoint-free":
            try: 
                self.result = tcp_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time, self.match_duration)
            except:
                self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}."    

        else:
            return


        