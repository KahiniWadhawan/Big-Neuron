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
# from dummy_db import get_tweet_list, get_tweet_tones  #Do we have a tone analyzer module -or- are we inserting tweets by hand into IBM tone analyzer to get the json output?
# import sys
# sys.path.insert(0, '../../databases/cassandra/')
# from bigneuron_cassandradb_api import get_tweet_list, get_tweet_tones

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
    print "request.form['candidate']  =",request.form['candidate'] 
    if request.method == "POST":
        if request.form["action"] == "Submit":
            print "SUBMIT"
            radio = request.form['candidate'] #this retrieves which radio button was pressed
            session['candidate'] = radio
            print "radio is -", radio
            # if radio == "trump":
            #     radio = "realDonaldTrump"
            if radio == 'clinton':
                print "Inside Sub clintn"
                return render_template("pages/clinton/clinton.html", cand=radio)
            elif radio == 'cruz':
                return render_template("pages/cruz/cruz.html", cand=radio)
            elif radio == 'kasich':
                return render_template("pages/kasich/kasich.html", cand=radio)
            elif radio == 'sanders':
                return render_template("pages/sanders/sanders.html", cand=radio)
            elif radio == 'trump':
                return render_template("pages/trump/trump.html", cand=radio)
            else:
                retVal = "Error in select_candidate(). Need to make an error page"
                return retVal
        elif request.form["action"] == "Realtime":
            print "REALTIME"
            radio = request.form['candidate'] #this retrieves which radio button was pressed
            session['candidate'] = radio
            print "Realtime radio is -", radio
            # if radio == "trump":
            #     radio = "realDonaldTrump"
            if radio == 'clinton':
                print "Inside realtime clintn"
                return render_template("pages/clinton/clinton_realtime.html", cand=radio)
            elif radio == 'cruz':
                return render_template("pages/cruz/cruz_realtime.html", cand=radio)
            elif radio == 'kasich':
                return render_template("pages/kasich/kasich_realtime.html", cand=radio)
            elif radio == 'sanders':
                return render_template("pages/sanders/sanders_realtime.html", cand=radio)
            elif radio == 'realDonaldTrump':
                return render_template("pages/trump/trump_realtime.html", cand=radio)
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
    if cand == 'clinton':
        return render_template("pages/clinton/clinton_wordcloud.html")
    elif cand == 'cruz':
        return render_template("pages/cruz/cruz_wordcloud.html")
    elif cand == 'kasich':
        return render_template("pages/kasich/kasich_wordcloud.html")
    elif cand == 'sanders':
        return render_template("pages/sanders/sanders_wordcloud.html")
    elif cand == 'realDonaldTrump':
        return render_template("pages/trump/trump_wordcloud.html")
    else:
        retVal = "Error in topic(). Need to make an error page"
    return retVal


'''
    Renders the realtime page for any candidate
'''
@app.route('/realtime', methods = ["GET", "POST"])
def realtime():
    retVal = ""
    print "Inside Realtime section! ", request
    
   
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
        retVal = render_template(fpath, cand=cand)
    else:
        retVal = "Error in topic(). Need to make an error page"
    return retVal


'''
    Renders the Sentence-level SA page for candidate selected
    Renders the SA Sentence-level visualization for any candidate
'''
@app.route('/tweetlevel')
def tweetlevel():
    print "Inside tweet level function"
    cand        = session['candidate']
    if cand == "trump":
        cand = "realDonaldTrump"
    print "CANDIDATE NAME IS --", cand
    tweet_num = 20 #for testing;
    print "In Sentence-level, session['candidate'] is - ", cand
    if cand == 'HillaryClinton':
        tweet_list = get_tweets( cand, tweet_num )
        return render_template("pages/clinton/clinton_sa_sentence.html",tweet_list=tweet_list )
    elif cand == 'tedcruz':
        tweet_list = get_tweets( cand, tweet_num )
        return render_template("pages/cruz/cruz_sa_sentence.html",tweet_list=tweet_list)
    elif cand == 'JohnKasich':
        tweet_list = get_tweets( cand, tweet_num )
        return render_template("pages/kasich/kasich_sa_sentence.html",tweet_list=tweet_list)
    elif cand == 'BernieSanders':
        tweet_list = get_tweets( cand, tweet_num )
        return render_template("pages/sanders/sanders_sa_sentence.html",tweet_list=tweet_list)
    elif cand == 'realDonaldTrump':
        print "inside the trump section--", cand
        tweet_list = get_tweets( cand, tweet_num )
        return render_template("pages/trump/trump_sa_sentence.html",tweet_list=tweet_list)
    else:
        print "Error in tweetlevel(). Need to make an error page"


'''
    For tweetlevel()
    Ensures proper json files are stored for Sentence-level SA Amcharts chart per candidate tweet
'''
@app.route('/change_viz_by_id', methods=['GET','POST'])
def change_viz_by_id():
    retVal   = None
    cand     = session['candidate']
    if cand=="trump":
        cand = "realDonaldTrump"
    tweet_id = request.args['id'] #serial 1,2,3..
    fpath    = "static/data/"
    if cand in ['realDonaldTrump','clinton', 'cruz', 'kasich', 'sanders', 'trump']:
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
    For tweetlevel()
    Fetch tweet dictionary from db
    Parameter(s): candidate (Type: string; Descr: Candidate name), tweet_num (Type: int; Descr: Number of tweets in dictionary, e.g. 20)
    Return: List of Tuples, specifically [(tweet_id, tweet_text), ...]
'''
def get_tweets( candidate, tweet_num ):
    tweet_dict = get_tweet_list( candidate, tweet_num )
    tweet_list = []
    for key in tweet_dict:
        print('KEY :: ', key)
        print('TWEET DICT KEY :: ', tweet_dict[key])
        tweet_list.append((key, tweet_dict[key]))
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



