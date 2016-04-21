from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return "This is the index page for word cloud"

@app.route('/homepage')
def homepage():
	return "<h2>  Visualisation will be displayed here </h2>"



@app.route('/index/<key1>')
def indexInitialisation(key1):
	return "Lightining API Key fetched as %s" %key1


@app.route('/index/<key1>')
def indexInitialisation(key1):
	return "Key fetched as %s" %key1

if __name__=="__main__":
	app.run(debug=True)