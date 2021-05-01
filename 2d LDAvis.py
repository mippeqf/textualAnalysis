from gensim.models.nmf import Nmf
from gensim.models import LdaModel
import logging
import pickle
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lda = LdaModel.load("models/lda")
dct = pickle.load(open("models/dct.pkl", "rb"))
corpus = pickle.load(open("models/corpus.pkl", "rb"))
nmf = Nmf.load("models/nmf")

ldaDisp = gensimvis.prepare(nmf, corpus, dct, sort_topics=False)
pyLDAvis.save_html(ldaDisp, "ldavistest.html")
os.startfile(".\ldavistest.html")
