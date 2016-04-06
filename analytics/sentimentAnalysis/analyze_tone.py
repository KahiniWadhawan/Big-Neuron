#-------------------------------------------------------------------------------
#Author: Kahini Wadhawan
#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer

def get_sentiment(text):
    #create Bluemix account to get service_username and service_password
    service_username = "fill--your---service--username"
    service_password ="fill--your---service---password"

    tone_analyzer = ToneAnalyzer(username=service_username,
                                 password=service_password,
                                 version='2016-02-11')

    sentiment_json = json.dumps(tone_analyzer.tone(text=text), indent=2)
    return sentiment_json


# text = "The IBM Watson Tone Analyzer Service uses linguistic analysis " \
#        "to detect three types of tones from written text emotions, social tendencies, " \
#        "and writing style. Emotions identified include things like anger, cheerfulness" \
#        "and sadness. Identified social tendencies " \
#        "include things from the Big Five personality traits used by some psychologists."



