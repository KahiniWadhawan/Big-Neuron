# -*- coding: utf-8 -*-
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
import operator
import re
from analyze_tone import IBMToneAnalyzer

from cassandra.cluster import Cluster


#-----------------------------------------------------------
#Loading configs for Tweepy
#-----------------------------------------------------------
#print ('current path :', sys.path[0])
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

    a= json.loads(tone_json)

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
         emotion_scores_dict[elem['tone_name']] = elem['score']

    #print ('emotion_scores_dict :: ',emotion_scores_dict)
    return emotion_scores_dict


def get_writing_scores(writing_json):
    #emotion score dict  - key = emotion name, val = score
    writing_scores_dict = {}
    for elem in writing_json:
         writing_scores_dict[elem['tone_name']] = elem['score']

    #print ('emotion_scores_dict :: ',emotion_scores_dict)
    return writing_scores_dict


def get_social_scores(social_json):
    #emotion score dict  - key = emotion name, val = score
    social_scores_dict = {}
    for elem in social_json:
         social_scores_dict[elem['tone_name']] = elem['score']

    #print ('emotion_scores_dict :: ',emotion_scores_dict)
    return social_scores_dict


#---------------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in Cassandra
# Access table by Candidate's name
#---------------------------------------------------------------------------
def insert_data_table_tweets(candname):
    #getting user tweets
    tweets = get_user_tweets(candname)
    #setting up db
    session = db_connect()
    count = 0
    for tweet in tweets:
        count += 1
        print count
        #inserting to tweets table
        # try:
        tweets_bound = prepare_tweets_query(candname,tweet,session)
        session.execute(tweets_bound)
        # except
        # #inserting data to Sentencelevel table
        # sentencelevel_bound = prepare_sentencelevel_query(candname,tweet,session)
        # session.execute(sentencelevel_bound)


def prepare_tweets_query(candname, tweet,session):
    #creating table name
    table_name = candname + '_tweets'

    datetime_lst = str(tweet.created_at).encode('utf-8').split()
    date = datetime_lst[0]
    time = datetime_lst[1]

    #print 'tweet :: ',tweet.text

    tweets_query = "insert into " + table_name + "(" + \
                "tweet_id, " \
                "tweet_text, " \
                "lang, " \
                "retweet_count, " \
                "created_at, " \
                "date, " \
                "time) " + " VALUES " \
                 "(?, ?, ?, ?, ?, ?, ?)"

    prepared = session.prepare(tweets_query)

    bound = prepared.bind((str(tweet.id_str.encode('utf-8')),
                           str(tweet.text.encode('utf-8')),
                           str(tweet.lang),
                           tweet.retweet_count,
                           str(tweet.created_at),
                           str(date),
                           str(time) ))


    #print('tweets_query', bound)

    return bound




#revisit - session close() on function closing
def insert_data_table_sentencelevel(candname):
    table_tweets = candname + '_tweets'
    table_sentencelevel = candname + '_sentencelevel'
    #setting up db
    session = db_connect()

    #getting tweets from tweets table to send to toneAnalyzer
    select_query = "select " + \
                "tweet_id, " \
                "tweet_text, " \
                "created_at " \
                " from " + table_tweets + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    result_jsons = {}
    count = 0
    for row in resultSet:
        count += 1
        print('inside sentencelevel gen processing record :: ',count)
        #if count > 679:

        tweet_id = row.tweet_id
        tweet_text = row.tweet_text
        print 'before regex :: ', tweet_text
        tweet_text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+'
                        r'[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
                        r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                        '', tweet_text)
        print tweet_text
        if tweet_text in ('',' '):
            tweet_text = "no text"

        tweet_created_at = row.created_at

        #calling prepare_sentencelevel_query for every tweet
        sentencelevel_bound = prepare_sentencelevel_query(candname,tweet_id,tweet_text
                                                              ,tweet_created_at,session)
        session.execute(sentencelevel_bound)



