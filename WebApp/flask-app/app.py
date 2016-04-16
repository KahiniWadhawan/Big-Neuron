''' Authors - 
        Jessica Lynch
        Tanvi Parikh
    Purpose - 
        Integration of Flask with Webapp
'''

__author__ = "Jessica, Tanvi"
__date__ = "$Apr 14, 2016 11:39:45 PM$"

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/realtime')
def realtime():
    return render_template("realtime.html")

@app.route("/candidatepage", methods = ["GET", "POST"])
def select_candidate():
    if request.method == "POST":

        radio = request.form['candidate'] #this retrieves which radio button was pressed

        if radio == 'clinton':
            return render_template("pages/clinton/clinton.html")
        elif radio == 'cruz':
            return render_template("pages/cruz/cruz.html")
        elif radio == 'C':
            return render_template("pages/kasich/kasich.html")
        elif radio == 'D':
            return render_template("pages/sanders/sanders.html")
        elif radio == 'E':
            return render_template("pages/trump/trump.html")

if __name__ == '__main__':
    app.debug = True
    app.run()



