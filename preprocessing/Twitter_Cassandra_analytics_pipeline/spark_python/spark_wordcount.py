from pyspark import SparkContext
class WordCloud(object):
	"""Counts words"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.logFile = "/home/piyush/Scala_Spark_gz/spark-1.6.1/file.txt"
	def getSparkContext():
		self.sc = SparkContext("local", "Simple App")
	def cacheFile():
		self.logData = sc.textFile(self.logFile).cache()



		
#logFile = "YOUR_SPARK_HOME/README.md"  # Should be some file on your system

x = WordCloud()

numAs = x.logData.filter(lambda s: 'a' in s).count()
numBs = x.logData.filter(lambda s: 'b' in s).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))