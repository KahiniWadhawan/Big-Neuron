#--------------------------------------------------------------------
#Author: Kahini Wadhawan
#Edited: Michael Muehlbradt
#NOTE before this script can work we need a running Cassandra cluster as per
#http://wiki.apache.org/cassandra/GettingStarted
#-------------------------------------------------------------------
import tweepy
# not sure if we have to import cassandra driver
import time

#-------------------------------------------------------------------
# Appache Cassandra setup
#-------------------------------------------------------------------
from cassandra.cluster import Cluster

cluster = Cluster()

#setting default keyspace to RAwData
session = cluster.connect(RawData)

#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Setup Tweepy auth and API object with Twitter application credentials
#-------------------------------------------------------------------
# Twitter Application key and secret
consumer_key = "fill---in--your--consumer_key"
consumer_secret = "fill---in---your---consumer_key"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
#-------------------------------------------------------------------

#---------------------------------------------------
# Get the User object for Donald Trump
#---------------------------------------------------
user = api.get_user('realDonaldTrump')

#-------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in MongoDB tweets collection
# P.S. To access the json for a tweet object, just call ._json on the tweet object
#-------------------------------------------------------------------
# The method below fetches 3.2k tweets for realDonaldTrump, in comparison to 31k tweets posted by him
# TODO - Fix the code below to fetch and store all 31k tweets
tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump').items()
# tweets is an 'tweepy.cursor.ItemIterator' object
for tweet in tweets:
	session.execute(
	"""
	INSERT INTO feed (tweet)
	VALUES (%s)
	""",
	("tweet._json")
	)

# TODO - The code below needs to be updated for the changes required to automatically
# detect the last tweet saved and then call the Tweepy API for tweets with
# id's higher than the tweet already saved.
# #-------------------------------------------------------------------
# # First insert the items from the first request in MongoDB collection
# #-------------------------------------------------------------------
# #global tweets
# tweets = None
# if (collection.count() == 0 ):
#     print "collection count is 0"
#     tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump').items()
#     # tweets is an 'tweepy.cursor.ItemIterator' object
#     for tweet in tweets:
#         #print "inserting tweets in collection"
#         collection.insert_one(tweet._json)
#
# while tweets:
#     #print "reiterating tweets for looking recent tweets"
#     recent_tweet = collection.find().sort([("_id", pymongo.DESCENDING)]).limit(1)
#     # recent_tweet is an 'pymongo.cursor.Cursor' object.
#     # Use count() to check the cursor actually points to an object or not
#     if (recent_tweet.count() > 0 ):
#         #print "recent tweets count 0"
#         recent_tweet = recent_tweet.next()
#         recent_id = recent_tweet['id_str']
#     else:
#         recent_id = 0
#     #global tweets
#     tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump', since_id=recent_id).items()
#     # 'tweepy.cursor.ItemIterator' object has num_objects field which returns
#     # the number of tweets returned by calling the API above
#     if tweets.num_tweets == 0 :
#         print "Waiting for 15 mins. Will request Twitter again"
#         time.sleep(60*15) # Wait for 15 mins
#         pass
#     else:
#         # Got new data from Twitter
#         # Add the newly found tweets in MongoDB
#         for tweet in tweets:
#             collection.insert_one(tweet._json)
