import json

def handle_request_post_clubs(input_text):
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'w') as clubs:
        clubs.write(input_text)
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as updated_clubs:
        lines = updated_clubs.readlines()
        line = lines[0]    
    
    #LOCAL EQUALS WEB
    json_clubs = line
    return {"result" : json_clubs}

def handle_request_get_single_scraper(input_text): 
    with open("/Users/rodrigobilbeny/Documents/GitHub/PadelOk/mysite/clubs.json", 'r') as clubs:
        lines = clubs.readlines()
        line = lines[0]

    #LOCAL EQUALS WEB
    return {"address" : input_text}