#-----------------------------------------------------------
#Author: Kahini Wadhawan

#-----------------------------------------------------------
#-----------------------------------------------------------
# This file provides Big Neuron mongo db access functions
#-----------------------------------------------------------
from pymongo import MongoClient


#--------------------------------------------------------------
# Function to setup connection with database
#---------------------------------------------------------------
def connect_db():
    #Creating a client out of Mongodb running on localhost
    client = MongoClient('localhost', 27017)
    #Switch to Big_Neuron database
    db = client.Big_Neuron
    return db


#--------------------------------------------------------------------
# Function to fetch sentiment json from tweets_sentiments collection
# Function Arguments: 1) limit - the no. of sentiment jsons you want
# Don't pass any argument if you want all of 3.2k tweets sentiments jsons
#---------------------------------------------------------------------
def fetch_sentiment_json(limit=None):
    #Setting up db connection
    db = connect_db()
    cursor = None

    if limit == None:
        cursor = db.tweets_sentiments.find()
    else:
        cursor = db.tweets_sentiments.find().limit(limit)

    for document in cursor:
        #print("before yield:: ",document)
        #Using yield to generate list of jsons on the fly
        #This will increase the iteration speed
        yield (document)



#-----------------------------------------------------------------
# Function testing
# Code block to do testing of functions in this file
#-----------------------------------------------------------------
#fetch_sentiment_json yeilds jsons on the fly
#So, usage given below, docs is a generator object
docs = fetch_sentiment_json(5)
print(docs)
#iterating over generator object
for doc in docs:
   print(doc)

