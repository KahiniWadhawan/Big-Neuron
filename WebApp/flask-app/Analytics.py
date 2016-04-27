import TOKENS
import json

class IBMToneAnalyzer(object):
	def __init__(self):
		from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer
		self.tone_analyzer = ToneAnalyzer(
			username=TOKENS.ibm_username,
			password=TOKENS.ibm_password,
			version='2016-02-11')
	def TestIBM(self):
		print "IBM function"
		print(json.dumps(self.tone_analyzer.tone(text='I am very happy'), indent=2))
		print "Program Exiting"
		exit()
