import tweepy

#-------------------------------------------------------------------
# Setup Tweepy auth and API object with Twitter application credentials
#-------------------------------------------------------------------
# Twitter Application key and secret
consumer_key = "BgJU5GvnsjFlachp6BTPbUvpU"
consumer_secret = "5f3AS7hiyv82AuWgxqDfM7bGMTnaaK2t2oLx7vyYl6HFLUD1Hs"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
#-------------------------------------------------------------------

#---------------------------------------------------
# Get all tweets by Donald Trump
#---------------------------------------------------
# Get the User object for Donald Trump
user = api.get_user('realDonaldTrump')
print user.screen_name
print user.followers_count

# P.S. API only allows to retrieve 200 tweets in one request
tweets = api.user_timeline(screen_name='realDonaldTrump',count=200)
print tweets.__class__
for tweet in tweets:
   print vars(tweet)
   print tweet.text
   # The id /id_str is the unique identifier for a tweet. We'll use id_str as it's unicode
   print tweet.id_str
   print "------------------"