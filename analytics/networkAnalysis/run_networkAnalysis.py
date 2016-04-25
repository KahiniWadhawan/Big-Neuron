#---------------------------------------------------------------
#Author: Kahini Wadhawan
#---------------------------------------------------------------

#---------------------------------------------------------------
# This file controls Network analysis and pre-processing
# and visulization for networks
#---------------------------------------------------------------
from gen_graph import get_edgelist, fill_out_graph
from analysis import run_analysis
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

def main():
    get_edgelist()
    run_analysis()
    fill_out_graph()

def get_info():
    settings = {}
    settings['screen_name'] = raw_input('Who do you want to run this for?: ')
    settings['size'] = int(raw_input('How many nodes?: '))

    #api = pull_tweets.connect_twitter() -revisit
    user_info = api.get_user(screen_name=settings['screen_name'])
    settings['user_id'] = int(user_info.id)

    f = open('user_info.json', 'wb')
    f.seek(0)
    settings_json = json.dumps(settings, sort_keys=True, indent=4)
    f.write(settings_json)
    f.truncate()
    f.close()

    main()

if __name__ == '__main__':
    get_info()
