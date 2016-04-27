# -*- coding: utf-8 -*-

'''
============================================================================
Name        : Tweets_cassandra.py
Author      : Piyush
Contributer:
Version     : 1
Copyright   : DS
Description : 
This module  (documention from Tweepy) is the singular entry point for using many twitter api searchs which includes
1. Getting Tweets from own timeline .
2. Getting Tweets from Someone else's timeline.
3. Searching Tweets based off of a keyword.
4. Doing all of the above using pagination. (This will be useful when we do analytics in batch)
5. Few more like, number of users you are following, number of users who follow you, 
a script to followeveryone who follows you 

I created this file so that we don't spend time looking over a functionality again.
If you find somemore functionalities, Please Go ahead and make a functon for that. 

But mention your name too in the function Description ( or just comment it) and 
add yourself to the Contributer. (Maybe a little description of the function? ) 
============================================================================
'''

import re
import tweepy
import sys
from CassandraDriver import CassandraAPI
from CassandraDriver import TOKENS
from CassandraDriver import time
import thread
import time
from pyspark import SparkContext
from nltk.corpus import stopwords
import json
#from __future__ import print_function
import sys
from operator import add
from operator import itemgetter
#Import secret phrase module

#Reference API
# http://tweepy.readthedocs.org/en/v3.5.0/api.html


