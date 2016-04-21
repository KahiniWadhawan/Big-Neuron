from flask import Flask,request,render_template

app = Flask(__name__)

'''
@app.route('/')
def index():
	return "This is the index page for word cloud" %request.method
'''
'''
@app.route('/')
def index():
	return "This is the index page for word cloud"
'''
@app.route('/')
def index():
	return "This is the index page for word cloud"

@app.route('/homepage',methods=['GET','POST'])
def homepage():
	return "<h2>  Visualisation will be displayed here </h2>"

'''

@app.route('/index/<key1>')
def indexInitialisation(key1):
	return "Lightining API Key fetched as %s" %key1
'''

@app.route('/index/<key1>')
def indexInitialisation(key1):
	return "Key fetched as %s" %key1


@app.route('/index/<int:key2>')
def indexInitialisation2(key2):
	return "<h1>Key fetched as %s</h1>" %key2

'''
'''
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

'''
'''
@app.route('/Realtime')
def Realtime():
	return render_template("index.html")

@app.route('/WordCloud')
def WordCloud():
	return "This is the index page for word cloud"%request.method


if __name__=="__main__":
	app.run()