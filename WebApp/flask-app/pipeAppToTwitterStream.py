from multiprocessing import Process
import twitter_stream
class PipeIt(object):
	def runit(self,name):
		twitter_stream.loop_a(name)