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
'''
f = open("static/data/tone.json", "r")
a = f.read()
a = eval (a)
l1,l2,l3 =  a['document_tone']['tone_categories'][0]['tones'], a['document_tone']['tone_categories'][1]['tones'], a['document_tone']['tone_categories'][2]['tones']

with open('static/data/emotion.json', 'w') as outfile:
    json.dump(l1, outfile)
with open('static/data/writing.json', 'w') as outfile:
    json.dump(l2, outfile)
with open('static/data/social.json', 'w') as outfile:
    json.dump(l3, outfile)
'''

def organize_dumpfiles(cand):
    if cand == "clinton":
        f1, f2, f3 = "static/data/clinton/emotion.json", "static/data/clinton/writing.json", "static/data/clinton/social.json"
    elif cand == "cruz":
        f1, f2, f3 = "static/data/cruz/emotion.json", "static/data/cruz/writing.json", "static/data/cruz/social.json"
    elif cand == "kasich":
        f1, f2, f3 = "static/data/kasich/emotion.json", "static/data/kasich/writing.json", "static/data/kasich/social.json"
    elif cand == "sanders":
        f1, f2, f3 = "static/data/sanders/emotion.json", "static/data/clinton/sanders.json", "static/data/sanders/social.json"
    elif cand == "trump":
        f1, f2, f3 = "static/data/trump/emotion.json", "static/data/trump/writing.json", "static/data/trump/social.json"
    return f1, f2, f3

def dump(f1, f2, f3, l1, l2, l3):
    with open(f1, 'w') as outfile1:
        json.dump(l1, outfile1)
    with open(f2, 'w') as outfile2:
        json.dump(l2, outfile2)
    with open(f3, 'w') as outfile3:
        json.dump(l3, outfile3)

def clean_json_data(rawData):
    a = eval( rawData )
    return a['document_tone']['tone_categories'][0]['tones'], a['document_tone']['tone_categories'][1]['tones'], a['document_tone']['tone_categories'][2]['tones']


def dump_json_data(cand, rawData):
    if cand == "clinton":
        emo, wri, soc = clean_json_data(rawData)
        f1, f2, f3 = organize_dumpfiles("clinton")
    elif cand == "cruz":
        emo, wri, soc = clean_json_data(rawData)
        f1, f2, f3 = organize_dumpfiles("cruz")
        dump(f1, f2, f3, l1, l2, l3)
    elif cand == "kasich":
        emo, wri, soc = clean_json_data(rawData)
        f1, f2, f3 = organize_dumpfiles("kasich")
    elif cand == "sanders":
        emo, wri, soc = clean_json_data(rawData)
        f1, f2, f3 = organize_dumpfiles("sanders")
    elif cand == "trump":
        emo, wri, soc = clean_json_data(rawData)
        f1, f2, f3 = organize_dumpfiles("trump")
    else:
        print "Error: Invalid candidate name."
    
    dump(f1, f2, f3, emo, wri, soc)
        
        

if __name__ == "__main__":
    pass #write test code here!  Pass in dummy data to test this module.