class TweetAPI(CassandraAPI):
   

   def __init__(self):
      CassandraAPI.__init__(self)
      self.consumer_key = TOKENS.consumer_key
      self.consumer_secret = TOKENS.consumer_secret
      self.access_token=TOKENS.access_token
      self.access_token_secret=TOKENS.access_token_secret
      self.tweetlist=[]
      self.numb=0
      self.repetations = 20

      



   def Connect(self):		
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,timeout=5)
   
   def TimelineTweet(self):	# View timeline tweets
		public_tweets = self.api.home_timeline()
		for tweet in public_tweets:
		    print tweet.text
		    raw_input("")
	
   def UserFollower(self):	# Get followers list, friend list
      #user = self.api.get_user('sivapalakurthi')
      user = self.api.get_user('sivapalakurthi')
      print user.screen_name
      print user.followers_count
      for friend in user.friends():
         print friend.screen_name

   def Pagination(self):
		for friend in tweepy.Cursor(self.api.friends).items():
			# Process the friend here
			print friend.screen_name

   def FriendTimeline(self):
		for status in tweepy.Cursor(self.api.friends_timeline).items(200):
			print status

	#This function follows every followers in your list.
   def FollowEveryFollower(self):
		for follower in tweepy.Cursor(self.api.followers).items():
			follower.follow()   			
			#raw_input("")
   def UserSelfTimeline(self):	#My tweets
		for status in tweepy.Cursor(self.api.user_timeline).items():
			print status.text
			raw_input("")

   '''
   So far we have just demonstrated pagination iterating per an item. 
   What if instead you want to process per a page of results? 
   '''
   def UserSelfTimeline_page(self):
   		for page in tweepy.Cursor(self.api.user_timeline).pages():
   			print page[0].text
   			raw_input("")


   def UsersTimeline(self):
   		for status in tweepy.Cursor(self.api.user_timeline, id="realDonaldTrump").items():
   			print status.text
   			raw_input("")

   def UsersLimits(self):
		for status in tweepy.Cursor(self.api.user_timeline).items(2):
			print status.text

   def UserLimits_pages(self):
		for page in tweepy.Cursor(self.api.user_timeline).pages(3):
			print page

   # https://dev.twitter.com/rest/public/search

   def SearchAPI_nonCursor(self):
      #tweetlist=[]
      for i in range(100000):
         try:
            results = self.api.search(q="Potter OR Khalifa OR Harry OR Dog OR Cat",lang="en",locale="en",count=100)
            for every in results:
               tweetlist.append(every.text)


            print i, "--- >",len(tweetlist),"--->",len(set(tweetlist))
         except:
            print "sleeping ..."
            time.sleep(15*60)

         
         
         #print "bankai",len(results)
         #print i, "----> ",  len(results)
         #for each in results:
         #   print each.text
         #raw_input("")


   def SearchAPI(self):
      
      try:
         for i,tweet in enumerate(tweepy.Cursor(self.api.search,q="Donald OR Trump OR DonaldTrump OR Donald trump OR trump ",lang="en",locale="en",count=100).items()):
            '''
            print "i= ",i," ", "Tweet= ",tweet.text
            self.tweetlist.append(tweet.text)
            print dir(tweet)
            print tweet.text
            print tweet.possibly_sensitive
            print tweet.coordinates
            print tweet.favorite_count
            print tweet.geo
            print tweet.place
            break
            '''
            print i
            #break
            #if (i%10==0):
            #print "TRY Length of tweets = ", len(self.tweetlist)
            self.numb=i
            #print "TRY Length of unique tweets = ",len(set(self.tweetlist))            
            #print "TRY Numb = ",self.numb,"\n\n\n"
               #raw_input("")
         #self.numb+=i
         #print "TRY (FOR) Numb = ",self.numb 
         #print "TRY (FOR) Length of tweets = ", len(self.tweetlist)
         #print "TRY (FOR) Length of unique tweets = ",len(set(self.tweetlist))

      except:

         #print "EXCEPT Sleeping ..."
         #print "EXCEPT numb= ",self.numb
         #print "EXCEPT Length of tweets = ", len(self.tweetlist)
         #print "EXCEPT Length of unique tweets = ",len(set(self.tweetlist)),"\n\n\n"

         if(len(set(self.tweetlist)) < 15000):
            self.SearchAPI()

         #print "Unexpected error:", sys.exc_info()[0]
      
      finally:
         print "FINALLY len(self.tweetlist)= ",len(self.tweetlist)
         print "FINALLY numb = ", self.numb
         self.tweetlist=[]
         self.numb=0
         #self.TestTimeout2()


   def WordCloud(self,twitter_tags_list,politician_table,repeat):
      if(repeat == "NO"):
      
         #logFile = "/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/data.json"  # Should be some file on the server
         sc = SparkContext("local", "Simple App")
         #logData = sc.textFile(logFile).cache()
         #numAs = logData.filter(lambda s: 'a' in s).count()
         #numBs = logData.filter(lambda s: 'b' in s).count()
         
         #print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
      


      if(politician_table=="donaldtrumpttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO donaldtrumpttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?) USING TTL 3600")
         #self.prepared_retrive_tweets = self.session.prepare("SELECT * FROM donaldtrumpttl LIMIT 100")
      elif(politician_table=="hillaryclintonttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO hillaryclintonttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?) USING TTL 3600")
         #self.prepared_retrive_tweets = self.session.prepare("SELECT * FROM hillaryclintonttl LIMIT 100")
      elif(politician_table=="berniesandersttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO berniesandersttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?) USING TTL 3600")
         #self.prepared_retrive_tweets = self.session.prepare("SELECT * FROM berniesandersttl LIMIT 100")
      elif(politician_table=="tedcruzttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO tedcruzttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?) USING TTL 3600")
         #self.prepared_retrive_tweets = self.session.prepare("SELECT * FROM tedcruzttl LIMIT 100")
      elif(politician_table=="johnkasichttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO johnkasichttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?) USING TTL 3600")
         #self.prepared_retrive_tweets = self.session.prepare("SELECT * FROM johnkasichttl LIMIT 100")
      values=[]
      executestmt=None
      rows=None
      #rows_wordcloud=None
      textlist=None
      textlist_wordcloud=None
      ftextlist_wordcloud_bigfile= open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/BigWordCloudFile.txt","w")
      IBMToneJSON=None
      WordCloudJSON=None

   #try:
      for i,tweet in enumerate(tweepy.Cursor(self.api.search,q=str(twitter_tags_list),lang="en",locale="en",count=100).items()):
         print "Inside for ",i         
         textlist=[]
         rows=None
         #rows_wordcloud=None
         IBMToneJSON=None
         WordCloudJSON=None
         if(i>2 and  (i%(self.repetations) == 0)):         
            if(politician_table=="donaldtrumpttl"):
               rows = self.session.execute("SELECT tweet_text FROM donaldtrumpttl LIMIT 100")
               #rows_wordcloud = self.session.execute("SELECT tweet_text FROM donaldtrumpttl")
            elif(politician_table=="hillaryclintonttl"):
               rows = self.session.execute("SELECT tweet_text FROM hillaryclintonttl LIMIT 100")
               #rows_wordcloud = self.session.execute("SELECT tweet_text FROM hillaryclintonttl")
            elif(politician_table=="berniesandersttl"):
               rows = self.session.execute("SELECT tweet_text FROM berniesandersttl LIMIT 100")
               #rows_wordcloud = self.session.execute("SELECT tweet_text FROM berniesandersttl")
            elif(politician_table=="tedcruzttl"):
               rows = self.session.execute("SELECT tweet_text FROM tedcruzttl LIMIT 100")
               #rows_wordcloud = self.session.execute("SELECT tweet_text FROM tedcruzttl")
            elif(politician_table=="johnkasichttl"):
               rows = self.session.execute("SELECT tweet_text FROM johnkasichttl LIMIT 100")
               #rows_wordcloud = self.session.execute("SELECT tweet_text FROM johnkasichttl")            
            
            IBMToneJSON=None
            WordCloudJSON=None
            if(len(textlist)!=0):
               textlist=[]
            for each in rows:
               textlist.append(each['tweet_text'])


            #Filter
            textlist= (" ").join(textlist).lower()
            #textlist_wordcloud= textlist
            textlist = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', textlist)
            textlist_wordcloud = textlist
            IBMToneJSON = eval(json.dumps(self.tone_analyzer.tone(text=textlist)))
            stop = stopwords.words('english')
            textlist_wordcloud =[i for i in textlist_wordcloud.split() if i not in stop]
                       
            textlist_wordcloud= (" ").join(textlist_wordcloud)
            ftextlist_wordcloud_bigfile.write(textlist_wordcloud.encode('utf-8'))
            textlist_wordcloud=[]

            lines = sc.textFile("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/BigWordCloudFile.txt")
            counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
            output = counts.collect()
            output=sorted(output, key=itemgetter(1))
            output = output[:20]
            


            WordCloudJSON_1=open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/data.json","w")
            each4_list_names=[]
            each4_list_numbers=[]



            #Anger, Disgust, Fear, Joy, Sadness
            IBMToneJSON_1= open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/testdata1.json","w")
            each1_list_names=[]
            each1_list_numbers=[]


            IBMToneJSON_2= open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/testdata2.json","w")
            each2_list_names=[]
            each2_list_numbers=[]

            IBMToneJSON_3= open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/testdata3.json","w")
            each3_list_names=[]
            each3_list_numbers=[]




            for (word, count) in output:
               each4_list_names.append(word)
               each4_list_numbers.append(count)

            #print IBMToneJSON['document_tone']['tone_categories'][2]['tones']
            #exit()
            for each in IBMToneJSON['document_tone']['tone_categories'][0]['tones']:
               each1_list_names.append(each['tone_name'])
               each1_list_numbers.append(each['score'])
            
            for each in IBMToneJSON['document_tone']['tone_categories'][1]['tones']:
               each2_list_names.append(each['tone_name'])
               each2_list_numbers.append(each['score'])

            for each in IBMToneJSON['document_tone']['tone_categories'][2]['tones']:
               each3_list_names.append(each['tone_name'])
               each3_list_numbers.append(each['score'])



            #IBMToneJSON_1.write( '[{ \"year\" : \" "+each1['tone_name']+" \", "" '    )   
            IBMToneJSON_1.write('['+'{"year":"Anger", "income": ' +str(each1_list_numbers[0])+ ' },'+ '{"year":"Disgust", "income": ' +str(each1_list_numbers[1])+ ' },'+'{"year":"Fear", "income": ' +str(each1_list_numbers[2])+ ' },'+ '{"year":"Joy", "income": ' +str(each1_list_numbers[3])+ ' },'+ '{"year":"Saddness", "income": ' +str(each1_list_numbers[4])+ ' }'+']' )            
            IBMToneJSON_1.close()

            IBMToneJSON_2.write('['+'{"year":"Analytical", "income": ' +str(each2_list_numbers[0])+ ' },'+ '{"year":"Confident", "income": ' +str(each2_list_numbers[1])+ ' },'+'{"year":"Tentative", "income": ' +str(each2_list_numbers[2])+ ' }'+']' )            
            IBMToneJSON_2.close()

            IBMToneJSON_3.write('['+'{"year":"Openness", "income": ' +str(each3_list_numbers[0])+ ' },'+ '{"year":"Conscientiousness", "income": ' +str(each3_list_numbers[1])+ ' },'+'{"year":"Extraversion", "income": ' +str(each3_list_numbers[2])+ ' },'+ '{"year":"Agreeableness", "income": ' +str(each3_list_numbers[3])+ ' },'+ '{"year":"Emotional Range", "income": ' +str(each3_list_numbers[4])+ ' }'+']' )            
            IBMToneJSON_3.close()

            WordCloudJSON_1.write('['+'{"key": \"'  + (each4_list_names[0]).replace("\"","").encode('utf-8')+'\", "value": ' +str(each4_list_numbers[0])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[1]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[1])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[2]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[2])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[3]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[3])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[4]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[4])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[5]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[5])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[6]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[6])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[7]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[7])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[8]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[8])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[9]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[9])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[10]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[10])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[11]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[11])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[12]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[12])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[13]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[13])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[14]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[14])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[15]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[15])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[16]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[16])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[17]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[17])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[18]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[18])+ ' },')
            WordCloudJSON_1.write('{"key": \" '  + (each4_list_names[19]).replace("\"","").encode('utf-8')+'\" , "value": ' +str(each4_list_numbers[19])+ ' }]')
            WordCloudJSON_1.close()
            #time.sleep(10)
      







            '''
            [{"key": "fish", "value": 11},{"key": "things", "value": 12},{"key": "look", "value": 13}]
            '''


            #[{"year": "Anger","income": 23.5},{"year": "Disgust","income": 26.2},{"year": "Fear","income": 30.1},{"year": "Joy","income": 29.5},{"year": "Sadness","income": 24.6}]


            #print 
            #exit()
            #print json.dumps(self.tone_analyzer.tone(text=textlist), indent=2)
         values=[]
         rows=None
         values.append(tweet.id)
         values.append(tweet.lang.replace("'",""))
         values.append(tweet.text.replace("'",""))            
         values.append(tweet.created_at)
         values.append(tweet.retweet_count)
         binding_stmt = self.prepared_insert_tweets.bind(values)
         executestmt=self.session.execute(binding_stmt)
         
      
   #except:
      #print "Inside except ",i
      if(len(set(self.tweetlist)) < 100000):
         self.WordCloud(twitter_tags_list,politician_table,"YES")
   #finally:
      #print "Inside finally ",i
      #print "FINALLY len(self.tweetlist)= ",len(self.tweetlist)
      #print "FINALLY numb = ", self.numb
      self.tweetlist=[]
      #self.TestTimeout2()


if __name__ == "__main__":
   tweets =  TweetAPI()
   tweets.Connect()
   #tweets.TestIBM()
   #tweets.SearchAPI()
   

   #tweets.TestIBM()
   tweets.WordCloud("Donald OR Trump OR DonaldTrump OR Donald trump OR trump ","donaldtrumpttl","NO")  #REMOVE THE BREAK STATEMENT

