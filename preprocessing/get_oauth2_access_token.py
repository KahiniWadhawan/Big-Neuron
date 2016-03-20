#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
__date__ = "$Feb 11, 2016 11:57:06 PM$"

from twython import Twython

'''
TO DO: Get each team members' key and secret.
       Store in dictionary or array of tuples.
       Implement twitter factory or flyweight pattern.
'''

def get_access_token(key, secret):
    twitter = Twython(key, secret, oauth_version=2)
    return twitter.obtain_access_token()
    
def get_twitter_instance(key, token):
    return Twython(key, token)
    
def main():
    APP_KEY = 'my_app_key'
    APP_SECRET = 'YOUR_APP_SECRET'
    ACCESS_TOKEN = get_access_token(APP_KEY, APP_SECRET)
    TWITTER = get_twitter_instance(APP_KEY, ACCESS_TOKEN)
        
   
if __name__ == "__main__":
    main()
