'''
============================================================================
Name        : Tweets_cassandra.py
Author      : Piyush
Contributer:
Version     : 2
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
If you find somemore functionalies, Please Go ahead and make a functon for that. 

But mention your name too in the function Description ( or just comment it) and 
add yourself to the Contributer. (Maybe a little description of the function? ) 
============================================================================
'''


import tweepy
import sys

from CassandraDriver import CassandraAPI
from CassandraDriver import TOKENS
from CassandraDriver import time



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


   def Connect(self):   
    self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
    self.auth.set_access_token(self.access_token, self.access_token_secret)
    self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,timeout=5)
   
   def TimelineTweet(self): # View timeline tweets
    public_tweets = self.api.home_timeline()
    for tweet in public_tweets:
        print tweet.text
        raw_input("")
  
   def UserFollower(self):  # Get followers list, friend list
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
   def UserSelfTimeline(self):  #My tweets
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
   def SearchAPI(self):
      results = self.api.search(q="HarryPotter",count=100,lang="en",locale="en")
      '''
      tone_analyzer = ToneAnalyzer(username=TOKENS.ibm_username,
                             password=TOKENS.ibm_password,
                             version='2016-02-11')
      '''
      for i,each in enumerate(results):         
         self.session.execute(
            """
            INSERT INTO Tweepy (counter, tweet, lang, sourcee, retweet_count, created_at, analytics)
            VALUES (%s, %s, %s,%s, %s, %s, %s)
            """,
            (i, each.text, each.lang, each.source, each.retweet_count, str(each.created_at),str(self.tone_analyzer.tone(text=each.text)) )
            )
   


   def TestTimeOut(self):
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
   def TestTimeout2(self):
      
      try:
         for i,tweet in enumerate(tweepy.Cursor(self.api.search,q="Potter OR Khalifa OR Harry OR Dog OR Cat",lang="en",locale="en",count=100).items()):
            print "i= ",i," ", "Tweet= ",tweet.text
            self.tweetlist.append(tweet.text)
            if (i%10==0):
               print "TRY Length of tweets = ", len(self.tweetlist)
               print "TRY Length of unique tweets = ",len(set(self.tweetlist)),"\n\n\n"
               #raw_input("")
         self.numb+=i
         print "TRY (FOR) Numb = ",self.numb 
         print "TRY (FOR) Length of tweets = ", len(self.tweetlist)
         print "TRY (FOR) Length of unique tweets = ",len(set(self.tweetlist))

      except:
      '''        
         print "EXCEPT Sleeping ..."
         print "EXCEPT numb= ",self.numb
         print "EXCEPT Length of tweets = ", len(self.tweetlist)
         print "EXCEPT Length of unique tweets = ",len(set(self.tweetlist)),"\n\n\n"
      '''

         if(self.numb < 15000):
            self.TestTimeout2()
         #print "Unexpected error:", sys.exc_info()[0]
      
      finally:
         self.tweetlist=[]
         self.numb=0
         print "FINALLY len(self.tweetlist)= ",len(self.tweetlist)
         print "FINALLY numb = ", numb
         
         #self.TestTimeout2()


      



if __name__ == "__main__":
   tweets =  TweetAPI()
   tweets.Connect()
   '''
   tweets.SearchAPI()
   '''
   tweets.TestTimeout2()

else:
   print "Redo module load"
   exit(0)
