import tweepy
import pymongo

#-------------------------------------------------------------------
# MongoDB setup
#-------------------------------------------------------------------
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# This creates a MongoDB database with the name tweets_database
db = client.tweets_database
# This creates a collection named tweets inside the database 'tweets_database'
collection = db.tweets
collection.create_index("id_str", unique=True)
#-------------------------------------------------------------------

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
# print user.screen_name
# print user.followers_count

# # P.S. API only allows to retrieve 200 tweets in one request
# tweets = api.user_timeline(screen_name='realDonaldTrump',count=200)
# print tweets.__class__
# for tweet in tweets:
#    print vars(tweet)
#    print tweet.text
#    # The id /id_str is the unique identifier for a tweet. We'll use id_str as it's unicode
#    print tweet.id_str
#    print "------------------"

#print len(tweets)
#-------------------------------------------------------------------
# Insert all tweets returned by the Cursor API and store them in MongoDB tweets collection
# P.S. To access the json for a tweet object, just call ._json on the tweet object
#-------------------------------------------------------------------

#recent_tweet = collection.find().sort([("_id", pymongo.DESCENDING)]).limit(1)
#print recent_tweet.__class__
#print recent_tweet
#j = recent_tweet.next()
#print j['id_str']
#
#exit()


#-------------------------------------------------------------------
# First insert the items from the first request in MongoDB collection
#-------------------------------------------------------------------
#global tweets
tweets = None
if (collection.count() == 0 ):
    print "collection count is 0"
    tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump').items()
    # tweets is an 'tweepy.cursor.ItemIterator' object
    for tweet in tweets:
        #print "inserting tweets in collection"
        collection.insert_one(tweet._json)

while tweets:
    #print "reiterating tweets for looking recent tweets"
    recent_tweet = collection.find().sort([("_id", pymongo.DESCENDING)]).limit(1)
    # recent_tweet is an 'pymongo.cursor.Cursor' object.
    # Use count() to check the cursor actually points to an object or not
    if (recent_tweet.count() > 0 ):
        #print "recent tweets count 0"
        recent_tweet = recent_tweet.next()
        recent_id = recent_tweet['id_str']
    else:
        recent_id = 0
    #global tweets
    tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump', since_id=recent_id).items()
    # 'tweepy.cursor.ItemIterator' object has num_objects field which returns
    # the number of tweets returned by calling the API above
    if tweets.num_tweets == 0 :
        print "Waiting for 15 mins. Will request Twitter again"
        time.sleep(60*15) # Wait for 15 mins
        pass
    else:
        # Got new data from Twitter
        # Add the newly found tweets in MongoDB
        for tweet in tweets:
            collection.insert_one(tweet._json)

