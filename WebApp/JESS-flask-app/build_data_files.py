#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
__date__ = "$Apr 18, 2016 9:51:53 PM$"

import os
import shutil
from amcharts_JSON import dump_json_data
#import sys
#sys.path.append("<path to db api module>")  #append path to db api module that has the method to get list of top tweets
#from db_api import get_tweetlist
'''
Assumption: Each list of top 20 tweets will be pre-run for each candidate.  Each tweet list per candidate will be saved
in a separate file.  These files will be read into this module to generate the json files.
'''
import sys
sys.path.append("<path to tone analyzer module>")  #append path to db api module that has the method to get list of top tweets
from tone_analyzer import analyze_tweet  #Do we have a tone analyzer module -or- are we inserting tweets by hand into IBM tone analyzer to get the json output?

'''
    Create data files: writing.json, emotion.json, social.json) for each candidate
'''
def build_data_files( cand ):
    # Get tweet list from db which is a list of tuples -- [(tweet_id, tweet_text), ...]
    tweetlist = get_tweetlist(cand)
    # Iterate through tweetlist to perform (1) tone analysis and (2) clean the raw JSON data (tone.json) on each tweet
    for tweet in tweetlist:
        fpath = build_data_dir( cand, tweet[0] )
        rawJSON = analyze_tweet(tweet[0])
        dump_json_data(fpath, rawJSON)           
    

def build_data_dir( cand, tweetID ):
    dir = "static/data/" + cand + "/" + tweetID
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    return dir


if __name__ == "__main__":
    candidates = ["clinton", "cruz", "kasich", "sanders", "trump"]
    
    for i in candidates:
        build_data_files( candidate[i] )
            
    