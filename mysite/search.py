from tcpmatchpoint_scraper import scraper as tcp_scraper
from tcpmatchpoint_scraper2 import scraper as tcp_scraper2
from easycancha_scraper import scraper as easy_scraper
from easycancha_scraper2 import scraper as easy_scraper2
from playtomic_scraper import scraper as play_scraper

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
        if self.club.web_scraper == "tcpmatchpoint":
            try: 
                self.result = tcp_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time, self.match_duration)
            except:
                self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}."

        elif self.club.web_scraper == "easycancha":
            try: 
                self.result = easy_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time, self.match_duration)
            except:
                self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}." 

        # elif self.club.web_scraper == "playtomic":
        #     try: 
        #         self.result = play_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time, self.match_duration)
        #     except:
        #         self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}."                    

        else:
            return
        
class ClubSearch2:
    """
    Creates a Search that defines the scope of the court web scrapping for 1 club, and performs it
    """

    def __init__(self, club, date):
        
        self.club = club
        self.date = date
        self.result = list()
        self.error = None

    def scrape(self, initial_search_time_str, final_search_time_str):
        if self.club.web_scraper == "tcpmatchpoint":
            try: 
                self.result = tcp_scraper2(self.club, self.date, initial_search_time_str, final_search_time_str)
            except:
                self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}."

        elif self.club.web_scraper == "easycancha":
            try: 
                self.result = easy_scraper2(self.club, self.date, initial_search_time_str, final_search_time_str)
            except:
                self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}." 

        # elif self.club.web_scraper == "playtomic":
        #     try: 
        #         self.result = play_scraper(self.search_type, self.club, self.date, self.initial_time, self.final_time, self.match_duration)
        #     except:
        #         self.error = f"Error while scraping {self.club.name} with {self.club.web_scraper}."                    

        else:
            return        


        