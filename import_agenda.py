# pip3 install pandas xlrd 
import sys
import pandas as pd
from db_table import db_table

# This class accepts panda data frame as data and insert corresponding rows to
# the created table.
class import_agenda:
	def __init__(self, data):
		self.data = data
		self.length = len(self.data["date"])
		self.sessions = db_table("sessions", 
								{ 
									"session_id": "integer PRIMARY KEY", 
									"date": "varchar(16) NOT NULL", 
									"time_start": "varchar(16) NOT NULL",
									"time_end": "varchar(16) NOT NULL",
									"session_type": "varchar(16) NOT NULL",
									"title": "text NOT NULL",
									"location": "text DEFAULT ''",
									"description": "text DEFAULT ''",
									"speaker": "text DEFAULT ''",
									"subsessions": "text DEFAULT ''",
								})

	def insert_data(self):
		# Index for current excel file must start with 14
		for i in range(14, self.length):
			session_id = i
			date = self.data["date"][i]
			time_start = self.data["time_start"][i]
			time_end = self.data["time_end"][i]
			session_type = self.data["session_type"][i]
			title = self.data["title"][i]
			location = self.data["location"][i]
			description = self.data["description"][i]
			# session speakers are separated with " ; " instead of "; " in order to
			# be selected by query with %LIKE%.
			speaker = self.data["speaker"][i].replace("; ", " ; ")
			subsessions = ""

			# subsessions attribute is "" when there exists no subsessions.
			# If there are any, subsessions attribute will have each subsessions'
			# id separated with " ; ".  
			if session_type == "Session" and i + 1 < self.length :
				subsessions = self.find_subsessions(self.data["session_type"], i+1)

			# insert into sessions table
			self.sessions.insert({ 
				"session_id": session_id, 
				"date": date, 
				"time_start": time_start,
				"time_end": time_end,
				"session_type": session_type,
				"title": title,
				"location":location,
				"description": description,
				"speaker": speaker,
				"subsessions": subsessions,
			})

	def find_subsessions(self, sessions, i):
		if sessions[i] == "Sub":
			return str(i) + " ; " + self.find_subsessions(sessions, i+1) if (i + 1 < self.length and sessions[i+1] == "Sub") else str(i)
		else:
			return ""

if __name__ == "__main__":
	
	# get command line argument as filename
	# Since current excel file does not have proper attribute names, the attribute
	# names of each column need to be chaged with rename method.
	if len(sys.argv) != 2:
		sys.exit("You must specify a filename you want to import.")

	excel_data_df = pd.read_excel(sys.argv[1], keep_default_na=False).rename(columns=
		{
		"Whova Agenda Excel Template": "date", 
		"Unnamed: 1": "time_start",
		"Unnamed: 2": "time_end",
		"Unnamed: 3": "session_type",
		"Unnamed: 4": "title",
		"Unnamed: 5": "location",
		"Unnamed: 6": "description",
		"Unnamed: 7": "speaker",
		})

	data = excel_data_df.to_dict()
	ia = import_agenda(data)
	ia.insert_data()
	print(sys.argv[1] + " has been successfully imported and inserted into db.")



