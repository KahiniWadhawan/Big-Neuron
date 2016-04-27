# -*- coding: utf-8 -*-

#------------------------------------------------------------------
#Author: Kahini Wadhawan
#------------------------------------------------------------------
import tweepy, json, collections, functools, operator
import time

#  Set these global variables to customize your analysis.
#  Register and create tokens at http://dev.twitter.com

# def load_configs():
#     configs = json.loads(open('user_info.json','r').read())
#     oauth = json.loads(open('oauth.json','r').read())
#
#     # Create a twitter API connection w/ OAuth.
#     auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
#     auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
#     api = tweepy.API(auth)

#---------------------------------------------------------
# Loading configs here - revisit later make it a function
#---------------------------------------------------------
configs = json.loads(open('user_info.json','r').read())
oauth = json.loads(open('oauth.json','r').read())

# Create a twitter API connection w/ OAuth.
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['access_token'], oauth['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

first_friends_limit = 20
second_friends_limit = 20
node_id = str(configs['user_id'])

#--revisit - write centre and first friends connection to data.edgelist also
def get_first_friends():
    my_friends = []
    friend_cursors = tweepy.Cursor(api.friends, id = configs['screen_name'])
    for friend_cursor in friend_cursors.items():
        friend = {}
        friend['screen_name'] = friend_cursor.screen_name
        friend['friends_count'] = friend_cursor.friends_count
        friend['followers_count'] = friend_cursor.followers_count
        friend['name'] = friend_cursor.name
        friend['profile_image_url'] = friend_cursor.profile_image_url
        friend['id'] = friend_cursor.id
        friend['following'] = friend_cursor.following
        my_friends.append(friend)

    # #calling pull_tweets functions
    # my_friends = pull_tweets.get_first_friends(configs['screen_name'])

    f = open('temp/myfriends.json', 'w')
    f.seek(0)
    friends_json = json.dumps(my_friends, sort_keys=True, indent=4)
    f.write(friends_json)
    f.truncate()
    f.close()

    totals = functools.reduce(operator.add, map(collections.Counter, my_friends))
    print "%s is follwing: %s" % (configs['screen_name'], len(my_friends))
    print "They follow a total of: %s" % totals['friends_count']
    print "And have a following of: %s" % totals['followers_count']



# Weird that I wasn't getting rate limited on this...
def get_second_friends():
    f = open('temp/myfriends.json','r').read()
    #api rate exceeds, so limiting second friends
    friends = json.loads(f)[:first_friends_limit]
    friend_ids = [f['id'] for f in friends]
    print('first friends_ids :: ', friend_ids)
    processed = []
    count = 0
    while True:
        if len(processed) == first_friends_limit:
            break
        try:
             for friend_id in friend_ids:
                #writing node_id and first friends connections to data.edgelist
                write_edgelist(node_id, friend_id)
                if friend_id not in processed:
                    processed.append(friend_id)
                    print "Getting followers for %s" % friend_id
                    id_list = api.friends_ids(user_id=friend_id)[:second_friends_limit]
                    print('second friends for friend id:: ', friend_id, len(id_list))
                    #writing edgelist of second_friends
                    for second_id in id_list:
                        count += 1
                        print count
                        write_edgelist(friend_id, second_id)

        except tweepy.TweepError, error:
            print type(error)

            if str(error) == 'Not authorized.':
                print 'Can''t access user data - not authorized.'
                #return id_list
                break

            if str(error) == 'User has been suspended.':
                print 'User suspended.'
                #return id_list
                break

            errorObj = error[0][0]

            print errorObj

            if errorObj['message'] == 'Rate limit exceeded':
                print 'Rate limited. Sleeping for 15 minutes.'
                time.sleep(15 * 60 + 15)
                continue


def write_edgelist(follower, followed):
    f = open('temp/data.edgelist', 'a')
    f.write("%s %s\n" % (follower, followed))
    f.close()

def fill_out_graph():
    #load_configs()
    #mygraph = json.loads(open('temp/small_graph.json', 'r').read())
    #data adding to network json for showing more details
    mygraph = json.loads(open('temp/network.json', 'r').read())
    for node in mygraph['nodes']:
        full_user = api.get_user(id=node['id'])
        node['screen_name'] = full_user.screen_name
        node['friends_count'] = full_user.friends_count
        node['followers_count'] = full_user.followers_count
        node['name'] = full_user.name
        node['profile_image_url'] = full_user.profile_image_url
        node['following'] = full_user.following
        print "Saved data for: %s" % full_user.screen_name

    f = open('static/graph.json', 'w')
    f.seek(0)
    graph_json = json.dumps(mygraph, sort_keys=True, indent=4)
    f.write(graph_json)
    f.truncate()
    f.close()

def print_configs():
    for key in configs.keys():
        print "%s: %s" % (key, configs[key])

def get_edgelist():
    #load_configs()
    # Create edgelist
    get_first_friends()
    get_second_friends()

if __name__ == '__main__':
    print "Nothing to do night now. Use run.py"