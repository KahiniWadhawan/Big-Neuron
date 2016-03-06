# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import ToneAnalyzerV3Beta as ToneAnalyzer

tone_analyzer = ToneAnalyzer(username='f7c9ae7a-a947-41b0-81e9-8ff1ae0e6084',
                             password='zLbkmbouGY8m',
                             version='2016-02-11')

text = "The IBM Watson™ Tone Analyzer Service uses linguistic analysis to detect three types of tones from written text emotions, social tendencies, and writing style. Emotions identified include things like anger, cheerfulness and sadness. Identified social tendencies include things from the Big Five personality traits used by some psychologists."

print(json.dumps(tone_analyzer.tone(text=text), indent=2))
