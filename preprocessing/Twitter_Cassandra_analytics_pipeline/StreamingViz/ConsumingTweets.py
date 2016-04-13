import pika

 #setup queue
connection = pika.BlockingConnection()
channel = connection.channel()

#function to get X messages from the queue
def get_tweets(size=10):
    tweets = []
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