def prepare_sentencelevel_query(candname,tweet_id,tweet_text,tweet_created_at,session):
    #creating table name
    table_name = candname + '_sentencelevel'

    #processing date and time
    datetime_lst = str(tweet_created_at).encode('utf-8').split()
    date = datetime_lst[0]
    time = datetime_lst[1]


    #processing and getting jsons - test
    tone_json = call_ibmToneAnalyzer(tweet_text.encode('utf-8'))
    emotion_json,writing_json,social_json = gen_EWS_json(tone_json)

    #converting json to string in order to store in db table text field
    emotion_json_str = str(json.dumps(emotion_json)).encode('utf-8')
    writing_json_str = str(json.dumps(writing_json)).encode('utf-8')
    social_json_str = str(json.dumps(social_json)).encode('utf-8')

    tone_json_str = str(json.dumps(tone_json)).encode('utf-8')

    #processing and getting emotion scores
    emotion_scores_dict = get_emotion_scores(emotion_json)

    #processing and getting emotion scores
    writing_scores_dict = get_writing_scores(writing_json)

    #processing and getting emotion scores
    social_scores_dict = get_social_scores(social_json)

    sentencelevel_query = "insert into " + table_name + "(" + \
                "tweet_id," \
                "created_at, " \
                "date, " \
                "time, " \
                "tone_json, " \
                "emotion_json, " \
                "writing_json, " \
                "social_json," \
                "anger_score," \
                "joy_score," \
                "fear_score," \
                "sadness_score," \
                "disgust_score, " + \
                "analytical_score," \
                "confident_score," \
                "tentative_score," \
                "openness_score," \
                "conscientiousness_score," \
                "extraversion_score," \
                "agreeableness_score," \
                "emotionalrange_score) " + \
                " VALUES " + \
                 "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    #print sentencelevel_query
    prepared = session.prepare(sentencelevel_query)

    bound = prepared.bind((str(tweet_id.encode('utf-8')),
                           str(tweet_created_at),
                           str(date),
                           str(time),
                           str(tone_json_str.encode('utf-8')),
                           str(emotion_json_str.encode('utf-8')),
                           str(writing_json_str.encode('utf-8')),
                           str(social_json_str.encode('utf-8')),
                           emotion_scores_dict['Anger'],
                           emotion_scores_dict['Joy'],
                           emotion_scores_dict['Fear'],
                           emotion_scores_dict['Sadness'],
                           emotion_scores_dict['Disgust'],
                           writing_scores_dict['Analytical'],
                           writing_scores_dict['Confident'],
                           writing_scores_dict['Tentative'],
                           social_scores_dict['Openness'],
                           social_scores_dict['Conscientiousness'],
                           social_scores_dict['Extraversion'],
                           social_scores_dict['Agreeableness'],
                           social_scores_dict['Emotional Range']
                           ))


    #print('sentencelevel_query :: ', bound)
    return bound
#def prepare_topics_query():
#def prepare_graph_query():



#--------------------------------------------------------------------------------
# Data fetch from db functions to be called by WebApp
#--------------------------------------------------------------------------------

#this function creates per week collective tweets json for doclevel visualization
#It aggregates all 5 emotion scores for a collection of tweets to return average score
#select c_group_and_total(created_at, anger_score) from realDonaldTrump_sentencelevel
#Revisit - do we need to store doc_json in db???
#revisit - get tweets between - current(time) - 5 weeks prior

