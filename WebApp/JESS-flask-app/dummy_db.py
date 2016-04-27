#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from amcharts_JSON import dump_json_data

__author__ = "Jessica"
__date__ = "$Apr 21, 2016 9:18:10 PM$"


def get_tweet_list( candidate, tweet_num):
    if (candidate != "" and tweet_num > 0):
        return {"0": "tweet tweet tweet tweet tweet tweet tweet tweet tweet tweet tweet tweet tweet tweet tweettweet tweet tweet tweet tweet tweettweet tweet tweettweet tweet tweettweet tweet tweet", "1": "tweet tweet tweet tweet tweet tweettweet tweet tweettweet tweet tweettweet tweet tweettweet tweet tweet" , "2": "tweet tweet tweet"}


def get_tweet_tones( candidate, tweet_id, fpath):
    print "entering get_jsons()"
    print "tweetID is: %s" % tweet_id
    fo = open(fpath + "tone.json", "r")
    data = fo.read()
    
    if (candidate != "" and tweet_id != ""):
        print "generate json files"
        dump_json_data(fpath, data)
    print "leaving get_jsons()"
    
    
