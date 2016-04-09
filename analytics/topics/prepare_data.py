#-------------------------------------------------------------
# Author: Kahini Wadhawan
#-------------------------------------------------------------

#-------------------------------------------------------------
# This File is to call Functions from tweepy tweets
# pulling class and write tweets to file. - Replace
# this reading from db
# Creates text files - One text file contains each
# line for a tweet & other is all tweets in a single line
#--------------------------------------------------------------

import os
import pickle

import sys
sys.path.insert(0, '../../preprocessing/')
import pull_tweets

#---------------------------------------------------------------------
# Paths for texts dir, models_dir
#---------------------------------------------------------------------
twitter_texts_DIR = "data/twitter_texts"

#--------------------------------------------------------------------
# Getting User tweets - revisit improve to get all users or take input
# from outside wrapper
#---------------------------------------------------------------------
def prepare_tweets_docs(username,num_results):
    if num_results == None:
        num_results = 200   #- can be set to 1000 or 1500 - it allows upto 2000

    # text file containing one tweet per line
    text1_file_path = os.path.join(twitter_texts_DIR,'tweets.txt')
    # if os.path.isfile(text1_file_path):
    #     os.remove(text1_file_path)
    fp1 = open(text1_file_path,'wb')

    # text file containing all tweets in a single line
    text2_file_path = os.path.join(twitter_texts_DIR,'tweets_single.txt')
    # if os.path.isfile(text2_file_path):
    #     os.remove(text2_file_path)
    fp2 = open(text2_file_path,'wb')

    print('text files path :: ',text1_file_path, text2_file_path)

    tweets = pull_tweets.get_user_tweets(username,num_results)

    #Preparing text 1
    for tweet in tweets:
        t_text = tweet._json['text']
        fp1.write(t_text.encode('utf-8'))
        fp1.write("\n")
        fp1.write("----------------------\n")
        fp2.write(t_text.encode('utf-8'))

    fp1.close()
    fp2.close()

prepare_tweets_docs('realDonaldTrump',10)


