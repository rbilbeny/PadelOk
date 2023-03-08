class TimeBlock2:
	"""
	Creates an object that represents the available block of time in which a court is available to play in
	"""

	def __init__(self, club_id, initial_time, final_time, court_name, match_duration, court_value, court_size):
		
		self.club_id = club_id
		self.initial_time = initial_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		self.final_time = final_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		self.court_name = court_name
		self.match_duration = match_duration
		self.court_value = court_value
		self.court_size = court_size

