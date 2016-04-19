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
#import db_api
'''
Assumption: Each list of top 20 tweets will be pre-run for each candidate.  Each tweet list per candidate will be saved
in a separate file.  These files will be read into this module to generate the json files.
'''
import sys
sys.path.append("<path to tone analyzer module>")  #append path to db api module that has the method to get list of top tweets
import tone_analyzer as tone #Do we have a tone analyzer module -or- are we inserting tweets by hand into IBM tone analyzer to get the json output?


def build_data_files( cand ):
    tweetlist = open("static/tweetlist/" + cand + ".txt") #TO DO: This file doesn't exist yet since list of top tweets not yet generated!!
    for tweet in tweetlist:
        rawJSON = tone.analyze_tweet(tweet) #TO DO: this might not yet be implemented - if it is, get correct module and method name!!
        dump_json_data(cand, rawJSON)            
    

def build_data_folders( cand ):
    dir = "static/data/" + cand
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


if __name__ == "__main__":
    candidates = ["clinton", "cruz", "kasich", "sanders", "trump"]
    
    for i in candidates:
        build_data_folders( candidates[i] )
        build_data_files( candidate[i] )
            
    