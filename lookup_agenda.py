#!/usr/bin/env python3
import sys
from db_table import db_table

# This class accepts panda data frame as data and insert corresponding rows to
# the created table.
class lookup_agenda:
	def __init__(self):
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

	# This function looks up the matching session whose attribute=value
	# If it contains subsessions, it will also return its subsessions too using find_subsessions function.
	def lookup(self, attribute, value):
		targets = self.sessions.select([], { attribute: value })
		result = ""
		existing = [target["session_id"] for target in targets]
		for target in targets:
			if target["subsessions"] == '':
				result += self.data_to_output(target)
			else:
				subsessions = target["subsessions"].split(" ; ")
				result += self.data_to_output(target) + self.find_subsessions(existing, subsessions)
		if result == "" :
			result = "There is no matching session with your request of "+attribute+"="+value+"\n"
		return result

		
	# This is a helper function for lookup. It will generate output string of subsessions that 
	# has the same session_id of subsessions elements.
	def find_subsessions(self, existing, subsessions):
		result = ""
		for subsession in subsessions:
			if int(subsession) not in existing:
				data = self.sessions.select([], {"session_id": subsession})[0]
				data["session_type"] = data["session_type"]
				result += self.data_to_output(data)
		return result

	def data_to_output(self, data):
		return data["title"] + "\t" + data["location"] + "\t" + data["date"] + "\t" + data["time_start"] + "\t" + data["time_end"] + "\t" + data["session_type"] + "\t" + data["speaker"] + "\t" + data["description"] + "\n"


if __name__ == "__main__":
	

	if len(sys.argv) < 3:
		sys.exit("You must specify column and value. (eg. python3 lookup_agenda.py column value)")
	columns = ["date", "time_start", "time_end", "title", "location", "description", "speaker"]

	# get command line argument as column and value
	column = sys.argv[1]

	# if value is not enclosed with "", it will join them and consider it as one value.
	value = " ".join(sys.argv[2:])
	if column not in columns:
		sys.exit("Your column argument must be one of the following : " + ", ".join(columns))


	la = lookup_agenda()
	resulting_elements = "Title\tLocation\tDate\tTime Start\tTime End\tType\tSpeakers\tDescription\n\n"
	print(resulting_elements)
	print(la.lookup(column, value))



