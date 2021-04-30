# Use N=1 to test for whole-document significance
# Tutorial: https://www.machinelearningplus.com/nlp/gensim-tutorial/#6howtocreateabagofwordscorpusfromatextfile
import gensim
import pickle
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Load the long list of tokenized paragaphs (not separation by article!)
minutes = pickle.load(open("data/2filteredParagraphs", "rb"))

# Map unique IDs to words (id to word mapping - ID2Word)
# Model computations are a lot efficient if IDs are used as word identifiers instead of the strings themselves
# That's the entire reason for using a dictionary
dct = gensim.corpora.Dictionary(minutes)

# TODO Concern by Schmeling and Wagner (very end of section 2.2) that topic modelling could induce hindsight
# bias, as model is trained on entire corpus of articles.
# Do a robustness test where training is only done on the past 5-10 years (simply start in 1993)

# Filter out extremes to limit the number of features
dct.filter_extremes(
    no_below=3,
    no_above=0.85,
    keep_n=5000
)

# Create the corpus, ie the document/term-frequency matrix, aka the bag-of-words (bow)
# Concretely: A list of lists representing paragraphs containing the frequency of terms
# as defined in the dictionary
# Iterate overall all paragraphs and using the dictionary, vectorize every paragraph
corpus = [dct.doc2bow(paragraph) for paragraph in minutes]

# Use TF-IDF to determine "unique (marginal) information content" of a given word
# If word is very prevalent in a given document (paragraph) but appears in few other documents,
# it adds to the unique information content of that document
# If words appears just a number of times but in almost every document, then ceteris-paribus
# those documents cannot be distinguished more easily, as that word is essentially just "white noise"
tfidf = gensim.models.TfidfModel(corpus)
transtfidf = tfidf[corpus]

# Train the LDA model
SEED = 130
TOPICS = 4  # number of overall topics
ALPHA = 0.15  #
ETA = 1.25  #
PASSES = 20  # number of iterations to train the model, 50 is default

# Haven't tested multicore training yet, only works with wrapping te following in - if __name__ == "__main__":
lda = gensim.models.LdaModel(
    corpus=corpus,
    id2word=dct,
    chunksize=2000,
    alpha='auto',
    eta='auto',
    iterations=400,
    num_topics=TOPICS,
    passes=PASSES,
    eval_every=None)

print("---------------------------")
lda.print_topics(10, 10)
print("---------------------------")
lda.save("data/lda.model")

# TODO Use TFIDF corpus instead of vanilla bag-of-words corpus
