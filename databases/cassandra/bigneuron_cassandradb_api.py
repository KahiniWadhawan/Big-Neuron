#-----------------------------------------------------------
#Author: Kahini Wadhawan
# This file provides Big Neuron cassandra db access functions
#-----------------------------------------------------------

import tweepy
import json
import time
import os
import sys

from cassandra.cluster import Cluster


#-----------------------------------------------------------
#Loading configs for Tweepy
#-----------------------------------------------------------
oauth = json.loads(open('../../config/oauth.json','r').read())

#------------------------------------------------------------
#Create a twitter API connection w/ OAuth
#------------------------------------------------------------
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#----------------------------------------------------------
#Connecting to Cassandra DB Keyspace
#----------------------------------------------------------
#revisit - add function to execute cassandra_setup.sh from here
def db_connect():
    cluster = Cluster()
    session = cluster.connect('twitterdataset')
    return session


#---------------------------------------------------
# Get the User object for Election Candidates
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

#---------------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in Cassandra
# Access table by Candidate's name
#---------------------------------------------------------------------------
def insert_tweets_to_db(username):
    #getting user tweets
    tweets = get_user_tweets(username,1)
    #setting up db
    session = db_connect()

    for tweet in tweets:
        print(tweet._json.keys())
        # session.execute("insert into " + username + " (tweet_sno, tweet_text," +
		# "tweet_created_at, tweet_favcount, tweet_lang, tweet_place)" +
		# "values(str(tweet._json.id), str(tweet._json.text), str(tweet.created_at),
        #int(tweet.favorite_count)," + "'test','testing')")

#insert_tweets_to_db('realDonaldTrump')




