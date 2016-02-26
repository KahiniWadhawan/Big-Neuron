import tweepy

# Twitter Application key and secret
consumer_key = "BgJU5GvnsjFlachp6BTPbUvpU"
consumer_secret = "5f3AS7hiyv82AuWgxqDfM7bGMTnaaK2t2oLx7vyYl6HFLUD1Hs"
# Twitter Access token & secret, to enable access to your own profile
# access_token = ""
# access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Only use this, if you want to get your own information from Twitter
# auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Method to access my own timeline
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

#---------------------------------------------------
# Get all tweets by Donald Trump
#---------------------------------------------------

# Get the User object for Donald Trump
user = api.get_user('realDonaldTrump')
print user.screen_name
print user.followers_count
# # Not relevant
# friends = user.friends()
# for friend in friends:
#    print friend.screen_name

# P.S. API only allows to retrieve 200 tweets in one request
tweets = api.user_timeline(screen_name='realDonaldTrump',count=200)
print tweets.__class__
for tweet in tweets:
   print vars(tweet)
   print tweet.text
   # The id /id_str is the unique identifier for a tweet. We'll use id_str as it's unicode
   print tweet.id_str
   print "------------------"