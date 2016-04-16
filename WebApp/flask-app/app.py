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
    Renders the realtime dashboard for any candidate
'''
@app.route('/realtime')
def realtime():
    print "REQUEST from realtime---", request
    return render_template("realtime.html")

'''
    Renders the landing dashboard for each candidate
'''
@app.route("/candidate", methods = ["GET", "POST"])
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

'''
    Load visualizations from their respective candidate pages
'''
@app.route("/wordcloud", methods = ["GET", "POST"])
def wordcloud():
    print "Inside wordcloud()"
    r = session['candidate']
    print "In wordcloud, request.candidate is - ", r

    if r == 'clinton':
        return render_template("pages/clinton/clinton_wordcloud.html")
    else:
        print "ERROR"
        pass

if __name__ == '__main__':
    app.debug = True
    app.run()