def gen_doclevel_emotion_json(candname, file_path):
    table_name = candname + '_sentencelevel'
    #setting up db
    session = db_connect()

    select_query = "select " + \
                "cus_group_and_total(date, anger_score)," \
                "cus_group_and_total(date, joy_score)," \
                "cus_group_and_total(date, fear_score)," \
                "cus_group_and_total(date, sadness_score)," \
                "cus_group_and_total(date, disgust_score) " \
                " from " + table_name + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)
    #print ('resultSet:: ',resultSet)

    #processing resultset for date:scores
    anger_score_dict = {}
    joy_score_dict = {}
    sadness_score_dict = {}
    disgust_score_dict = {}
    fear_score_dict = {}

    for row in resultSet:
        for key,val in row.twitterdataset_cus_group_and_total_date__anger_score.iteritems():
            anger_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__joy_score.iteritems():
            joy_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__sadness_score.iteritems():
            sadness_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__fear_score.iteritems():
            fear_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__disgust_score.iteritems():
            disgust_score_dict[key] = val



    # print 'anger_score_dict', anger_score_dict
    # print 'anger_score_dict', joy_score_dict
    # print 'anger_score_dict', sadness_score_dict
    # print 'anger_score_dict', fear_score_dict
    # print 'disgust_score_dict', disgust_score_dict


    #Now we have got all emotion score dicts with day-wise data
    #generating doc level json format required by visualization
    #revisit - normalize sum/no.of days, put day number - 1,2,3 ...
    doc_json = []
    date_list = [i for i in anger_score_dict.keys()]
    #print 'date_list', date_list

    #sort date_list - increasing order
    date_list.sort()

    #number of days
    num_tweets_date_dict = {}
    #select count (tweet_id) from
    # realDonaldTrump_sentencelevel where date = '2016-04-24' ALLOW FILTERING;
    for date in date_list:
        select_query = "select " + \
                "count(tweet_id)" \
                 " from " + table_name + \
                " where date = '" + date + "'" + \
                " ALLOW FILTERING " + \
                ";"

        #print 'num of tweets per day query:: ', select_query
        resultSet  = session.execute(select_query)
        for row in resultSet:
            #print row
            num_tweets_date_dict[date] = row.system_count_tweet_id

        #print 'num_tweets_date_dict',num_tweets_date_dict


    for date_key,anger_s in anger_score_dict.iteritems():
        temp = {}
        anger_score = anger_s/float(num_tweets_date_dict[date])
        joy_score = joy_score_dict[date_key]/float(num_tweets_date_dict[date])
        sadness_score = sadness_score_dict[date_key]/float(num_tweets_date_dict[date])
        fear_score = fear_score_dict[date_key]/float(num_tweets_date_dict[date])
        disgust_score = disgust_score_dict[date_key]/float(num_tweets_date_dict[date])

        #converting scores to %ges for pie-chart viz
        total_score = anger_score + joy_score + sadness_score + fear_score + disgust_score
        if total_score == 0:
            total_score = 1
        anger_score_norm = (anger_score/float(total_score)) * 100
        joy_score_norm = (joy_score/float(total_score)) * 100
        sadness_score_norm = (sadness_score/float(total_score)) * 100
        fear_score_norm = (fear_score/float(total_score)) * 100
        disgust_score_norm = (disgust_score/float(total_score)) * 100

        temp["anger"] = round(anger_score_norm,2)
        temp["joy"] = round(joy_score_norm,2)
        temp["sadness"] = round(sadness_score_norm,2)
        temp["fear"] = round(fear_score_norm,2)
        temp["disgust"] = round(disgust_score_norm,2)
        #inserting date index in sorted date_list instead of its value
        temp["day"] = date_key
        #temp["day"] = date_list.index(date_key) + 1

        doc_json.append(temp)

    #print doc_json

    #sorting doc_json - ordering it on day value
    doc_json.sort(key=operator.itemgetter('day'))

    #print 'doc_json sorted :: ', doc_json

    #writing doc_json to provided file_path - revisit not writing
    #revisit - permission denied to write file
    with open(os.path.join(file_path,'doc_emotion.json'), 'wb') as outfile:
            json.dump(doc_json, outfile)
    outfile.close()

    #return doc_json


#Writing json -format
#[{"tone_name": "Analytical", "score": 0.0, "tone_id": "analytical"},
# {"tone_name": "Confident", "score": 0.0, "tone_id": "confident"},
# {"tone_name": "Tentative", "score": 0.0, "tone_id": "tentative"}]

