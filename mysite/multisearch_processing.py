import json
from pathlib import Path
from time import sleep
from multisearch import MultiSearch

def get_next_search(lines):
    searches_data = json.loads(lines)
    for search_dict in searches_data:
        search = MultiSearch(**search_dict)
        if search.state == "pending":
            return search
    return None    

def run_next_search():
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
        lines = searches.read()
    searches_data = json.loads(lines)
    searches = []
    for search_dict in searches_data:
        search = MultiSearch(**search_dict)
        searches.append(search)
       
    for search in searches:
        if search.state == "pending":
            search.state = "running"
            current_search = search
            break

    searches_data = [search.__dict__ for search in searches]
    searches_json = json.dumps(searches_data)
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'w') as searches:
        searches.write(searches_json)

    results = current_search.scrape()

    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
        lines = searches.read()
    searches_data = json.loads(lines)
    searches = []
    for search_dict in searches_data:
        search = MultiSearch(**search_dict)
        searches.append(search)
       
    for search in searches:
        if search.id == current_search.id:
            search = current_search
            break

    searches_data = [search.__dict__ for search in searches]
    searches_json = json.dumps(searches_data)
    with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'w') as searches:
        searches.write(searches_json)    



if __name__ == "__main__":
    while True:
        with open(f"{str(Path(__file__).parent)}/multisearch_jobs.json", 'r') as searches:
            lines = searches.read()
        if len(lines) == 0:
            sleep(0.5)
        else:
            next_search = get_next_search(lines)
            if next_search is None:
                sleep(0.5)
            else:
                run_next_search()

  
            


        
   
