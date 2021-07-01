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
import math

# TODO Several useful descriptive insight methods in this article
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#15visualizethetopicskeywords
# https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/#14.-pyLDAVis

if not os.path.exists("img"):
    os.mkdir("img")

#####################################################################################
# Wordcloud by topic
#####################################################################################

# Load model(s)
# lda = LdaModel.load("models/lda")
dct = gensim.utils.SaveLoad.load("models/dct")
corpus = gensim.corpora.MmCorpus("models/corpus")
nmf = Nmf.load("models/nmf")

# Generate word cloud for final model
labels = {1: "Economic activity", 2: "Policy action", 3: "Economic outlook", 4: " Employment", 5: "Financial Markets", 6: "Inflation"}
for topic in range(0, NUM_TOPICS):
    termsnmf = nmf.show_topic(topic, topn=50)
    # Model returns list of tuples, wordcloud wants a dictionary instead
    wordcloudnmf = WordCloud(background_color="white").generate_from_frequencies(dict(termsnmf))
    plt.subplot(3, 2, topic+1)
    plt.imshow(wordcloudnmf)
    plt.axis("off")
    plt.title(str(topic+1)+" - "+labels[topic+1])
plt.tight_layout()
# plt.suptitle("NMF wordclouds by topic")
plt.savefig(f"img/nmf_topic.png")
plt.clf()

# Generate word clouds for all 20 topics and save to folder img/nmfClouds
# Not needed for the thesis, only to subjectively select the best model
if False:
    # GENERATE WORDCLOUDS FOR SUBJECTIVE MODEL SELECTION
    for numtopics in range(1, 21):
        nmf = Nmf.load("models/nmf"+str(numtopics))
        rows = math.ceil(math.sqrt(numtopics))
        cols = math.ceil(numtopics/rows)
        for topic in range(1, numtopics+1):
            print("numtopics", numtopics, "rows", rows, "cols", cols, "topic", topic)
            termsnmf = nmf.show_topic(topic-1, topn=50)
            wordcloudnmf = WordCloud(background_color="white").generate_from_frequencies(dict(termsnmf))
            plt.subplot(rows, cols, topic)
            plt.imshow(wordcloudnmf)
            plt.axis("off")
            plt.title("Topic"+str(topic))
        plt.tight_layout()
        # plt.suptitle("NMF wordclouds by topic")
        plt.savefig(f"img/nmfClouds/nmf"+str(numtopics)+".png")
        plt.show()
        plt.clf()

# exit()

#####################################################################################
# intertemporal progression of topic mixture
#####################################################################################

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "dataExport"), "rb"))

df = pd.DataFrame(minutes)
df = df[["release", *["nmfProp"+str(i) for i in range(1, NUM_TOPICS+1)]]]
print(df.head())
df.rename(columns={"nmfProp1": "Economic activity", "nmfProp2": "Policy action", "nmfProp3": "Economic Outlook",
                   "nmfProp4": "Employment", "nmfProp5": "Financial Markets", "nmfProp6": "Inflation"}, inplace=True)
order = [5, 4, 3, 2, 1, 0]
df.plot.area(stacked=True, x="release")
ax = plt.subplot(111)
box = ax.get_position()
plt.legend(labels=["asdf" for i in range(0, 6)])
ax.set_position([box.x0+box.width*0.01, box.y0 + box.height * 0.03, box.width*0.99, box.height * 0.97])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
# plt.title("NMF topic proportions stacked")
plt.tight_layout()
plt.margins(x=0, y=0, tight=True)
plt.ylim(0, 1)
# plt.xlabel("Publication date")
# plt.ylabel("Topic proportion")
plt.xlabel("")
plt.savefig("img/nmfPropStacked.png")
plt.clf()

exit()

# Stuff in the following is not used anymore

#################################################################
# LDAvis
#################################################################

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

ldaDisp = gensimvis.prepare(lda, corpus, dct, sort_topics=False)
pyLDAvis.save_html(ldaDisp, "ldavistest.html")
os.startfile(".\ldavistest.html")


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

if False:
    minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "dataExport"), "rb"))
    df = pd.DataFrame(minutes)
    df = df[["release", "ldaProp1", "ldaProp2", "ldaProp3", "ldaProp4", "ldaProp5", "ldaProp6", "ldaProp7", "ldaProp8"]]
    df.plot.area(stacked=True, x="release").legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.title("LDA topic proportions stacked")
    plt.savefig("img/ldaPropStacked.png")
    plt.clf()
