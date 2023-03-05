import json
from pathlib import Path
from time import sleep
from multisearch import MultiSearch

def get_searches():
    try:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
        searches_data = json.loads(lines)
        searches = []
        for search_dict in searches_data:
            search = MultiSearch("","","","")
            search.club_ids = search_dict["club_ids"]
            search.date = search_dict["date"]
            search.initial_search_time_str = search_dict["initial_search_time_str"]
            search.final_search_time_str = search_dict["final_search_time_str"]
            search.id = search_dict["id"]
            search.started_at = search_dict["started_at"]
            search.finished_at = search_dict["finished_at"]
            search.processing_time = search_dict["processing_time"]
            search.state = search_dict["state"]
            search.results = search_dict["results"]
            search.errors = search_dict["errors"]
            searches.append(search)
    except:
        searches = []
    return searches  

def get_next_search():
    searches = get_searches()
    for search in searches:
        if search.state == "pending":
            return search
    return None   

def save_searches(searches):
    searches_data = [search.__dict__ for search in searches]
    searches_json = json.dumps(searches_data)
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'w') as searches:
        searches.write(searches_json)

def run_next_search(): 
    searches = get_searches()   
    for search in searches:
        if search.state == "pending":
            search.state = "running"
            current_search = search
            break
    save_searches(searches)    
    current_search.scrape()
    searches = get_searches() 
    for search in searches:
        if search.id == current_search.id:
            search.started_at = str(current_search.started_at)
            search.finished_at = str(current_search.finished_at)
            search.processing_time = current_search.processing_time
            search.state = current_search.state
            search.results = current_search.results
            search.errors = current_search.errors
            break
    save_searches(searches)
    print(f"Finished search {current_search.id} in {current_search.processing_time} seconds, scraping a total of {len(current_search.club_ids)} clubs, with {len(current_search.results)} results.")        



if __name__ == "__main__":
    while True:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
        if len(lines) == 0:
            sleep(0.5)
        else:
            next_search = get_next_search()
            if next_search is None:
                sleep(0.5)
            else:
                run_next_search()

  
            


        
   
