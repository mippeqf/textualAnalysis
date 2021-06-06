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
from pprint import pprint
from functools import reduce
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if False:
    minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
    minutes = [para for doc in minspickeled for para in doc["filteredParagraphs"]]
    dct = gensim.corpora.Dictionary(minutes)
    dct.filter_extremes(
        no_below=3,
        no_above=0.85,
        keep_n=5000
    )
    corpus = [dct.doc2bow(paragraph) for paragraph in minutes]
    tfidf = gensim.models.TfidfModel(corpus)
    transtfidf = tfidf[corpus]

    avgScoreArr = []
    topicScoreArr = []
    for num_topics in tqdm(range(1, 20, 1)):
        model = gensim.models.nmf.Nmf(
            corpus=transtfidf,
            num_topics=num_topics,
            id2word=dct,
            chunksize=2000,
            passes=5,
            kappa=.1,
            minimum_probability=0.01,
            w_max_iter=300,
            w_stop_condition=0.0001,
            h_max_iter=100,
            h_stop_condition=0.001,
            eval_every=10,
            normalize=True,
            random_state=42
        )

        output = model.top_topics(corpus, coherence='u_mass', topn=20)
        topicScores = [item[1] for item in output]
        avgScore = 0
        for score in topicScores:
            avgScore += score
        avgScoreArr.append(avgScore/num_topics)
        topicScoreArr.append(topicScores)
        print(avgScore, avgScore/num_topics)

    pickle.dump(topicScoreArr, open("topicCoherenceArr", "wb"))

topics = range(1, 20, 1)

topicScoreArr = pickle.load(open("topicCoherenceArr", "rb"))

avgScoreArr = [sum(arr)/len(arr) for arr in topicScoreArr]
plt.plot(topics, avgScoreArr)
plt.xlabel("Number of topics")
plt.ylabel("Coherence")
plt.title("Average coherence score per topic")
plt.savefig("img/coherenceAgg.png")
plt.clf()

# Fill missing values
dataNew = []
for vals in topicScoreArr:
    newVals = vals
    for j in range(0, 20-len(vals)):
        newVals.append(None)
    dataNew.append(newVals)
datanewnew = [[]for i in range(1, 20)]

# Transpose dataframe
for i in range(0, 19):
    for j in range(0, 19):
        datanewnew[i].append(dataNew[j][i])

for i, series in enumerate(datanewnew):
    plt.plot(topics, series)
    plt.ylim([-2.5, -1])
    plt.xlim([1, 20])
    plt.tight_layout()
    if i <= 16:
        plt.subplot(4, 5, i+1)
plt.savefig("img/coherenceIndividual.png")

exit()


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
    tfidf = gensim.models.TfidfModel(corpus)
    transtfidf = tfidf[corpus]

    models, coherenceVals = compute_coherence_values(dct, transtfidf, minutes, 16, 1, 1)
    print(coherenceVals)

    x_axis = [x for x in range(1, 16)]
    plt.plot(x_axis, coherenceVals)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.show()
