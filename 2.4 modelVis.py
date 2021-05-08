import os
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import logging
from gensim.models import LdaModel
from gensim.models.nmf import Nmf
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import gensim.corpora
import gensim.utils

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

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

# minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
# minutes = [para for doc in minspickeled for para in doc["filteredParagraphs"]]

if not os.path.exists("img"):
    os.mkdir("img")

for topic in range(0, 8):
    termslda = lda.show_topic(topic, topn=50)  # get_topic_terms would return words as dict IDs, not strings
    # Model returns list of tuples, wordcloud wants a dictionary instead
    wordcloudlda = WordCloud(background_color="white").generate_from_frequencies(dict(termslda))
    plt.imshow(wordcloudlda)
    plt.axis("off")
    plt.savefig(f"img/lda_topic_{topic+1}.png")

for topic in range(0, 8):
    termsnmf = nmf.show_topic(topic, topn=50)
    # Model returns list of tuples, wordcloud wants a dictionary instead
    wordcloudnmf = WordCloud(background_color="white").generate_from_frequencies(dict(termsnmf))
    plt.imshow(wordcloudnmf)
    plt.axis("off")
    plt.savefig(f"img/nmf_topic_{topic+1}.png")
