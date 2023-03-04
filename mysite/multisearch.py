from concurrent.futures import ThreadPoolExecutor

from tcpmatchpoint_scraper2 import scraper as tcp_scraper2
from easycancha_scraper2 import scraper as easy_scraper2

class MultiSearch:
    """
    Creates a Search that defines the scope of the court web scrapping for N clubs
    """

    def __init__(self, clubs, date):
        self.clubs = clubs
        self.date = date
        self.results = list()
        self.errors = list()

    def scrape(self, initial_search_time_str, final_search_time_str):
        with ThreadPoolExecutor() as executor:
            future_to_club = {executor.submit(scrape_single_club, club, self.date, initial_search_time_str, final_search_time_str): club for club in self.clubs}
            for future in future_to_club:
                if future[1] is not None:
                    self.errors.append(future[1])
                else:    
                    for block in future[0]:
                        self.results.append(block)

        response= {"results": self.results, "errors": self.errors}                               
        return response



def scrape_single_club(club, date, initial_search_time_str, final_search_time_str):
        single_club_results = list()
        single_club_error = None
        
        if club.club.web_scraper == "tcpmatchpoint":
            try: 
                single_club_results = tcp_scraper2(club, date, initial_search_time_str, final_search_time_str)
            except:
                single_club_error = f"Error while scraping {club.name} with {club.web_scraper}."

        elif club.web_scraper == "easycancha":
            try: 
                single_club_results = easy_scraper2(club, date, initial_search_time_str, final_search_time_str)
            except:
                single_club_error= f"Error while scraping {club.name} with {club.web_scraper}."

        else :
            single_club_error.error = f"Error while scraping {club.name}: no valid scraper defined on clubs.json file."             

        return single_club_results, single_club_error     
            