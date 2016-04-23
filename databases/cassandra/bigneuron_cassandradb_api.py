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


#---------------------------------------------------------------------
#This below function is contributed by: Tanvi Parikh, Piyush Patel
#----------------------------------------------------------------------
def gen_EWS_json(tone_json):
    #tone_json is json structure
    #f = open("../data/tone.json", "r")
    #a = f.read()
    a= tone_json
    l1,l2,l3 =  a['document_tone']['tone_categories'][0]['tones'],\
                a['document_tone']['tone_categories'][1]['tones'],\
                a['document_tone']['tone_categories'][2]['tones']

    emotion_json = l1
    writing_json = l2
    social_json = l3

    return (emotion_json,writing_json,social_json)

    # with open('../data/emotion.json', 'w') as outfile:
    #     json.dump(l1, outfile)
    # with open('../data/writing.json', 'w') as outfile:
    #     json.dump(l2, outfile)
    # with open('../data/social.json', 'w') as outfile:
    #     json.dump(l3, outfile)

#----------------------------------------------------------------------------

#Function to process emotion scores
'''[{
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
	}]'''

def get_emotion_scores(emotion_json):
    #emotion score dict  - key = emotion name, val = score
    emotion_scores_dict = {}
    for elem in emotion_json:
         print elem
         emotion_scores_dict[elem['tone_name']] = elem['score']

    print ('emotion_scores_dict :: ',emotion_scores_dict)
    return emotion_scores_dict


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
        #date_time = str(tweet.created_at).split()
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
        tweets_query = prepare_tweets_query(candname,tweet)
        session.execute(tweets_query)

        #inserting data to Sentencelevel table
        sentencelevel_query = prepare_sentencelevel_query(candname,tweet)
        session.execute(sentencelevel_query)


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

# tweet_id varchar primary key,
# created_at varchar,
# tone_json text,
# emotion_json text,
# writing_json text,
# social_json text,
# anger_score double,
# joy_score double,
# fear_score double,
# sadness_score double,
# disgust_score double

def prepare_sentencelevel_query(candname,tweet):
    #creating table name
    table_name = candname + '_sentencelevel'

    #processing and getting jsons - test
    tone_json = call_ibmToneAnalyzer(tweet.text.encode('utf-8'))
    emotion_json,writing_json,social_json = gen_EWS_json(tone_json)

    #converting json to string in order to store in db table text field
    emotion_json_str = str(json.dumps(emotion_json)).encode('utf-8')
    writing_json_str = str(json.dumps(writing_json)).encode('utf-8')
    social_json_str = str(json.dumps(social_json)).encode('utf-8')

    tone_json_str = str(json.dumps(tone_json)).encode('utf-8')

    #processing and getting emotion scores
    emotion_scores_dict = get_emotion_scores(emotion_json)
    
    sentencelevel_query = "insert into " + table_name + "(" + \
                "tweet_id," \
                "created_at, " \
                "tone_json, " \
                "emotion_json, " \
                "writing_json, " \
                "social_json," \
                "anger_score," \
                "joy_score," \
                "fear_score," \
                "sadness_score," \
                "disgust_score) " + "values('" + \
                str(tweet.id_str.encode('utf-8')) + "', '" + \
                str(tweet.created_at) + "', '"  + \
                str(tone_json_str.encode('utf-8')) + "', '" + \
                str(emotion_json_str.encode('utf-8')) + "', '" + \
                str(writing_json_str.encode('utf-8')) + "', '" + \
                str(social_json_str.encode('utf-8')) + "', " + \
                str(emotion_scores_dict['Anger']) + ", " + \
                str(emotion_scores_dict['Joy']) + ", " + \
                str(emotion_scores_dict['Fear']) + "," + \
                str(emotion_scores_dict['Sadness']) + "," + \
                str(emotion_scores_dict['Disgust']) + "" + \
                ");"


    print(sentencelevel_query)
    return sentencelevel_query


#def prepare_topics_query():
#def prepare_graph_query():



insert_data_table_tweets('realDonaldTrump')





