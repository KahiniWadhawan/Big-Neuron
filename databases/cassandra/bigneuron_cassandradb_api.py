#--------------------------------------------------------------------
#Author: Kahini Wadhawan
# This file provides Big Neuron cassandra db access functions
#revisit : put try - except blocks for exception - refer gen_graph.py
#----------------------------------------------------------------------

import tweepy
import json
import time
import os
import sys
from analyze_tone import IBMToneAnalyzer

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


# this function processes tone of tweet by calling IBM Tone Analyzer
def call_ibmToneAnalyzer(tweet_text):
    toneAnalyzer = IBMToneAnalyzer()
    tone_json = toneAnalyzer.get_sentiment(tweet_text)
    return tone_json


#---------------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in Cassandra
# Access table by Candidate's name
#---------------------------------------------------------------------------
def insert_data_table_tweets(candname):
    #getting user tweets
    tweets = get_user_tweets(candname,10)
    #setting up db
    session = db_connect()

    for tweet in tweets:
        print('in for::',tweet.text)
        #print(tweet._json.keys())
        # session.execute("insert into " + username + " (tweet_sno, tweet_text," +
		# "tweet_created_at, tweet_favcount, tweet_lang, tweet_place)" +
		# "values(str(tweet._json.id), str(tweet._json.text), str(tweet.created_at),
        #int(tweet.favorite_count)," + "'test','testing')")
        #below method returns date format - 2016-04-22 23:33:20
        date_time = str(tweet.created_at).split()
        #the below method returns date format -  u'Fri Apr 22 23:33:20 +0000 2016'
        # print('tweet timestamp :: ', tweet._json['created_at'])
        # print(date_time)
        #storing - date and timestamps as string
        #string comparison's can compare time and date easily
        # day = date_time[2]
        # month = date_time[1]
        # year = date_time[5]
        # time = date_time[3]
        #inserting to tweets table

        session.execute(tweets_query)

        #inserting data to Sentencelevel table



def prepare_tweets_query(candname, tweet):
    #creating table name
    table_name = candname + '_tweets'
    tweets_query = "insert into " + table_name + "(" + \
                "tweet_id, " \
                "tweet_text, " \
                "lang, " \
                "retweet_count, " \
                "created_at) " + "values('" + \
                str(tweet.id_str.encode('utf-8')) + "', '" + \
                str(tweet.text.encode('utf-8')) + "', '" + \
                str(tweet.lang) + "', " + \
                str(tweet.retweet_count) + ", '" + \
                str(tweet.created_at) + "'" \
                ");"
                # str(day) + "', '" + \
                # str(month) + "', '" + \
                # str(year) + "', '" + \
                # str(time) + "', '" + \
                #");"

    print(tweets_query)
    return tweets_query

def prepare_sentencelevel_query(candname,tweet):
    #creating table name
    table_name = candname + '_sentencelevel'
    
    sentencelevel_query = "insert into " + table_name + "(" + \
                "tweet_id, " \
                "tweet_text, " \
                "lang, " \
                "retweet_count, " \
                "created_at) " + "values('" + \
                str(tweet.id_str.encode('utf-8')) + "', '" + \
                str(tweet.text.encode('utf-8')) + "', '" + \
                str(tweet.lang) + "', " + \
                str(tweet.retweet_count) + ", '" + \
                str(tweet.created_at) + "'" \
                ");"
                # str(day) + "', '" + \
                # str(month) + "', '" + \
                # str(year) + "', '" + \
                # str(time) + "', '" + \
                #");"

    print(sentencelevel_query)
    return sentencelevel_query


#def prepare_topics_query():
#def prepare_graph_query():



insert_data_table_tweets('realDonaldTrump')





