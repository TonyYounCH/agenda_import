# pip3 install pandas xlrd 
import sys
import pandas as pd
from db_table import db_table

# This class accepts panda data frame as data and insert corresponding rows to
# the created table.
class import_agenda:
	def __init__(self, data):
		self.data = data
		self.length = len(self.data["sessiont_date"])
		self.sessions = db_table("sessions", 
								{ 
									"session_id": "integer PRIMARY KEY", 
									"sessiont_date": "varchar(16) NOT NULL", 
									"time_start": "varchar(16) NOT NULL",
									"time_end": "varchar(16) NOT NULL",
									"session_type": "varchar(16) NOT NULL",
									"session_title": "text NOT NULL",
									"session_location": "text DEFAULT ''",
									"session_description": "text DEFAULT ''",
									"session_speakers": "text DEFAULT ''",
									"subsessions": "text DEFAULT ''",
								})

	def insert_data(self):
		# Index for current excel file must start with 14
		for i in range(14, self.length):
			session_id = i
			sessiont_date = self.data["sessiont_date"][i]
			time_start = self.data["time_start"][i]
			time_end = self.data["time_end"][i]
			session_type = self.data["session_type"][i]
			session_title = self.data["session_title"][i]
			session_location = self.data["session_location"][i]
			session_description = self.data["session_description"][i]
			# session speakers are separated with " ; " instead of "; " in order to
			# be selected by query with %LIKE%.
			session_speakers = self.data["session_speakers"][i].replace("; ", " ; ")
			subsessions = ""

			# subsessions attribute is "" when there exists no subsessions.
			# If there are any, subsessions attribute will have each subsessions'
			# id separated with " ; ".  
			if session_type == "Session" and i + 1 < self.length :
				subsessions = self.find_subsessions(self.data["session_type"], i+1)

			# insert into sessions table
			self.sessions.insert({ 
				"session_id": session_id, 
				"sessiont_date": sessiont_date, 
				"time_start": time_start,
				"time_end": time_end,
				"session_type": session_type,
				"session_title": session_title,
				"session_location":session_location,
				"session_description": session_description,
				"session_speakers": session_speakers,
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
	excel_data_df = pd.read_excel(sys.argv[1], keep_default_na=False).rename(columns=
		{
		"Whova Agenda Excel Template": "sessiont_date", 
		"Unnamed: 1": "time_start",
		"Unnamed: 2": "time_end",
		"Unnamed: 3": "session_type",
		"Unnamed: 4": "session_title",
		"Unnamed: 5": "session_location",
		"Unnamed: 6": "session_description",
		"Unnamed: 7": "session_speakers",
		})

	data = excel_data_df.to_dict()
	ia = import_agenda(data)
	ia.insert_data()
	print(sys.argv[1] + " has been successfully imported and inserted into db.")



