'''
============================================================================
Name        : FetchData.py
Author      : Piyush
Version     : 1
Copyright   : DS
Description : 
Extract data from the Cassandra Database. The output is in the form of JSON file.
The superclass CassandraAPI is inherited and intilised in the Connect() function.
The Columns names that exists in the database are listed out in the __init__ method.

Henceforth, if any changes to the database is made (alter any columns or columns name etc..),
the same must be reflected back in the __init__ method for consistency.
============================================================================
'''
import TOKENS
from CassandraDriver import CassandraAPI
driver = CassandraAPI()

class DataFields(CassandraAPI):

	# Database columns names
	def __init__(self):
		self.counter=None
		self.tweet=None
		self.lang=None
		self.sourcee=None
		self.retweet_count=None
		self.created_at=None
		self.analytics=None

	# Connect to cassandra drivers.
	def Connect(self):
		CassandraAPI.__init__(self)

	# Fetch data from database in a resultset. later to be converted to streaming it from database by using since_ID
	#or by extracting it as a timeseries datra, which is really easy since we already have a datetime field.  
	def Fetchdata(self):
		result = self.session.execute("select tweet, sourcee , analytics from tweepy")	# Queries to the Database
		for i, each in enumerate(result):
			#print i, each
			# Convert to JSON dumps later.
			print "{ "+ "\"tweet\": "+" \" "+ each.tweet +  " \", "
			print "{ "+ "\"sourcee\": "+" \" "+ each.sourcee +  " \", "
			print "{ "+ "\"analytics\": "+" \" "+ each.analytics +  " \" "
			raw_input()




if __name__ == "__main__":
   getData= DataFields()
   #tweets.TestSupport()
   getData.Connect()
   getData.Fetchdata()
else:
   print "Redo module load"
   exit(0)







