from concurrent.futures import ThreadPoolExecutor
from club import Club2

from tcpmatchpoint_scraper2 import scraper as tcp_scraper2
from easycancha_scraper2 import scraper as easy_scraper2

class MultiSearch:
    """
    Creates a Search that defines the scope of the court web scrapping for N clubs.
    """

    def __init__(self, club_ids, date, initial_search_time_str, final_search_time_str):
        self.club_ids = club_ids
        self.date = date
        self.initial_search_time_str = initial_search_time_str
        self.final_search_time_str = final_search_time_str
        self.results = list()
        self.errors = list()

    #This function handles the parallel scraping of all the clubs in the list using ThreadPoolExecutor as threading method
    def scrape(self):
        with ThreadPoolExecutor() as executor:
            future_to_club = {executor.submit(scrape_single_club, club_id, self.date, self.initial_search_time_str, self.final_search_time_str): club_id for club_id in self.club_ids}
            for future in future_to_club:
                if future.result()[1] is not None:
                    self.errors.append(future.result()[1])
                else:    
                    for block in future.result()[0]:
                        self.results.append(block.__dict__)
        json_courts = {"results": self.results, "errors": self.errors}                            
        return json_courts



def scrape_single_club(club_id, date, initial_search_time_str, final_search_time_str):
        single_club_results = list()
        single_club_error = None
        club = Club2(club_id)
        
        if club.web_scraper == "tcpmatchpoint":
            try: 
                single_club_results = tcp_scraper2(club, date, initial_search_time_str, final_search_time_str)
            except:
                single_club_error = f"Error while scraping {club.name} with {club.web_scraper}."

        # elif club.web_scraper == "easycancha":
        #     try: 
        #         single_club_results = easy_scraper2(club, date, initial_search_time_str, final_search_time_str)
        #     except:
        #         single_club_error= f"Error while scraping {club.name} with {club.web_scraper}."

        else :
            single_club_error.error = f"Error while scraping {club.name}: no valid scraper defined on clubs.json file."             

        return (single_club_results, single_club_error)    

