'''
	Author: Tanvi Parikh
	Purpose: Customize the JSON produced by IBM tone analyser to a format acceptable by Amcharts for rendition

	Current input:
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

	Required Output:
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