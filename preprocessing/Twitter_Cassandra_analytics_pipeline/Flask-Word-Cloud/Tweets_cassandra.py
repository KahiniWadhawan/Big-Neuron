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


import tweepy
import sys

from CassandraDriver import CassandraAPI
from CassandraDriver import TOKENS
from CassandraDriver import time
import thread
import time

Repetations = 300
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
      self.repetations = 100



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


   def WordCloud(self,name,Politician_name):
      if(Politician_name=="donaldtrumpttl"):
         self.prepared_insert_tweets = self.session.prepare("INSERT INTO donaldtrumpttl (tweet_id, lang, tweet_text, created_at, retweet_count) VALUES(?,?,?,?,?)")
      values=[]
      executestmt=None
        
   #try:

      for i,tweet in enumerate(tweepy.Cursor(self.api.search,q=str(name),lang="en",locale="en",count=100).items()):
         print "Inside for ",i

         if(i>1 and  (i%(self.repetations) ==0)):
            print "...Computing..."
         print tweet.id, type(tweet.id)
         print tweet.lang,type(tweet.lang)
         print tweet.text,type(tweet.text.replace("'",""))
         print tweet.created_at,type(tweet.created_at)
         print tweet.retweet_count,type(tweet.retweet_count)
         print "\n\n\n"


         values=[]
         values.append(tweet.id)
         values.append(tweet.lang.replace("'",""))
         values.append(tweet.text.replace("'",""))            
         values.append(tweet.created_at)
         values.append(tweet.retweet_count)

         binding_stmt = self.prepared_insert_tweets.bind(values)
         #print "Before execute ",i
         executestmt=self.session.execute(binding_stmt)
         
         
   #except:
      #print "Inside except ",i
      if(len(set(self.tweetlist)) < 100000):
         self.WordCloud(name,Politician_name)
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
   tweets.WordCloud("Donald OR Trump OR DonaldTrump OR Donald trump OR trump ","donaldtrumpttl")  #REMOVE THE BREAK STATEMENT


else:
   print "Redo module load"
   exit(0)
