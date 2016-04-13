import tweepy
import time
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('twitterdataset')

consumer_key = "XaDHyTvQz4S4AZtYZ8ZRyTURJ"
consumer_secret = "ytjcGMfAZ6AebykaN6ngHMxHoYHN45ZnCP7QHhzKq4SrDt7lFn"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
#user = api.get_user('realDonaldTrump')
tweets = tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump').items()

for i,tweet in enumerate(tweets):
	#session.execute("""insert into tweet_users (tweet_sno,tweet_text,tweet_created_at,tweet_favcount,tweet_lang,tweet_place) values('testing','testing','testing',1000,'testing','testing')""")
	



	session.execute("""
		insert into tweet_users (tweet_sno,tweet_text,tweet_created_at,tweet_favcount,tweet_lang,tweet_place) values(str(i),str(tweet.text),str(tweet.created_at),int(tweet.favorite_count),'test','testing')
		""")

	#print type(tweet),"\n\n" ,dir(tweet),"\n\n----->",tweet.text
	#print "tweet.text: ",tweet.text,type(tweet.text)
	#print "tweet.author ",tweet.author
	#print "tweet.coordinates ",tweet.coordinates
	#print "tweet.created_at ",str(tweet.created_at),type(tweet.created_at)
	#print "tweet.favorite ",tweet.favorite
	#print "tweet.favorite_count ",tweet.favorite_count,type(tweet.favorite_count)
	#print "tweet.favorited ",tweet.favorited
	#print "tweet.geo ",tweet.geo,type(tweet.geo)
	#print "tweet.id ",tweet.id,type(tweet.id)
	#print "tweet.id_str ",tweet.id_str
	#print "tweet.is_quote_status ",tweet.is_quote_status,type(tweet.created_at)
	#print "tweet.lang ",tweet.lang,type(tweet.lang)
	#print "tweet.parse ",tweet.parse
	#print "tweet.parse_list ",tweet.parse_list
	#print "tweet.place ",tweet.place,type(tweet.place)
	#print "tweet.retweet ",tweet.retweet
	#print "tweet.retweet_count ",tweet.retweet_count,type(tweet.retweet_count)
	#print "tweet.retweeted ",tweet.retweeted
	#print "tweet.retweets ",tweet.retweets
	#print "tweet.source ",str(tweet.source),type(tweet.source)
	#print "tweet.source_url ",tweet.source_url
	#print "tweet.truncated ",tweet.truncated
	#print "tweet.user ",tweet.user
	#raw_input()

	for i,tweet in enumerate(tweets):
		print type(tweet.text)
		print type(tweet.lang)
		print type(tweet.source)
		print type(tweet.retweet_count)
		print type(tweet.created_at)