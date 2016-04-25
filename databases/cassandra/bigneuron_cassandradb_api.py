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


#---------------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in Cassandra
# Access table by Candidate's name
#---------------------------------------------------------------------------
def insert_data_to_table(candname):
    #getting user tweets
    tweets = get_user_tweets(candname,4)
    #setting up db
    session = db_connect()

    for tweet in tweets:
        #inserting to tweets table
        # try:
        tweets_query = prepare_tweets_query(candname,tweet)
        session.execute(tweets_query)
        # except
        #inserting data to Sentencelevel table
        sentencelevel_query = prepare_sentencelevel_query(candname,tweet)
        session.execute(sentencelevel_query)


def prepare_tweets_query(candname, tweet):
    #creating table name
    table_name = candname + '_tweets'

    datetime_lst = str(tweet.created_at).encode('utf-8').split()
    date = datetime_lst[0]
    time = datetime_lst[1]

    print 'tweet :: ',tweet.text

    tweets_query = "insert into " + table_name + "(" + \
                "tweet_id, " \
                "tweet_text, " \
                "lang, " \
                "retweet_count, " \
                "created_at, " \
                "date, " \
                "time) " + "values('" + \
                str(tweet.id_str.encode('utf-8')) + "','" + \
                str(tweet.text.encode('utf-8')) + "', '" + \
                str(tweet.lang) + "', " + \
                str(tweet.retweet_count) + ", '" + \
                str(tweet.created_at) + "', '" + \
                str(date) + "', '" + \
                str(time) + "'" \
                ");"

    print('tweets_query', tweets_query)
    return tweets_query


def prepare_sentencelevel_query(candname,tweet):
    #creating table name
    table_name = candname + '_sentencelevel'

    #processing date and time
    datetime_lst = str(tweet.created_at).encode('utf-8').split()
    date = datetime_lst[0]
    time = datetime_lst[1]


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
                "disgust_score) " + "values('" + \
                str(tweet.id_str.encode('utf-8')) + "', '" + \
                str(tweet.created_at) + "', '"  + \
                str(date) + "', '"  + \
                str(time) + "', '"  + \
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


    #print('sentencelevel_query :: ', sentencelevel_query)
    return sentencelevel_query


#def prepare_topics_query():
#def prepare_graph_query():



#--------------------------------------------------------------------------------
# Data fetch from db functions to be called by WebApp
#--------------------------------------------------------------------------------

