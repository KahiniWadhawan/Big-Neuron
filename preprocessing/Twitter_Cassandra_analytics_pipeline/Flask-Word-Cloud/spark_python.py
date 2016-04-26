'''
============================================================================
Name        : tweet_cassandra_analytic_api.py
Author      : Piyush
Contributer:
Version     : 1
Copyright   : DS
Description : 

Wordcloud with Apache spark


============================================================================
'''

from pyspark import SparkContext
from tweet_cassandra_analytic_api import TweetAPI
from nltk.corpus import stopwords

class SparkAPI(TweetAPI):
	def __init__(self):
		TweetAPI.__init__(self)
		#TweetAPI.Connect(self)

		
		self.logFile = "/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/data.json"  # Should be some file on the server
		'''
		self.sc = self.SparkContext("local", "Simple App")
		self.logData = sc.textFile(self.logFile).cache()
		self.numAs = self.logData.filter(lambda s: 'a' in s).count()
		self.numBs = self.logData.filter(lambda s: 'b' in s).count()
		'''
		self.politician_name="Donald"
		self.twitter_tags_list="Donald OR Trump OR DonaldTrump OR Donald trump OR trump"
		self.politician_table= "donaldtrumpttl"




if __name__== "__main__":
	print "Spark module loaded succesfully"
	
	logFile = "/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/data.json"  # Should be some file on the server
	sc = SparkContext("local", "Simple App")
	logData = sc.textFile(logFile).cache()
	numAs = logData.filter(lambda s: 'a' in s).count()
	numBs = logData.filter(lambda s: 'b' in s).count()
	print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
	

	SparkCloud = SparkAPI()
	SparkCloud.Connect()

	
	if (SparkCloud.politician_name == "Donald"):
		SparkCloud.WordCloud(SparkCloud.twitter_tags_list,SparkCloud.politician_table)
	
	







	