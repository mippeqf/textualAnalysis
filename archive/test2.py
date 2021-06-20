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

numtopics = 4
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
