from gensim.models import LdaModel, CoherenceModel
from gensim.models.nmf import Nmf
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import gensim.corpora
import gensim.utils
from envVars import NUM_TOPICS
import pickle
import os.path
import logging
from tqdm import tqdm


# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=1):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in tqdm(range(start, limit, step)):
        model = LdaModel(corpus=corpus,
                         id2word=dictionary,
                         chunksize=2000,
                         alpha='auto',
                         eta='auto',
                         iterations=400,
                         num_topics=num_topics,
                         passes=30,
                         eval_every=None)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


if __name__ == '__main__':
    # Train the LDA model
    SEED = 130
    # NUM_TOPICS = 10  # number of overall topics, following Jegadeesh&Wu
    ALPHA = 0.15  #
    ETA = 1.25  #
    PASSES = 20  # number of iterations to train the model, 50 is default

    minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
    minutes = [para for doc in minspickeled for para in doc["filteredParagraphs"]]
    dct = gensim.corpora.Dictionary(minutes)
    dct.filter_extremes(
        no_below=3,
        no_above=0.85,
        keep_n=5000
    )
    corpus = [dct.doc2bow(paragraph) for paragraph in minutes]

    models, coherenceVals = compute_coherence_values(dct, corpus, minutes, 16, 1, 1)
    print(coherenceVals)

    x_axis = [x for x in range(1, 16)]
    plt.plot(x_axis, coherenceVals)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.show()
