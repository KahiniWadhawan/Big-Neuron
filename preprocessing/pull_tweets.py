#--------------------------------------------------------------------
#Author: Kahini Wadhawan
#-------------------------------------------------------------------
import tweepy
import pymongo
import time
import json
import os
import sys
#sys.path.insert(0, '../analytics/sentimentAnalysis/')
#import analyze_tone

#-------------------------------------------------------------------
# Setting up paths
#-------------------------------------------------------------------
config_DIR = "../config/"
#-------------------------------------------------------------------
# MongoDB setup
#-------------------------------------------------------------------
from pymongo import MongoClient

def db_connect():
    client = MongoClient('localhost', 27017)
    # This creates a MongoDB database with the name tweets_database
    db = client.Big_Neuron
    # This creates a collection named tweets inside the database 'tweets_database'
    t_collection = db.tweets
    ts_collection = db.tweets_sentiments
    # Create a unique index on the field 'id_str' so that the tweets fetched from Twitter
    # are not duplicated in the MongoDB collection
    t_collection.create_index("id_str", unique=True)
    ts_collection.create_index("id_str", unique=True)
    return t_collection,ts_collection


#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Setup Tweepy auth and API object with Twitter application credentials
#-------------------------------------------------------------------
# Twitter Application key and secret
#consumer_key = "fill--your---consumer--key"
#consumer_secret = "fill--your--consumer--secret"
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(auth)

#Loading oauth credentials
oauth = json.loads(open(os.path.join(config_DIR,'oauth.json'),'r').read())
# Create a twitter API connection w/ OAuth.
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = tweepy.API(auth)

#making above as a function - for other files to use
def connect_twitter():
    # #Loading oauth credentials
    # oauth = json.loads(open('oauth.json','r').read())
    #
    # # Create a twitter API connection w/ OAuth.
    # auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
    # auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
    # api = tweepy.API(auth)
    return api



#---------------------------------------------------
# Get the User object for Donald Trump
#---------------------------------------------------
def get_user(username):
    #username = 'realDonaldTrump'
    user = api.get_user(username)
    return user

def get_user_tweets(username,num=None):
    #username = 'realDonaldTrump'
    tweets = None
    if not num:
        tweets = tweepy.Cursor(api.user_timeline, screen_name=username).items()
    else:
        tweets = tweepy.Cursor(api.user_timeline, screen_name=username).items(num)

    return tweets

#-------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in MongoDB tweets collection
# P.S. To access the json for a tweet object, just call ._json on the tweet object
#-------------------------------------------------------------------
# The method below fetches 3.2k tweets for realDonaldTrump, in comparison to 31k tweets posted by him
# TODO - Fix the code below to fetch and store all 31k tweets
#tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump').items()
# tweets is an 'tweepy.cursor.ItemIterator' object

def insert_tweets_data_db(username):
    #getting user tweets
    tweets = get_user_tweets(username)
    #setting up db
    t_collection,ts_collection = db_connect()

    for tweet in tweets:
        t_collection.insert_one(tweet._json)
        t_id_str = tweet._json['id_str']
        t_text = tweet._json['text']
        #----------------------------------------------------------
        # Calling IBM tone analyzer to get sentiment of the tweet
        #----------------------------------------------------------
        sentiment_str = analyze_tone.get_sentiment(t_text)
        #adding tweets id_str to sentiment json
        sentiment_json = json.loads(sentiment_str)
        #inserting id_str
        sentiment_json['id_str'.encode('utf-8')] = t_id_str.encode('utf-8')
        #print("sentiment json keys:: ", sentiment_json.keys())
        ts_collection.insert_one(sentiment_json)

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


#--------------------------------------------------------------
# More functions for deep analytics
#--------------------------------------------------------------
def get_first_friends(username):
    my_friends = []
    #friend_cursors = tweepy.Cursor(api.friends, id = configs['screen_name'])
    friend_cursors = tweepy.Cursor(api.friends, id = username)
    for friend_cursor in friend_cursors.items():
        friend = {}
        friend['screen_name'] = friend_cursor.screen_name
        friend['friends_count'] = friend_cursor.friends_count
        friend['followers_count'] = friend_cursor.followers_count
        friend['name'] = friend_cursor.name
        friend['profile_image_url'] = friend_cursor.profile_image_url
        friend['id'] = friend_cursor.id
        friend['following'] = friend_cursor.following
        my_friends.append(friend)

    return my_friends

def get_second_friends():
    f = open('temp/myfriends.json','r').read()
    friends = json.loads(f)
    friend_ids = [f['id'] for f in friends]
    for friend_id in friend_ids:
        print "Getting followers for %s" % friend_id
        id_list = api.friends_ids(user_id=friend_id)
        for second_id in id_list:
            write_edgelist(friend_id, second_id)