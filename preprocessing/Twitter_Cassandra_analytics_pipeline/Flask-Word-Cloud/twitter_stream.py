import tweepy
import json
import TOKENS
from Analytics import IBMToneAnalyzer
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = TOKENS.consumer_key
consumer_secret = TOKENS.consumer_secret
access_token = TOKENS.access_token
access_token_secret = TOKENS.access_token_secret

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener,IBMToneAnalyzer):
    def __init__(self):
        IBMToneAnalyzer.__init__(self)


    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        tweet=decoded['text'].encode('ascii', 'ignore')

        
        #print(self.tone_analyzer.tone(text=tweet))

        f=open("/home/piyush/Big-neuron/Big-Neuron/preprocessing/Twitter_Cassandra_analytics_pipeline/Flask-Word-Cloud/static/realtimetwitter.json","w")
        f.write(tweet.encode('utf-8'))

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['election','trump2016','trump'])
    #stream.filter(track=['snarfblob'])