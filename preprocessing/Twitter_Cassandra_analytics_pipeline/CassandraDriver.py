import TOKENS
import time
class CassandraAPI(object):
	def __init__(self):
		from cassandra.cluster import Cluster
		cluster = Cluster()
		session = cluster.connect(TOKENS.cassandra_cluster)

	def TestSupport(self):		
		self.aaa=10






		


