#-----------------------------------------------------------------
#Author: Kahini Wadhawan
#----------------------------------------------------------------
#----------------------------------------------------------------------------
# This file contains Gensim module processing. It requires search_twitter.py
# to be executed before resulting in text file of pulled tweets from Twitter.
#----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
import logging
import nltk
import os
import pickle
import gensim
from gensim import corpora, models

#---------------------------------------------------------------------
# Paths for texts dir, models_dir
#---------------------------------------------------------------------
twitter_texts_DIR = "../data/twitter_texts"
gensim_models_DIR = "../data/gensim_models"
stoplist = set(nltk.corpus.stopwords.words("english"))

# #--------------------------------------------------------------------
# # Gensim module code
# # Logging the Gensim events
# #--------------------------------------------------------------------
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#--------------------------------------------------------------------
# Text pre-processing and creation of bag of words format
#--------------------------------------------------------------------
def iter_docs(topdir, stoplist):
    for fn in os.listdir(topdir):
        if fn.__eq__('tweets.txt'):
            fin = open(os.path.join(topdir, fn), 'rb')
            text = fin.read()
            texts = text.split("----------------------")[:-1]

            #iterating over texts list - every text = one tweet - treated as one doc
            for text in texts:
                yield (x for x in
                        gensim.utils.tokenize(text, lowercase=True, deacc=True,
                                        errors="ignore")
                        if x not in stoplist)

            fin.close()


class MyCorpus(object):

        def __init__(self, topdir, stoplist):
            self.topdir = topdir
            self.stoplist = stoplist
            self.dictionary = gensim.corpora.Dictionary(iter_docs(topdir, stoplist))

        def __iter__(self):
            for tokens in iter_docs(self.topdir, self.stoplist):
                yield self.dictionary.doc2bow(tokens)


def gen_bowModel():
    #---------------------------------------------------------------------
    # Creating dictionary from tokens generated from texts and
    # store the dictionary, for future reference
    #Corpus Streaming code for bulk of documents
    #---------------------------------------------------------------------
    corpus = MyCorpus(twitter_texts_DIR, stoplist)
    dict_file_path = os.path.join(gensim_models_DIR, "twitterSearch.dict")
    if os.path.isfile(dict_file_path):
        os.remove(dict_file_path)
    corpus.dictionary.save(dict_file_path)

    #---------------------------------------------------------------------
    #Saving corpus by serializing
    #---------------------------------------------------------------------
    corpus_file_path = os.path.join(gensim_models_DIR, "twitterSearch.mm")
    if os.path.isfile(corpus_file_path):
        os.remove(corpus_file_path)
    corpora.MmCorpus.serialize(corpus_file_path, corpus)

