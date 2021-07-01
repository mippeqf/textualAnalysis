from gensim.models import LdaModel, CoherenceModel
from gensim.models.nmf import Nmf
import matplotlib.pyplot as plt
import gensim.corpora
import gensim.utils
from envVars import NUM_TOPICS
import pickle
import os.path
import logging
from tqdm import tqdm
from pprint import pprint
from functools import reduce
import matplotlib.pyplot as plt
from gensim.models.coherencemodel import CoherenceModel
import csv

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Compute coherence scores, skipped this section for debugging the plotting section
# Alt method with CoherenceModel is based on https://towardsdatascience.com/topic-modeling-articles-with-nmf-8c6b2a227a45
if True and __name__ == '__main__':
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
    coherenceScoreAlt = []
    for num_topics in tqdm(range(1, 21, 1)):
        print("Starting to train nmf model")
        model = gensim.models.nmf.Nmf(
            corpus=transtfidf,
            num_topics=num_topics,
            id2word=dct,
            chunksize=2000,
            passes=50,
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
        print("Saving nmf model")

        model.save("models/nmf"+str(num_topics))

        # MANUAL APPROACH, CoherenceModel below does the same, but only provides the aggregated values
        output = model.top_topics(corpus=transtfidf, texts=minutes, coherence='u_mass', topn=20)
        topicScores = [item[1] for item in output]
        avgScore = 0
        for score in topicScores:
            avgScore += score
        avgScoreArr.append(avgScore/num_topics)
        topicScoreArr.append(topicScores)
        print(avgScore, avgScore/num_topics)

        print("Starting to apply coherence model")

        cm = CoherenceModel(
            model=model,
            corpus=transtfidf,
            texts=minutes,
            dictionary=dct,
            coherence='u_mass'
        )
        coherenceScoreAlt.append(round(cm.get_coherence(), 5))

        # print("Finished using coherence model, next iteration")

    pickle.dump(topicScoreArr, open("coherenceDump", "wb"))
    pickle.dump(coherenceScoreAlt, open("coherenceDumpAlt", "wb"))

# exit()

coherenceScore = pickle.load(open("coherenceDump", "rb"))
coherenceScoreAlt = pickle.load(open("coherenceDumpAlt", "rb"))

avgScoreArr = [sum(arr)/len(arr) for arr in coherenceScore]
plt.plot(range(1, 21, 1), avgScoreArr)
plt.xlabel("Number of topics")
plt.ylabel("Coherence")
plt.title("Average coherence score per topic")
plt.savefig("img/coherenceManual.png")
plt.clf()

plt.plot(range(1, 21, 1), coherenceScoreAlt)
plt.xlabel("Number of topics")
plt.ylabel("Coherence")
plt.title("Coherence score using gensim's CoherenceModel")
plt.savefig("img/coherenceAlt.png")
plt.clf()

# Fill missing values
dataNew = []
for vals in coherenceScore:
    newVals = vals
    for j in range(0, 21-len(vals)):
        newVals.append(None)
    dataNew.append(newVals)
datanewnew = [[]for i in range(1, 21)]

# Transpose dataframe
for i in range(0, 20):
    for j in range(0, 20):
        datanewnew[i].append(dataNew[j][i])

for i, series in enumerate(datanewnew):
    plt.plot(range(1, 21, 1), series)
    plt.ylim([-2.5, -1])
    plt.xlim([1, 20])
    plt.tight_layout()
    if i <= 20:
        plt.subplot(4, 5, i+1)
plt.savefig("img/coherenceIndividual.png")

with open(os.path.join(os.path.dirname(__file__), "coherenceExport.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(dataNew)

with open(os.path.join(os.path.dirname(__file__), "coherenceAggExport.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for val in coherenceScoreAlt:
        writer.writerow([val])

exit()


# Stuff below here is most likely not in active use anymore

# LDA no longer needed!
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
