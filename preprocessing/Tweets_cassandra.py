import tweepy
import TOKENS	#Import secret phrase module
#Rerference API
# http://tweepy.readthedocs.org/en/v3.5.0/api.html
class Tweet:
	def Connect(self):
		self.consumer_key = TOKENS.consumer_key
		self.consumer_secret = TOKENS.consumer_secret
		self.access_token=TOKENS.access_token
		self.access_token_secret=TOKENS.access_token_secret
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)

	def TimelineTweet(self):	# View timeline tweets
		public_tweets = self.api.home_timeline()
		for tweet in public_tweets:
		    print tweet.text
		    raw_input("")
	
	def UserFollower(self):	# Get followers list, friend list
		#user = self.api.get_user('sivapalakurthi')
		user = self.api.get_user('sivapalakurthi')
		print user.screen_name
		print user.followers_count
		for friend in user.friends():
   			print friend.screen_name

   	def Pagination(self):
   		for friend in tweepy.Cursor(self.api.friends).items():
   			# Process the friend here
   			print friend.screen_name

   	def FriendTimeline(self):
   		for status in tweepy.Cursor(self.api.friends_timeline).items(200):
   			print status

   	#This function follows every followers in your list.
   	def FollowEveryFollower(self):
   		for follower in tweepy.Cursor(self.api.followers).items():
   			follower.follow()   			
   			#raw_input("")
   	def UserSelfTimeline(self):	#My tweets
   		for status in tweepy.Cursor(self.api.user_timeline).items():
   			print status.text
   			raw_input("")

   	'''
   	So far we have just demonstrated pagination iterating per an item. 
   	What if instead you want to process per a page of results? 
   	'''
   	def UserSelfTimeline_page(self):
   		for page in tweepy.Cursor(self.api.user_timeline).pages():
   			print page[0].text
   			raw_input("")



   	def UsersTimeline(self):
   		for status in tweepy.Cursor(self.api.user_timeline, id="realDonaldTrump").items():
   			print status.text
   			raw_input("")


   	def UsersLimits(self):
   		for status in tweepy.Cursor(self.api.user_timeline).items(2):
   			print status.text

   	def UserLimits_pages(self):
   		for page in tweepy.Cursor(self.api.user_timeline).pages(3):
   			print page

   	def SearchAPI(self):
   		results = self.api.search(q="HarryPotter",lang="en",locale="en")
   		for i in results:   			
				print i.text
				#print i.lang
				raw_input("")






   	#Running this snippet will print all users you follow that themselves follow 
   	#less than 300 people total - to exclude obvious spambots, 
   	#for example - and will wait for 15 minutes each time it hits the rate limit.
'''
	def limit_handled(cursor):
	    while True:
	        try:
	            yield cursor.next()
	        except tweepy.RateLimitError:
	            time.sleep(15 * 60)


for follower in limit_handled(tweepy.Cursor(api.followers).items()):
    if follower.friends_count < 300:
        print follower.screen_name

'''
if __name__=="__main__":
	tweets =  Tweet()
	tweets.Connect()
	tweets.SearchAPI()
else:
	print "Redo module load"
	exit(0)
