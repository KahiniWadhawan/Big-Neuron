'''
============================================================================
Name        : CassandraDriver.py
Author      : Piyush
Version     : 1
Copyright   : DS
Description : 
API's required to connect to the Cassandra database. Create object of this class and call the __init__()
method on this superclass to create an instance of the driver. ( You can test it by calling the TestSupport
method.)

============================================================================
'''
#Import keys and tokens
import TOKENS

#For using datetime functions
import time

class CassandraAPI(object):

	# Initialize the Cassandra drivers and import required tokens
	# Connect to 'Keyspace attribute' in Cassandra
	def __init__(self):
		from cassandra.cluster import Cluster
		cluster = Cluster()
		self.session = cluster.connect(TOKENS.cassandra_cluster)


	# Check if classes are prperly connected
	def TestSupport(self):		
		self.aaa=10
		print "Hello there"
		exit()






		


