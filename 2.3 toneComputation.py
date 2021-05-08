# PURPOSE
# Simple Application of LM dictionary (bag of words approach)
#
# Naive Bayes (Antweiler & Frank und Problem 15 of Hillert's course) requires manual classification
# of a training data set, because Bayes needs prior probabilities obvs.
#
# Not sure where Stemming and Lemmtization could be relevant, but I don't see the need for it right now
# Word complexity, sentence length and Jaccard similarity are all aditional tools that can be used, but
# are not necessary for tonal analysis
#
# Use only modern Minutes for now, if there's enough time, see if reliable release schedule of
# Minutes of Actions (67-93) can be obtained.

# pysentiment don't give access to uncertainty score!
# Copy query structure and implement yourself!
# import pysentiment2 as ps
from bs4 import BeautifulSoup
import csv
import pickle
import pandas as pd
import gensim.utils
import os.path
from tqdm import tqdm

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
# Minutes are a list of dictionaries with fields year, meeting, link, and list of lists containing preprocessed paragraphs

dct = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "dct"))
lda = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "lda"))
nmf = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "nmf"))

minutesNew = []

lmRAW = pd.read_csv(os.path.join(os.path.dirname(__file__), "statics", "LmDict.csv"))
lmPOS = set(lmRAW.query('Positive > 0')['Word'])
lmNEG = set(lmRAW.query('Negative > 0')['Word'])
lmUNCERT = set(lmRAW.query('Uncertainty > 0')['Word'])

