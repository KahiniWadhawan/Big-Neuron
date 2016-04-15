#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Jessica"
__date__ = "$Apr 14, 2016 11:39:45 PM$"

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test():
    return "Hello, World!"

@app.route('/index')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
