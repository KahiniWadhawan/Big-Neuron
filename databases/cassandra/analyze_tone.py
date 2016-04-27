#-------------------------------------------------------------------------------
#Author: Kahini Wadhawan, Piyush Patel
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
import json
import sys
#from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer
#import TOKENS

#revisit - handling relative paths file imports
class IBMToneAnalyzer(object):
	def __init__(self):
		from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer
		#Load IBM Tone Analyzer credentials
		#print('ibm tone analyzer :: ', sys.path[0])
		oauth = json.loads(open('../../config/oauth.json','r').read())

		self.tone_analyzer = ToneAnalyzer(
			username=oauth['ibm_username'],
			password=oauth['ibm_password'],
			version='2016-02-11')


	def TestIBM(self):
		print "IBM function"
		exit()


	def get_sentiment(self, text):
		#print "tweet : text :: ", text
		sentiment_json = json.dumps(self.tone_analyzer.tone(text=text), indent=2)
		return sentiment_json





