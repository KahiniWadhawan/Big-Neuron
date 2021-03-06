''' Authors - 
        Jessica Lynch
        Tanvi Parikh
    Purpose - 
        Integration of Flask with Webapp
    Date - 
        16th April, 2016
'''

__author__ = "Jessica, Tanvi"
__date__ = "$Apr 14, 2016 11:39:45 PM$"

from flask import Flask, render_template, request, session

app = Flask(__name__)
# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a secret key (random text) and keep it secret
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

#sys.path.append(os.path.dirname(__file__) + r"/static/data/dummy_db.py")  #append path to db api module that has the method to get list of top tweets
from dummy_db import get_tweet_list, get_tweet_tones  #Do we have a tone analyzer module -or- are we inserting tweets by hand into IBM tone analyzer to get the json output?
#import sys
#sys.path.insert(0, '../../databases/cassandra/')
#from bigneuron_cassandradb_api import get_tweet_list, get_tweet_tones

'''
    Renders the dashboard.
'''
@app.route('/')
def home():
    print "REQUEST from index---", request
    return render_template("index.html")

'''
    Renders the landing dashboard for each candidate
'''
@app.route("/{{ request.form['candidate'] }}", methods = ["GET", "POST"])
def select_candidate():
    retVal = None
    if request.method == "POST":
        radio = request.form['candidate'] #this retrieves which radio button was pressed
        session['candidate'] = radio
        if radio in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
            fpath = "pages/%s/%s.html" % (radio, radio)
            retVal = render_template(fpath, cand=radio)
        else:
            retVal = "Error in select_candidate(). Need to make an error page"
    return retVal

'''
    Load visualizations from their respective candidate pages
'''
@app.route("/wordcloud", methods = ["GET", "POST"])
def wordcloud():
    print "Inside wordcloud()"
    retVal = None
    cand   = session['candidate']
    print "In wordcloud, session['candidate'] is - ", cand
    if cand in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
        fpath = "pages/%s/%s_wordcloud.html" % (cand, cand)
        retVal = render_template(fpath)
    else:
        retVal = "Error in topic(). Need to make an error page"
    return retVal

    
'''
    Renders the realtime dashboard for any candidate
'''
@app.route('/realtime')
def realtime():
    print "REQUEST from realtime---", request
    return render_template("realtime.html")

'''
    Renders the Follower's Network visualization for any candidate
'''
@app.route('/network')
def network():
    print "Inside network() function"
    retVal = None
    cand   = session['candidate']
    print "In Follower's Network, session['candidate'] is - ", cand
    if cand in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
        fpath = "pages/%s/%s_network.html" % (cand, cand)
        retVal = render_template(fpath)
    else:
        retVal = "Error in topic(). Need to make an error page"
    return retVal


'''
    Renders the Topic Modelling visualization for any candidate
'''
@app.route('/topic')
def topic():
    print "Inside topic() function"
    retVal = None
    cand   = session['candidate']
    print "In Topic Modelling, session['candidate'] is - ", cand
    if cand in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
        fpath = "pages/%s/%s_topicmodel.html" % (cand, cand)
        retVal = render_template(fpath)
    else:
        retVal = "Error in topic(). Need to make an error page"
    return retVal


'''
    Renders the Sentence-level SA page for candidate selected
'''
@app.route('/tweetlevel')
def tweetlevel():
    print "Inside tweet level function" 
    retVal      = None
    cand        = session['candidate']
    tweet_num   = 3 #for testing; will change to 20 when db api methods are finished and available
    print "In Sentence-level, session['candidate'] is - ", cand
    if cand in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
        fpath = "pages/%s/%s_sa_sentence.html" % (cand, cand)
        tweet_list = get_tweets( cand, tweet_num )
        retVal = render_template(fpath, tweet_list=tweet_list)
    else:
        retVal = "Error in tweetlevel()."
    return retVal

'''
    Ensures proper json files are stored for Sentence-level SA Amcharts chart per candidate tweet
'''
@app.route('/change_viz_by_id', methods=['GET','POST'])
def change_viz_by_id():
    retVal   = None
    cand     = session['candidate']
    tweet_id = request.args['id']
    fpath    = "static/data/"
    if cand in ['clinton', 'cruz', 'kasich', 'sanders', 'trump']:
        get_tweet_tones(cand, tweet_id, fpath)
        retVal = ""
    else:
        retVal = "Error in tweetlevel()."
    return retVal
    
'''
    Renders the SA Document-level visualization for any candidate
'''
@app.route('/alltweet')
def alltweet():
    print "Inside All tweets function" 
    cand = session['candidate']
    print "In Document-level, session['candidate'] is - ", cand
    if cand == 'clinton':
        return render_template("pages/clinton/clinton_sa_document.html")
    elif cand == 'cruz':
        return render_template("pages/cruz/cruz_sa_document.html")
    elif cand == 'kasich':
        return render_template("pages/kasich/kasich_sa_document.html")
    elif cand == 'sanders':
        return render_template("pages/sanders/sanders_sa_document.html")
    elif cand == 'trump':
        return render_template("pages/trump/trump_sa_document.html")
    else:
        print "Error in alltweet(). Need to make an error page"



############### Helper Functions #################
'''
    Fetch tweet dictionary from db
    Parameter(s): candidate (Type: string; Descr: Candidate name), tweet_num (Type: int; Descr: Number of tweets in dictionary, e.g. 20)
    Return: List of Tuples, specifically [(tweet_id, tweet_text), ...]    
'''
def get_tweets( candidate, tweet_num ):
    tweet_dict = get_tweet_list( candidate, tweet_num )
    tweet_list = []
    counter = 0
    for key in tweet_dict:
        tweet_list.append((counter, tweet_dict[key]))
        counter += 1
    
    return tweet_list

''' [THIS ONE MAY NOT BE NEEDED]
    Fetch raw tweet json data from db
    Parameter(s): candidate (Type: string; Descr: Candidate name), tweet_id (Type: string; Descr: Tweet identifier)
    This will change likely --> Return: Tuple, specifically (tweet_id, tweet_text, ...)   
'''
#def get_data( candidate, tweet_id ):
#    return get_jsons( candidate, tweet_id )



if __name__ == '__main__':
    app.debug = True
    app.run()



