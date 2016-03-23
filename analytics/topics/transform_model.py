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

def transform(model_val):
    #----------------------------------------------------------------------------------
    # Loading dictionary and corpus generated by gensim bow model
    # by vectorize_docs file
    #----------------------------------------------------------------------------------
    gensim_models_DIR = "path to dir like gensim_models"
    dictionary = gensim.corpora.Dictionary.load(os.path.join(gensim_models_DIR, "twitterSearch.dict"))
    corpus = gensim.corpora.MmCorpus(os.path.join(gensim_models_DIR, "twitterSearch.mm"))

    #--------------------------------------------------------------------
    # Applying transformation on vectorized corpus
    # Projection to reduced dimension - can try LDA, PCA and other algorithms
    #--------------------------------------------------------------------
    topics_num = 5
    tfidf = models.TfidfModel(corpus, normalize=True)
    if (model_val == 'lsi'):
        model = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=topics_num
                                ,onepass=True, power_iters=2)
    elif(model_val== 'lda'):
        clipped_corpus = gensim.utils.ClippedCorpus(corpus, corpus.num_docs)
        model = models.LdaModel(clipped_corpus, id2word=dictionary, num_topics=topics_num,
                                passes=10)


    #-------------------------------------------------------------------
    # Writing coordinates to a csv file
    #-------------------------------------------------------------------
    csv_file_path = os.path.join(gensim_models_DIR, "transform_coords.csv")
    if os.path.isfile(csv_file_path):
        os.remove(csv_file_path)
    fcoords = open(csv_file_path, 'wb')
    for vector in model[corpus]:
        if len(vector) != topics_num:
            continue
        #vector[0][1]....vector[topics_num-1][1] - docs - topic dist.
        fcoords.write("%6.4f\t%6.4f\n" % (vector[0][1], vector[1][1]))
    fcoords.close()