def gen_doclevel_writing_json(candname, file_path):
    table_name = candname + '_sentencelevel'
    #setting up db
    session = db_connect()

    select_query = "select " + \
                "cus_group_and_total(date, analytical_score)," \
                "cus_group_and_total(date, confident_score)," \
                "cus_group_and_total(date, tentative_score)" \
                " from " + table_name + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)
    #print ('resultSet:: ',resultSet)

    #processing resultset for date:scores
    analytical_score_dict = {}
    confident_score_dict = {}
    tentative_score_dict = {}

    for row in resultSet:

        for key,val in row.twitterdataset_cus_group_and_total_date__analytical_score.iteritems():
            analytical_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__confident_score.iteritems():
            confident_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__tentative_score.iteritems():
            tentative_score_dict[key] = val


    # print 'analytical_score_dict', analytical_score_dict
    # print 'confident_score_dict', confident_score_dict
    # print 'tentative_score_dict', tentative_score_dict


    #Now we have got all emotion score dicts with day-wise data
    #generating doc level json format required by visualization
    #revisit - normalize sum/no.of days, put day number - 1,2,3 ...
    doc_json = []
    date_list = [i for i in analytical_score_dict.keys()]
    #print 'date_list', date_list

    #sort date_list - increasing order
    date_list.sort()

    #number of days
    num_tweets_date_dict = {}
    #select count (tweet_id) from
    # realDonaldTrump_sentencelevel where date = '2016-04-24' ALLOW FILTERING;
    for date in date_list:
        select_query = "select " + \
                "count(tweet_id)" \
                 " from " + table_name + \
                " where date = '" + date + "'" + \
                " ALLOW FILTERING " + \
                ";"

        #print 'num of tweets per day query:: ', select_query
        resultSet  = session.execute(select_query)
        for row in resultSet:
            #print row
            num_tweets_date_dict[date] = row.system_count_tweet_id

        #print 'num_tweets_date_dict',num_tweets_date_dict


    for date_key,analytical_s in analytical_score_dict.iteritems():
        temp = {}
        analytical_score = analytical_s/float(num_tweets_date_dict[date])
        confident_score = confident_score_dict[date_key]/float(num_tweets_date_dict[date])
        tentative_score = tentative_score_dict[date_key]/float(num_tweets_date_dict[date])

        #converting scores to %ges for pie-chart viz
        total_score = analytical_score + confident_score + tentative_score
        if total_score == 0:
            total_score = 1
        analytical_score_norm = (analytical_score/float(total_score)) * 100
        confident_score_norm = (confident_score/float(total_score)) * 100
        tentative_score_norm = (tentative_score/float(total_score)) * 100

        temp["analytical"] = round(analytical_score_norm,2)
        temp["confident"] = round(confident_score_norm,2)
        temp["tentative"] = round(tentative_score_norm,2)
        #inserting date index in sorted date_list instead of its value
        #temp["day"] = date_key
        temp["day"] = date_list.index(date_key) + 1

        doc_json.append(temp)

    #print doc_json

    #sorting doc_json - ordering it on day value
    #revisit here to limit no. of records in doc_json
    doc_json.sort(key=operator.itemgetter('day'))

    #print 'doc_json sorted :: ', doc_json

    #writing doc_json to provided file_path - revisit not writing
    #revisit - permission denied to write file
    with open(os.path.join(file_path,'doc_writing.json'), 'wb') as outfile:
            json.dump(doc_json, outfile)
    outfile.close()

    #return doc_json


#Social json - format
#[{"tone_name": "Openness", "score": 0.829, "tone_id": "openness_big5"},
# {"tone_name": "Conscientiousness", "score": 0.976, "tone_id": "conscientiousness_big5"},
# {"tone_name": "Extraversion", "score": 0.933, "tone_id": "extraversion_big5"},
# {"tone_name": "Agreeableness", "score": 0.916, "tone_id": "agreeableness_big5"},
# {"tone_name": "Emotional Range", "score": 0.019, "tone_id": "neuroticism_big5"}]

# openness_score double,
# conscientiousness_score double,
# extraversion_score double,
# agreeableness_score double,
# emotionalrange_score double

