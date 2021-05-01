import os
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import logging
from gensim.models import LdaModel
from gensim.models.nmf import Nmf
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle

filteredParagraphs = pickle.load(open("data/2filteredParagraphs", "rb"))
rawParagraphs = pickle.load(open("data/2rawParagraphs", "rb"))

# Flatten main list for word cloud
flattenedList = [token for paragraph in filteredParagraphs for token in paragraph]
wordcloud = WordCloud(background_color="white").generate(','.join(flattenedList))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Same for raw paragraphs as a comparison
flattenedList = [token for paragraph in rawParagraphs for token in paragraph]
wordcloud = WordCloud(background_color="white").generate(','.join(flattenedList))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lda = LdaModel.load("models/lda")
dct = pickle.load(open("models/dct.pkl", "rb"))
corpus = pickle.load(open("models/corpus.pkl", "rb"))
nmf = Nmf.load("models/nmf")

ldaDisp = gensimvis.prepare(nmf, corpus, dct, sort_topics=False)
pyLDAvis.save_html(ldaDisp, "ldavistest.html")
os.startfile(".\ldavistest.html")


# TODO Do some sort of table showing the most common words overall, most common negative and most common positive words
# similar to the table in Schmeling and Wagner
