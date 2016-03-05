#---------------------------------------------------------------------------
#Author: Kahini Wadhawan
#--------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# File to pull data from Twitter for a given query and dump it to filesystem.
# It uses Twitter Search and Tweepy python library.
#----------------------------------------------------------------------------

import tweepy
import os
import pickle

#---------------------------------------------------------------------
# Paths for texts dir, models_dir
#---------------------------------------------------------------------
twitter_texts_DIR = "../data/twitter_texts"

#-------------------------------------------------------------------
# Twitter data fetch code
# It is overwriting the existing text file.
# Setup Tweepy auth and API object with Twitter application credentials
#-------------------------------------------------------------------
consumer_key = "--fill--your--consumer-key"
consumer_secret = "--fill--your--consumer--secret"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


def search_twitter(query, num_results=None):
    if num_results == None:
        num_results = 200   #- can be set to 1000 or 1500 - it allows upto 2000

    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query,lang="en").items(num_results)]
    text_file_path = os.path.join(twitter_texts_DIR,'tweets.txt')
    if os.path.isfile(text_file_path):
        os.remove(text_file_path)
    fp = open(text_file_path,'wb')

    #create a list of dicts - each dict has keys - 'text', 'created_at'
    tweets_lst_dump = []

    for t in searched_tweets:
        tweet_json_dump = { "created_at" : t._json['created_at'], "text" : t._json['text'] }
        tweets_lst_dump.append(tweet_json_dump)
        if not t._json['retweeted']:   #excluded retweets - revisit
            fp.write(t._json['text'].encode('utf-8'))
            fp.write("\n")
            fp.write("----------------------\n")

    fp.close()

    dump_file_path = os.path.join(twitter_texts_DIR,'tweets_json_dump.p')
    if os.path.isfile(dump_file_path):
        os.remove(dump_file_path)
    pickle.dump(tweets_lst_dump, open(dump_file_path,'wb'))

#revisit to dump it to mongodb











