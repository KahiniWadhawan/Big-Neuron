#---------------------------------------------------------------
#Author: Kahini Wadhawan
#---------------------------------------------------------------

#---------------------------------------------------------------
# This file controls Network analysis and pre-processing
# and visulization for networks
#---------------------------------------------------------------
from gen_graph import get_edgelist, fill_out_graph
#from analysis_functions import run_analysis
import tweepy
import json

import sys
# sys.path.insert(0, '../../preprocessing/')
# import pull_tweets
import os

#-----------------------------------------------------------------------
# Loading twitter credentials - revisit remove and call from pull_tweets
#----------------------------------------------------------------------
config_DIR = "../../config/"
#Loading oauth credentials
oauth = json.loads(open(os.path.join(config_DIR,'oauth.json'),'r').read())
# Create a twitter API connection w/ OAuth.
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = tweepy.API(auth)

