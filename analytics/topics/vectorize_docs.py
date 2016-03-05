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