def gen_doclevel_social_json(candname, file_path):
    table_name = candname + '_sentencelevel'
    #setting up db
    session = db_connect()

    select_query = "select " + \
                "cus_group_and_total(date, openness_score)," \
                "cus_group_and_total(date, conscientiousness_score)," \
                "cus_group_and_total(date, extraversion_score)," \
                "cus_group_and_total(date, agreeableness_score)," \
                "cus_group_and_total(date, emotionalrange_score) " \
                " from " + table_name + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)
    #print ('resultSet:: ',resultSet)

    #processing resultset for date:scores
    openness_score_dict = {}
    conscientiousness_score_dict = {}
    extraversion_score_dict = {}
    agreeableness_score_dict = {}
    emotionalrange_score_dict = {}

    for row in resultSet:
        for key,val in row.twitterdataset_cus_group_and_total_date__openness_score.iteritems():
            openness_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__conscientiousness_score.iteritems():
            conscientiousness_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__extraversion_score.iteritems():
            extraversion_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__agreeableness_score.iteritems():
            agreeableness_score_dict[key] = val

        for key,val in row.twitterdataset_cus_group_and_total_date__emotionalrange_score.iteritems():
            emotionalrange_score_dict[key] = val



    # print 'openness_score_dict', openness_score_dict
    # print 'conscientiousness_score_dict', conscientiousness_score_dict
    # print 'extraversion_score_dict', extraversion_score_dict
    # print 'agreeableness_score_dict', agreeableness_score_dict
    # print 'emotionalrange_score_dict', emotionalrange_score_dict


    #Now we have got all emotion score dicts with day-wise data
    #generating doc level json format required by visualization
    #revisit - normalize sum/no.of days, put day number - 1,2,3 ...
    doc_json = []
    date_list = [i for i in openness_score_dict.keys()]
    #print 'date_list', date_list

    #sort date_list - increasing order
    date_list.sort()

    #number of days
    num_tweets_date_dict = {}
    #select count (tweet_id) from
    # realDonaldTrump_sentencelevel where date = '2016-04-24' ALLOW FILTERING;
    for date in date_list:
        select_query = "select " + \
                "count(tweet_id)" \
                 " from " + table_name + \
                " where date = '" + date + "'" + \
                " ALLOW FILTERING " + \
                ";"

        #print 'num of tweets per day query:: ', select_query
        resultSet  = session.execute(select_query)
        for row in resultSet:
            #print row
            num_tweets_date_dict[date] = row.system_count_tweet_id

        #print 'num_tweets_date_dict',num_tweets_date_dict


    for date_key,openness_s in openness_score_dict.iteritems():
        temp = {}
        openness_score = openness_s/float(num_tweets_date_dict[date])
        conscientiousness_score = conscientiousness_score_dict[date_key]/float(num_tweets_date_dict[date])
        extraversion_score = extraversion_score_dict[date_key]/float(num_tweets_date_dict[date])
        agreeableness_score = agreeableness_score_dict[date_key]/float(num_tweets_date_dict[date])
        emotionalrange_score = emotionalrange_score_dict[date_key]/float(num_tweets_date_dict[date])

        #converting scores to %ges for pie-chart viz
        total_score = openness_score + conscientiousness_score + extraversion_score \
                      + agreeableness_score + emotionalrange_score

        if total_score == 0:
            total_score = 1
        openness_score_norm = (openness_score/float(total_score)) * 100
        conscientiousness_score_norm = (conscientiousness_score/float(total_score)) * 100
        extraversion_score_norm = (extraversion_score/float(total_score)) * 100
        agreeableness_score_norm = (agreeableness_score/float(total_score)) * 100
        emotionalrange_score_norm = (emotionalrange_score/float(total_score)) * 100

        temp["openness_score"] = round(openness_score_norm,2)
        temp["conscientiousness_score"] = round(conscientiousness_score_norm,2)
        temp["extraversion_score"] = round(extraversion_score_norm,2)
        temp["agreeableness_score"] = round(agreeableness_score_norm,2)
        temp["emotionalrange_score"] = round(emotionalrange_score_norm,2)
        #inserting date index in sorted date_list instead of its value
        #temp["day"] = date_key
        temp["day"] = date_list.index(date_key) + 1

        doc_json.append(temp)

    #print doc_json

    #sorting doc_json - ordering it on day value
    doc_json.sort(key=operator.itemgetter('day'))

    #print 'doc_json sorted :: ', doc_json

    #writing doc_json to provided file_path - revisit not writing
    #revisit - permission denied to write file
    with open(os.path.join(file_path,'doc_social.json'), 'wb') as outfile:
            json.dump(doc_json, outfile)
    outfile.close()

    #return doc_json

#getting top tweets based on retweet_count
def get_tweet_list(candname,num=20):
    tweets_dict = {}
    #revisit - "ORDER BY is only supported when the partition key is
    # restricted by an EQ or an IN."

    table_name = candname + '_tweets'
    #setting up db
    session = db_connect()

    select_query = "select " + \
                "tweet_id, " \
                "retweet_count " \
                " from " + table_name + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    temp = {}
    tweets_count = 0
    for row in resultSet:
        tweets_count +=1
        temp[row.tweet_id] = row.retweet_count

    #sorting dict to get top tweets with retweet_count
    sorted_temp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
    #print 'sorted_temp', sorted_temp
    if num < tweets_count:
        top_tweets = sorted_temp[:num]

    #print 'top_tweets',top_tweets

    #making top tweet_id's list to pass on to select query
    top_tweets_id_str = ""
    count = 0
    for tup in top_tweets:
        count +=1
        #print 'tup', tup
        if count == 1:
            top_tweets_id_str =  "'" + tup[0]
        else:
            top_tweets_id_str += "','" + tup[0]

    top_tweets_id_str += "'"
    #print 'top_tweets_id_str :: ',top_tweets_id_str

    #fetching text for top tweets
    select_query = "select " + \
                "tweet_id, " \
                "tweet_text " \
                " from " + table_name + \
                " where tweet_id in (" + top_tweets_id_str + ")" + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    #preparing tweets_dict containing tweet_id and text to be used by WebApp
    for row in resultSet:
        tweet_text = row.tweet_text
        tweet_text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+'
                    r'[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
                    r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                    '', tweet_text)
        tweets_dict[row.tweet_id] = tweet_text

    #print tweets_dict
    return tweets_dict


