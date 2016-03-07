#---------------------------------------------------------------------------
#Author: Kahini Wadhawan
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#This file creates features from bow corpus. It applies TF-IDF, LSI and LDA
# to find topics.
#---------------------------------------------------------------------------

import gensim
import logging
import os
from gensim import corpora, models

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
#                     level=logging.INFO)
