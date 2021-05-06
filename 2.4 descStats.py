import os
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import logging
from gensim.models import LdaModel
from gensim.models.nmf import Nmf
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle
import gensim.corpora
import gensim.utils
from tqdm import tqdm
import pandas as pd

#  TODO
# - Proportion evolution (see Medium article)
# - Wordcloud by topic (as list with according topic weights in second column)
# - Use Schmeling Wagner as a guide for wordcloud, they're pretty meticulous

# TODO Several useful descriptive insight methods in this article
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#15visualizethetopicskeywords
# https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/#14.-pyLDAVis

#################################################################
# LDAvis
#################################################################

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lda = LdaModel.load("models/lda")
dct = gensim.utils.SaveLoad.load("models/dct")
corpus = gensim.corpora.MmCorpus("models/corpus")
nmf = Nmf.load("models/nmf")

if False:
    ldaDisp = gensimvis.prepare(lda, corpus, dct, sort_topics=False)
    pyLDAvis.save_html(ldaDisp, "ldavistest.html")
    os.startfile(".\ldavistest.html")


#####################################################################################
# Fig 1 JeWu - intertemporal progression of topic mixture
#####################################################################################

# lda.print_topics(5, 10)

minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
minutes = [para for doc in minspickeled for para in doc["filteredParagraphs"]]
