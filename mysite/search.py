from tcpmatchpoint_scraper import scraper as tcp_scraper

class ClubSearch:
    """
    Creates a Search that defines the scope of the court web scrapping for 1 club, and performs it
    """

    def __init__(self, search_type, club, date, inital_time, final_time):
        
        self.search_type = search_type
        self.club = club
        self.date = date
        self.initial_time = inital_time
        self.final_time = final_time
        self.result = list()

    def scrape(self):
        if self.club.web_scraper == "tcpmatchpoint-fixed" or self.club.web_scraper == "tcpmatchpoint-free":
            self.result = tcp_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time)

        else:
            return


        