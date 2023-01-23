import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from search import ClubSearch
from club import Club


def handle_request_post_clubs(input_text):
    input_text = input_text.replace('\\', "")
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]    
    
    #LOCAL EQUALS WEB
    json_clubs = line
    return {"result" : json_clubs}




def handle_request_get_single_scraper(club_id, date, inital_time, final_time): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    #LOCAL EQUALS WEB
    club = Club(line, club_id)
    single_club_search = ClubSearch(club, date, inital_time, final_time)
    single_club_search.scrape()
    search_result_list = []
    for court in single_club_search.result:
        search_result_list.append(court.__dict__)

    json_courts = json.dumps(search_result_list, indent=4)
    return json_courts

'''
def handle_request_get_multi_scraper(clubs_ids, initial_date, final_date, inital_time, final_time): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]
    
    #LOCAL EQUALS WEB
            start_date = datetime.strptime(self.initial_date, "%d/%m/%Y")
            end_date = datetime.strptime(self.final_date, "%d/%m/%Y")
            delta = timedelta(days=1)
            current_date = start_date
            while current_date <= end_date:
                self.result.extend(tcp_scraper(self.club, current_date.strftime("%d/%m/%Y"), self.initial_time, self.final_time))
                current_date += delta   

    json_courts = json.dumps(multisearch_result_list, indent=4)
    return json_courts
'''    