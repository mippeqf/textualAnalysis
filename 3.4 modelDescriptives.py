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
from envVars import NUM_TOPICS
import pickle
import pandas as pd

#  TODO
# - Proportion evolution (see Medium article)
# - Wordcloud by topic (as list with according topic weights in second column)
# - Use Schmeling Wagner as a guide for wordcloud, they're pretty meticulous

# TODO Several useful descriptive insight methods in this article
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#15visualizethetopicskeywords
# https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/#14.-pyLDAVis

if not os.path.exists("img"):
    os.mkdir("img")

#####################################################################################
# Fig 1 JeWu - intertemporal progression of topic mixture
#####################################################################################
if False:
    minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "dataExport"), "rb"))
    df = pd.DataFrame(minutes)
    df = df[["release", "ldaProp1", "ldaProp2", "ldaProp3", "ldaProp4", "ldaProp5", "ldaProp6", "ldaProp7", "ldaProp8"]]
    df.plot.area(stacked=True, x="release").legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.title("LDA topic proportions stacked")
    plt.savefig("img/ldaPropStacked.png")
    plt.clf()

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "dataExport"), "rb"))
df = pd.DataFrame(minutes)
df = df[["release", *["nmfProp"+str(i) for i in range(1, NUM_TOPICS+1)]]]
df.plot.area(stacked=True, x="release").legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.title("NMF topic proportions stacked")
plt.tight_layout()
plt.savefig("img/nmfPropStacked.png")
plt.clf()

#####################################################################################
# Wordcloud by topic
#####################################################################################

lda = LdaModel.load("models/lda")
dct = gensim.utils.SaveLoad.load("models/dct")
corpus = gensim.corpora.MmCorpus("models/corpus")
nmf = Nmf.load("models/nmf")

if False:
    for topic in range(0, NUM_TOPICS):
        termslda = lda.show_topic(topic, topn=50)  # get_topic_terms would return words as dict IDs, not strings
        # Model returns list of tuples, wordcloud wants a dictionary instead
        wordcloudlda = WordCloud(background_color="white").generate_from_frequencies(dict(termslda))
        plt.subplot(3, 3, topic+1)
        plt.imshow(wordcloudlda)
        plt.axis("off")
        plt.title("Topic"+str(topic+1))
    plt.suptitle("LDA wordclouds by topic")
    plt.savefig(f"img/lda_topic.png")
    plt.clf()

for topic in range(0, NUM_TOPICS):
    termsnmf = nmf.show_topic(topic, topn=50)
    # Model returns list of tuples, wordcloud wants a dictionary instead
    wordcloudnmf = WordCloud(background_color="white").generate_from_frequencies(dict(termsnmf))
    plt.subplot(3, 3, topic+1)
    plt.imshow(wordcloudnmf)
    plt.axis("off")
    plt.title("Topic"+str(topic+1))
plt.suptitle("NMF wordclouds by topic")
plt.savefig(f"img/nmf_topic.png")
plt.clf()

exit()
#################################################################
# LDAvis
#################################################################

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

ldaDisp = gensimvis.prepare(lda, corpus, dct, sort_topics=False)
pyLDAvis.save_html(ldaDisp, "ldavistest.html")
os.startfile(".\ldavistest.html")
