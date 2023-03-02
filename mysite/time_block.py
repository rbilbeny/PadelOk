from datetime import datetime

class TimeBlock:
	"""
	Creates an object that represents the available block of time in which a court is available to play in
	"""

	def __init__(self, club_id, date, initial_time, final_time, court_name, court_value):
		
		self.club_id = club_id
		self.date = str(datetime.strptime(date, '%d/%m/%Y'))
		self.initial_time = initial_time
		self.final_time = final_time
		self.court_name = court_name
		self.court_value = court_value
		self.duration_text = ""

	def save_block_duration_text(self):
		initial_time = datetime.strptime(self.initial_time, "%H:%M")
		final_time = datetime.strptime(self.final_time, "%H:%M")
		duration = final_time - initial_time
		if duration.total_seconds()/60 == 60:
			self.duration_text = "1 h"
		elif duration.total_seconds()/60 == 90:
			self.duration_text =  "1,5 hrs"
		elif duration.total_seconds()/60 == 120:
			self.duration_text =  "2 hrs"
		elif duration.total_seconds()/60 == 150:
			self.duration_text =  "2,5 hrs"
		elif duration.total_seconds()/60 == 180:
			self.duration_text =  "3 hrs"
		elif duration.total_seconds()/60 == 240:
			self.duration_text =  "4 hrs"

		return 

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

