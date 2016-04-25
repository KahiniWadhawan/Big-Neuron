#-------------------------------------------------------------------------------
#Author: Kahini Wadhawan, Piyush Patel
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
import json
#from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer
#import TOKENS


#-----------------------------------------------------------------
#Load IBM Tone Analyzer credentials
#------------------------------------------------------------------
oauth = json.loads(open('../../config/oauth.json','r').read())


class IBMToneAnalyzer(object):
	def __init__(self):
		from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer
		self.tone_analyzer = ToneAnalyzer(
			username=oauth['ibm_username'],
			password=oauth['ibm_password'],
			version='2016-02-11')

	def TestIBM(self):
		print "IBM function"
		exit()

	def get_sentiment(self, text):
		sentiment_json = json.dumps(tone_analyzer.tone(text=text), indent=2)
		return sentiment_json