#this function returns a dictionary of tone_json, writing_json, emotion_json and social_json
#revisit - ask Jessica - write to path or return json dict
def get_tweet_tones(candname,tweet_id,file_path):
    table_name = candname + '_sentencelevel'
    #setting up db
    session = db_connect()

    select_query = "select " + \
                "tone_json, " \
                "writing_json, " \
                "emotion_json, " \
                "social_json" \
                " from " + table_name + \
                " where tweet_id = '" + tweet_id + "'" + \
                ";"

    #print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    result_jsons = {}
    for row in resultSet:
        # tone_json = json.loads(row.tone_json)
        # with open(os.path.join(file_path,'tone.json'), 'wb') as outfile:
        #     json.dump(tone_json, outfile)

        writing_json = json.loads(row.writing_json)
        with open(os.path.join(file_path,'writing.json'), 'wb') as outfile:
            json.dump(writing_json, outfile)
        outfile.close()

        emotion_json = json.loads(row.emotion_json)
        with open(os.path.join(file_path,'emotion.json'), 'wb') as outfile:
            json.dump(emotion_json, outfile)
        outfile.close()

        social_json = json.loads(row.social_json)
        with open(os.path.join(file_path,'social.json'), 'wb') as outfile:
            json.dump(social_json, outfile)
        outfile.close()


    #print 'result_jsons', result_jsons

    #return result_jsons


#testing all functions here in a sequence

#populating tweets tables
#insert_data_table_tweets('realDonaldTrump')
#insert_data_table_tweets('HillaryClinton')
#insert_data_table_tweets('BernieSanders')
#insert_data_table_tweets('tedcruz')
#insert_data_table_tweets('JohnKasich')

#populating sentencelevel tables
#insert_data_table_sentencelevel('realDonaldTrump')
#insert_data_table_sentencelevel('HillaryClinton')
#insert_data_table_sentencelevel('BernieSanders')
#insert_data_table_sentencelevel('tedcruz')
#insert_data_table_sentencelevel('JohnKasich')

#generating doc level jsons
#gen_doclevel_emotion_json('realDonaldTrump','data/')
#gen_doclevel_writing_json('realDonaldTrump','data/')
#gen_doclevel_social_json('realDonaldTrump','data/')
#gen_doclevel_json('HillaryClinton','data/')
#get_tweet_list('realDonaldTrump',2)
#get_tweet_tones('realDonaldTrump','722967660833722369','data/')


#--------------------------------
#testing
#---------------------------------

def test(candname):
    table_name = candname + '_tweets'
    #getting user tweets
    tweets = get_user_tweets(candname,20)
    #setting up db
    session = db_connect()

#     prepare(statement)[source]
# Prepares a query string, returning a PreparedStatement instance which can be used as follows:
#
# >>> session = cluster.connect("mykeyspace")
# >>> query = "INSERT INTO users (id, name, age) VALUES (?, ?, ?)"
# >>> prepared = session.prepare(query)
# >>> session.execute(prepared, (user.id, user.name, user.age))
# Or you may bind values to the prepared statement ahead of time:
#
# >>> prepared = session.prepare(query)
# >>> bound_stmt = prepared.bind((user.id, user.name, user.age))
# >>> session.execute(bound_stmt)
# Of course, prepared statements may (and should) be reused:
#
# >>> prepared = session.prepare(query)
# >>> for user in users:
# ...     bound = prepared.bind((user.id, user.name, user.age))
# ...     session.execute(bound)


    query = "INSERT INTO " + table_name + \
            "(tweet_id, " \
            "tweet_text, " \
            "lang, " \
            "retweet_count, " \
            "created_at," \
            "date," \
            "time" \
            ") VALUES " \
            "(?, ?, ?, ?, ?, ?, ?)"

    prepared = session.prepare(query)

    for i,tweet in enumerate(tweets):
        #print ('processing tweet :: ',i)

        datetime_lst = str(tweet.created_at).encode('utf-8').split()
        date = datetime_lst[0]
        time = datetime_lst[1]

        bound = prepared.bind((str(tweet.id_str.encode('utf-8')), str(tweet.text.encode('utf-8')),
                               str(tweet.lang),tweet.retweet_count,
                               str(tweet.created_at),date,time))
        #print 'bound :: ',bound
        session.execute(bound)



#test('HillaryClinton')