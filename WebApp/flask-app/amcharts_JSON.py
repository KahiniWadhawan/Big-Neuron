'''
	Author: Piyush Patel, Tanvi Parikh
	Purpose: Customize the JSON produced by IBM tone analyser to a format acceptable by Amcharts for rendition
	Documentation:
		This file will crunch the json from data/tone.json
		And output three files
			data/emotion.json
			data/

	Example Current input:
	{
	   "document_tone":{
	      "tone_categories":[
	         {
	            "category_id":"emotion_tone",
	            "tones":[
	               {
	                  "tone_name":"Anger",
	                  "score":0.25653,
	                  "tone_id":"anger"
	               },
	               {
	                  "tone_name":"Disgust",
	                  "score":0.109379,
	                  "tone_id":"disgust"
	               },
	               {
	                  "tone_name":"Fear",
	                  "score":0.012457,
	                  "tone_id":"fear"
	               },
	               {
	                  "tone_name":"Joy",
	                  "score":0.002487,
	                  "tone_id":"joy"
	               },
	               {
	                  "tone_name":"Sadness",
	                  "score":0.192886,
	                  "tone_id":"sadness"
	               }
	            ],
	            "category_name":"Emotion Tone"
	         } ]
	    }
	}

	Example Required Output:
	[{
	  "tone_name":"Anger",
	  "score":20,
	  "tone_id":"anger"
	},{
	  "tone_name":"Disgust",
	  "score":20,
	  "tone_id":"disgust"
	},{
	  "tone_name":"Fear",
	  "score":20,
	  "tone_id":"fear"
	},{
	  "tone_name":"Joy",
	  "score":20,
	  "tone_id":"joy"
	},{
	  "tone_name":"Sadness",
	  "score":20,
	  "tone_id":"sadness"
	}]
'''
import json

f = open("static/data/tone.json", "r")

a = f.read()
a= eval (a)
l1,l2,l3 =  a['document_tone']['tone_categories'][0]['tones'],a['document_tone']['tone_categories'][1]['tones'],a['document_tone']['tone_categories'][2]['tones']
with open('static/data/emotion.json', 'w') as outfile:
    json.dump(l1, outfile)
with open('static/data/writing.json', 'w') as outfile:
    json.dump(l2, outfile)
with open('static/data/social.json', 'w') as outfile:
    json.dump(l3, outfile)