# Compute document-level tone/uncert and topic-specific scores - qualitative topics
minutes.reverse()
for i, row in enumerate(tqdm(minutes)):

    netToneScoreAggLda = {i: 0 for i in range(0, 8)}
    uncertScoreAggLda = {i: 0 for i in range(0, 8)}
    netToneScoreAggNmf = {i: 0 for i in range(0, 8)}
    uncertScoreAggNmf = {i: 0 for i in range(0, 8)}
    topTopicLdaAgg = {i: 0 for i in range(0, 8)}
    topTopicNmfAgg = {i: 0 for i in range(0, 8)}
    topicAgg = {i: 0 for i in range(0, 8)}
    totalLength = sum([len(para) for para in row["rawParagraphs"]])  # total length of entire document
    docLevelNetToneScore = 0
    docLevelUncertScore = 0
    posnegcounter = 0
    uncertcounter = 0

    for paragraph in row["filteredParagraphs"]:

        # Skip if paragraph is empty, would crash the /len(paragraph) part without
        if not len(paragraph):
            continue

        # Feed text into topic models
        bow = dct.doc2bow(paragraph)  # generate word vector / bag-of-words from tokenized paragraph
        ldatopics = lda.get_document_topics(bow, minimum_phi_value=0.01)  # Paramter necessary, bug in the library
        nmftopics = nmf.get_document_topics(bow)

        # Iterate through text to count LM term corruences
        posScore = 0
        negScore = 0
        uncertScore = 0
        for token in paragraph:
            if token.upper() in lmPOS:
                posScore += 1
            if token.upper() in lmNEG:
                negScore += 1
            if token.upper() in lmUNCERT:
                uncertScore += 1

        # COMPUTE PARAGRAPH-LEVEL METRICS AND ADD TO AGGREGATORS

        # Sentiment by topic (net tone and uncertainty)
        for index, weight in ldatopics:  # Iterate through Lda topics
            # EQUATION 6 IN JEWU (PAGE 17)
            netToneScoreAggLda[index] += (posScore-negScore)*weight/len(paragraph)
            uncertScoreAggLda[index] += uncertScore*weight/len(paragraph)
        for index, weight in nmftopics:  # Iterate through Nmf topics
            netToneScoreAggNmf[index] += (posScore-negScore)*weight/len(paragraph)
            uncertScoreAggNmf[index] += uncertScore*weight/len(paragraph)

        # Regular topic proportions
        paraLength = len(row["rawParagraphs"][i])
        for index, weight in lda.get_document_topics(dct.doc2bow(paragraph)):
            topicAgg[index] += weight*paraLength/totalLength

        # Top topic sentiment

        # Top topic proportion
        topTopicLdaAgg[sorted(ldatopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1
        if len(nmftopics):  # Nmf can return no topics, thus check
            topTopicNmfAgg[sorted(nmftopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1

        # Document-level metrics
        docLevelNetToneScore += (posScore-negScore)/len(paragraph)
        docLevelUncertScore += uncertScore/len(paragraph)
        posnegcounter += posScore+negScore
        uncertcounter += uncertScore

    # COMPUTE FINAL DOCUMENT-LEVEL METRICS

    # Divide topTopic counts by the total number of paragraphs, blows up list comprehension for some reason
    for key, value in topTopicLdaAgg.items():
        if not sum(0 if val == "." else val for val in topTopicLdaAgg.values()):
            topTopicLdaAgg[key] = "."  # missing
        else:
            topTopicLdaAgg[key] = value/sum(0 if val == "." else val for val in topTopicLdaAgg.values())
    for key, value in topTopicNmfAgg.items():
        if not sum(0 if val == "." else val for val in topTopicNmfAgg.values()):
            topTopicNmfAgg[key] = "."  # missing
        else:
            topTopicNmfAgg[key] = value/sum(0 if val == "." else val for val in topTopicNmfAgg.values())

    netToneLda = {"ldaNetTone"+str(key+1): value for key, value in netToneScoreAggLda.items()}
    uncertLda = {"ldaUncert"+str(key+1): value for key, value in uncertScoreAggLda.items()}
    netToneNmf = {"nmfNetTone"+str(key+1): value for key, value in netToneScoreAggNmf.items()}
    uncertNmf = {"nmfUncert"+str(key+1): value for key, value in uncertScoreAggNmf.items()}
    topicProps = {"propTopic"+str(key+1): value for key, value in topicAgg.items()}
    topTopicPropLda = {"topTopicPropLda"+str(key+1): value for key, value in topTopicLdaAgg.items()}
    topTopicPropNmf = {"topTopicPropNmf"+str(key+1): value for key, value in topTopicNmfAgg.items()}
    minutesNew.append({**row, **netToneLda, **uncertLda, **netToneNmf, **uncertNmf,  **topicProps, **topTopicPropLda, **topTopicPropNmf,
                       "DL_nettone": docLevelNetToneScore, "DL_uncert": docLevelUncertScore,
                       "posnegcnt": posnegcounter, "uncertcnt": uncertcounter})


# Reduce size of dataset before exporting
for i, mins in enumerate(minutesNew):
    del mins["rawParagraphs"]
    del mins["filteredParagraphs"]
    minutesNew[i] = mins
# Dump dataset containing timeseries of textual analysis to csv for Stata
with open(os.path.join(os.path.dirname(__file__), "data", "dataExport.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minutesNew[0].keys())
    writer.writeheader()
    writer.writerows(minutesNew)

exit()


# Add topic proportions - quantitative topics
minutesNewNew = []
for doc in tqdm(minutesNew):
    topicAgg = {i: 0 for i in range(0, 8)}
    totalLength = sum([len(para) for para in doc["rawParagraphs"]])  # total length of entire document
    for i, para in enumerate(doc["filteredParagraphs"]):
        paraLength = len(doc["rawParagraphs"][i])
        # print(lda.get_document_topics(dct.doc2bow(para)))
        for index, weight in lda.get_document_topics(dct.doc2bow(para)):
            topicAgg[index] += weight*paraLength/totalLength
    topicProps = {"propTopic"+str(key+1): value for key, value in topicAgg.items()}
    minutesNewNew.append({**doc, **topicProps})


# Add top topic proportions - quantitative topics
# TODO Infuse topic props with sentiment score - qualitative topics
# Yes, it would be a lot more efficient if combined with the first for-loop, but I wouldn't understand anything two weeks down the road
minutesNewNewNew = []
for doc in tqdm(minutesNewNew):
    topTopicLdaAgg = {i: 0 for i in range(0, 8)}
    topTopicNmfAgg = {i: 0 for i in range(0, 8)}
    for i, para in enumerate(doc["filteredParagraphs"]):
        if not len(para):  # Skip if paragraph is empty, would crash the /len(paragraph) part without
            continue
        bow = dct.doc2bow(para)  # generate word vector / bag-of-words from tokenized paragraph
        ldatopics = lda.get_document_topics(bow, minimum_phi_value=0.01)  # Paramter necessary, bug in the library
        nmftopics = nmf.get_document_topics(bow)
        topTopicLdaAgg[sorted(ldatopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1
        if len(nmftopics):
            topTopicNmfAgg[sorted(nmftopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1
    # Divide topTopic counts by the total number of paragraphs, blows up list comprehension for some reason
    for key, value in topTopicLdaAgg.items():
        if not sum(0 if val == "." else val for val in topTopicLdaAgg.values()):
            topTopicLdaAgg[key] = "."  # missing
        else:
            topTopicLdaAgg[key] = value/sum(0 if val == "." else val for val in topTopicLdaAgg.values())
    for key, value in topTopicNmfAgg.items():
        if not sum(0 if val == "." else val for val in topTopicNmfAgg.values()):
            topTopicNmfAgg[key] = "."  # missing
        else:
            topTopicNmfAgg[key] = value/sum(0 if val == "." else val for val in topTopicNmfAgg.values())
    topTopicPropLda = {"topTopicPropLda"+str(key+1): value for key, value in topTopicLdaAgg.items()}
    topTopicPropNmf = {"topTopicPropNmf"+str(key+1): value for key, value in topTopicNmfAgg.items()}
    minutesNewNewNew.append({**doc, **topTopicPropLda, **topTopicPropNmf})
