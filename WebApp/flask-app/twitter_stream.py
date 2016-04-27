import tweepy
import json
import TOKENS
from Analytics import IBMToneAnalyzer
from multiprocessing import Process

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
        #try:

        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        tweet=decoded['text'].encode('ascii', 'ignore')
        IBMToneJSON=None
        IBMToneJSON = self.tone_analyzer.tone(text=tweet)
        #need to give the full system path
        #need to give the full system path
        IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
        TwitterRealtimef=open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimetwitter.json","w")
        each1_list_names=[]
        each1_list_numbers=[]
        TwitterRealtimef.write(tweet.encode('utf-8'))
        for each in IBMToneJSON['document_tone']['tone_categories'][0]['tones']:
               each1_list_names.append(each['tone_name'])
               each1_list_numbers.append(each['score'])
        IBMToneJSON_1.write('['+'{"year":"Anger", "income": ' +str(each1_list_numbers[0])+ ' },'+ '{"year":"Disgust", "income": ' +str(each1_list_numbers[1])+ ' },'+'{"year":"Fear", "income": ' +str(each1_list_numbers[2])+ ' },'+ '{"year":"Joy", "income": ' +str(each1_list_numbers[3])+ ' },'+ '{"year":"Saddness", "income": ' +str(each1_list_numbers[4])+ ' }'+']' )            




        IBMToneJSON_1.close()
        TwitterRealtimef.close()

        return True


        #except:
        #    pass
    def on_error(self, status):
        print status



def loop_trump():
    print "Inside loop trump"

    #need to give the full system path
    IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['DonaldTrump','trump2016','trump'])

def loop_sanders():
    print "Inside loop sanders"
    #need to give the full system path
    IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['bernie','sanders','berniesanders','feelthebern','berniesander'])

def loop_clinton():
    print "Inside loop clinton"
    #need to give the full system path
    IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['clinton','hillary','hillaryclinton','hillary2016'])


def loop_kasich():
    print "Inside loop kasich"
    #need to give the full system path
    IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['kasich','johnkasich','johnkasich','kasich4us','kasich2016'])


def loop_cruz():
    print "Inside loop cruz"
    #need to give the full system path
    IBMToneJSON_1= open("/home/ubuntu/BigDataProject/Big-Neuron/WebApp/flask-app/static/realtimesentiment.json","w")
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['cruz','tedcruz','tedcruz2016'])

def loop_b(var2):
    if(var2=='trump'):
        Process(target=loop_trump).start()
    elif(var2=='clinton'):
        Process(target=loop_clinton).start()
    elif(var2=='sanders'):
        Process(target=loop_sanders).start()
    elif(var2=='cruz'):
        Process(target=loop_cruz).start()
    elif(var2=='kasich'):
        Process(target=loop_kasich).start()
    else:
        print "ERRRRROR"
        pass




'''
if __name__ == '__main__':
    pass
else:
    pass
    #Process(target=loop_a).start()
'''