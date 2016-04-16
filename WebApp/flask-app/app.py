#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
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
            retVal = render_template("pages/clinton.html")
        elif radio == 'cruz':
            retVal = render_template("pages/cruz.html")
        elif radio == 'C':
            retVal = render_template("pages/kasich.html")
        elif radio == 'D':
            retVal = render_template("pages/sanders.html")
        elif radio == 'E':
            retVal = render_template("pages/trump.html")
    return retVal

if __name__ == '__main__':
    app.run(debug=True)
