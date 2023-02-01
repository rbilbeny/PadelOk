class TimeBlock:
    """
    Creates an object that represents the available block of time in which a court is available to play in
    """

    def __init__(self, club_id, date, initial_time, final_time, court_name, court_value):
        
        self.club_id = club_id
        self.date = date
        self.initial_time = initial_time
        self.final_time = final_time
        self.court_name = court_name
        self.court_value = court_value