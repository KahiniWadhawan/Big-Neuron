from flask import Flask, Response
import pika
import json
import pandas

 #setup queue
connection = pika.BlockingConnection()
channel = connection.channel()


#function to get data from queue
def get_tweets(size=10):
    tweets = []
    # Get ten messages and break out
    count = 0
    for method_frame, properties, body in channel.consume('twitter_topic_feed'):

        tweets.append(json.loads(body))

        count += 1

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)

        # Escape out of the loop after 10 messages
        if count == size:
            break

    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    print 'Requeued %i messages' % requeued_messages

    return tweets

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)


@app.route('/feed/raw_feed', methods=['GET'])
def get_raw_tweets():
    tweets = get_tweets(size=5)
    text = ""
    for tweet in tweets:
        tt = tweet.get('text', "")
        text = text + tt + "<br>"

    return text


@app.route('/feed/word_count', methods=['GET'])
def get_word_count():

    #get tweets from the queue
    tweets = get_tweets(size=30)

    #dont count these words
    ignore_words = [ "rt", "chelsea"]
    words = []
    for tweet in tweets:
        tt = tweet.get('text', "").lower()
        for word in tt.split():
            if "http" in word:
                continue
            if word not in ignore_words:
                words.append(word)

    p = pandas.Series(words)
    #get the counts per word
    freq = p.value_counts()
    #how many max words do we want to give back
    freq = freq.ix[0:300]

    response = Response(freq.to_json())

    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__ == "__main__":
    app.run()