#this function creates per week collective tweets json for doclevel visualization
#It aggregates all 5 emotion scores for a collection of tweets to return average score
#select c_group_and_total(created_at, anger_score) from realDonaldTrump_sentencelevel
#Revisit - do we need to store doc_json in db???
def gen_doclevel_json(candname, file_path):
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

    print 'select_query ::',select_query
    resultSet  = session.execute(select_query)
    #print ('resultSet:: ',resultSet)

    #processing resultset for date:scores
    anger_score_dict = {}
    joy_score_dict = {}
    sadness_score_dict = {}
    disgust_score_dict = {}
    fear_score_dict = {}

    for row in resultSet:
        #print row
        # print row.twitterdataset_cus_group_and_total_date__anger_score.keys(),\
        #     row.twitterdataset_cus_group_and_total_date__anger_score.values()

        # anger_score_dict[row.twitterdataset_cus_group_and_total_date__anger_score.keys()[0]] = \
        #     row.twitterdataset_cus_group_and_total_date__anger_score.values()[0]
        # joy_score_dict[row.twitterdataset_cus_group_and_total_date__joy_score.keys()[0]] = \
        #     row.twitterdataset_cus_group_and_total_date__joy_score.values()[0]
        # sadness_score_dict[row.twitterdataset_cus_group_and_total_date__sadness_score.keys()[0]] = \
        #     row.twitterdataset_cus_group_and_total_date__sadness_score.values()[0]
        # fear_score_dict[row.twitterdataset_cus_group_and_total_date__fear_score.keys()[0]] = \
        #     row.twitterdataset_cus_group_and_total_date__fear_score.values()[0]
        # disgust_score_dict[row.twitterdataset_cus_group_and_total_date__disgust_score.keys()[0]] = \
        #     row.twitterdataset_cus_group_and_total_date__disgust_score.values()[0]

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



    print 'anger_score_dict', anger_score_dict
    print 'anger_score_dict', joy_score_dict
    print 'anger_score_dict', sadness_score_dict
    print 'anger_score_dict', fear_score_dict
    print 'disgust_score_dict', disgust_score_dict


    #Now we have got all emotion score dicts with day-wise data
    #generating doc level json format required by visualization
    #revisit - normalize sum/no.of days, put day number - 1,2,3 ...
    doc_json = []
    date_list = [i for i in anger_score_dict.keys()]
    print 'date_list', date_list

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

        print 'num of tweets per day query:: ', select_query
        resultSet  = session.execute(select_query)
        for row in resultSet:
            #print row
            num_tweets_date_dict[date] = row.system_count_tweet_id

        print 'num_tweets_date_dict',num_tweets_date_dict


    for date_key,anger_s in anger_score_dict.iteritems():
        temp = {}
        anger_score = anger_s/float(num_tweets_date_dict[date])
        joy_score = joy_score_dict[date_key]/float(num_tweets_date_dict[date])
        sadness_score = sadness_score_dict[date_key]/float(num_tweets_date_dict[date])
        fear_score = fear_score_dict[date_key]/float(num_tweets_date_dict[date])
        disgust_score = disgust_score_dict[date_key]/float(num_tweets_date_dict[date])

        #converting scores to %ges for pie-chart viz
        total_score = anger_score + joy_score + sadness_score + fear_score + disgust_score
        anger_score_norm = (anger_score/float(total_score)) * 100
        joy_score_norm = (joy_score/float(total_score)) * 100
        sadness_score_norm = (sadness_score/float(total_score)) * 100
        fear_score_norm = (fear_score/float(total_score)) * 100
        disgust_score_norm = (disgust_score/float(total_score)) * 100

        temp["anger"] = anger_score_norm
        temp["joy"] = joy_score_norm
        temp["sadness"] = sadness_score_norm
        temp["fear"] = fear_score_norm
        temp["disgust"] =disgust_score_norm
        #inserting date index in sorted date_list instead of its value
        #temp["day"] = date_key
        temp["day"] = date_list.index(date_key) + 1

        doc_json.append(temp)

    print doc_json

    #writing doc_json to provided file_path - revisit not writing
    with open(os.path.join(file_path,'doc.json'), 'wb') as outfile:
            json.dump(doc_json, outfile)


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

    print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    temp = {}
    tweets_count = 0
    for row in resultSet:
        tweets_count +=1
        temp[row.tweet_id] = row.retweet_count

    #sorting dict to get top tweets with retweet_count
    sorted_temp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
    print 'sorted_temp', sorted_temp
    if num < tweets_count:
        top_tweets = sorted_temp[:num]

    print 'top_tweets',top_tweets

    #making top tweet_id's list to pass on to select query
    top_tweets_id_str = ""
    count = 0
    for tup in top_tweets:
        count +=1
        print 'tup', tup
        if count == 1:
            top_tweets_id_str =  "'" + tup[0]
        else:
            top_tweets_id_str += "','" + tup[0]

    top_tweets_id_str += "'"
    print 'top_tweets_id_str :: ',top_tweets_id_str

    #fetching text for top tweets
    select_query = "select " + \
                "tweet_id, " \
                "tweet_text " \
                " from " + table_name + \
                " where tweet_id in (" + top_tweets_id_str + ")" + \
                ";"

    print 'select_query ::',select_query
    resultSet  = session.execute(select_query)

    #preparing tweets_dict containing tweet_id and text to be used by WebApp
    for row in resultSet:
        tweets_dict[row.tweet_id] = row.tweet_text

    print tweets_dict
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

        emotion_json = json.loads(row.emotion_json)
        with open(os.path.join(file_path,'emotion.json'), 'wb') as outfile:
            json.dump(emotion_json, outfile)

        social_json = json.loads(row.social_json)
        with open(os.path.join(file_path,'social.json'), 'wb') as outfile:
            json.dump(social_json, outfile)


    #print 'result_jsons', result_jsons

    #return result_jsons


#testing all functions here in a sequence
#insert_data_to_table('realDonaldTrump')
#insert_data_to_table('HillaryClinton')
# insert_data_to_table('BernieSanders')
# insert_data_to_table('tedcruz')
# insert_data_to_table('JohnKasich')

#gen_doclevel_json('realDonaldTrump','/data')
#gen_doclevel_json('HillaryClinton','data/')
#get_tweet_list('realDonaldTrump',2)
#get_tweet_tones('realDonaldTrump','724237889886904320')


#--------------------------------
#testing
#---------------------------------

# def test(candname):
#     #getting user tweets
#     tweets = get_user_tweets(candname,6)
#     #setting up db
#     session = db_connect()
#
#     for i,tweet in enumerate(tweets):
#         print ('processing tweet :: ',i)
#         session.execute("""
#             insert into tweet_users (tweet_id,tweet_text,lang,
#             retweet_count,created_at) values(str(tweet.id_str),
#             str(tweet.text),str(tweet.lang),tweet.retweet_count,
#             str(tweet.created_at))
#             """)
#         for i,tweet in enumerate(tweets):
#             print type(tweet.text)
#             print type(tweet.lang)
#             print type(tweet.source)
#             print type(tweet.retweet_count)
#             print type(tweet.created_at)


#test('HillaryClinton')