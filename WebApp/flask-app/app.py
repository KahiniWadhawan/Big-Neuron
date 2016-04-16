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

from flask import Flask, render_template, request, session, g

app = Flask(__name__)

# Sessions variables are stored client side, on the users browser
# the content of the variables is encrypted, so users can't
# actually see it. They could edit it, but again, as the content
# wouldn't be signed with this hash key, it wouldn't be valid
# You need to set a scret key (random text) and keep it secret
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

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
    if request.method == "POST":

        radio = request.form['candidate'] #this retrieves which radio button was pressed

        session['candidate'] = radio
        if radio == 'clinton':
            return render_template("pages/clinton/clinton.html", cand=radio)
        elif radio == 'cruz':
            return render_template("pages/cruz/cruz.html")
        elif radio == 'kasich':
            return render_template("pages/kasich/kasich.html")
        elif radio == 'sanders':
            return render_template("pages/sanders/sanders.html")
        elif radio == 'trump':
            return render_template("pages/trump/trump.html")
        else:
            print "Error in select_candidate(). Need to make an error page"

'''
    Load wordcloud visualization from their respective candidate pages
'''
@app.route("/wordcloud", methods = ["GET", "POST"])
def wordcloud():
    print "Inside wordcloud()"
    cand = session['candidate']
    print "In wordcloud, session['candidate'] is - ", cand
    if cand == 'clinton':
        return render_template("pages/clinton/clinton_wordcloud.html")
    elif cand == 'cruz':
        return render_template("pages/cruz/cruz_wordcloud.html")
    elif cand == 'kasich':
        return render_template("pages/kasich/kasich_wordcloud.html")
    elif cand == 'sanders':
        return render_template("pages/sanders/sanders_wordcloud.html")
    elif cand == 'trump':
        return render_template("pages/trump/trump_wordcloud.html")
    else:
        print "Error in wordcloud(). Need to make an error page"

'''
    Load tweet (sentence) level visualizations from their respective candidate pages
'''
@app.route("/tweet_level", methods = ["GET", "POST"])
def tweet_level():
    print "Inside tweet_level()"
    cand = session['candidate']
    print "In tweet_level, session['candidate'] is - ", cand
    if cand == 'clinton':
        return render_template("pages/clinton/clinton_sa_sentence.html")
    elif cand == 'cruz':
        return render_template("pages/cruz/cruz_sa_sentence.html")
    elif cand == 'kasich':
        return render_template("pages/kasich/kasich_sa_sentence.html")
    elif cand == 'sanders':
        return render_template("pages/sanders/sanders_sa_sentence.html")
    elif cand == 'trump':
        return render_template("pages/trump/trump_sa_sentence.html")
    else:
        print "Error in tweet_level(). Need to make an error page"
        
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
@app.route('/followers')
def followers():
    print "Inside followers " 
    return none

'''
    Renders the Topic Modelling visualization for any candidate
'''
@app.route('/topic')
def topic():
    print " Inside Topic Modelling " 
    return none

'''
    Renders the SA Sentence-level visualization for any candidate
'''
@app.route('/tweetlevel')
def tweetlevel():
    print "Inside Tweet Level" 
    return none

'''
    Renders the SA All tweets visualization for any candidate
'''
@app.route('/alltweet')
def alltweet():
    print "All tweets" 
    return none

if __name__ == '__main__':
    app.debug = True
    app.run()
