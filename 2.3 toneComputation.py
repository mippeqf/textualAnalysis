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

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2documentlevelfilteredParagraphs"), "rb"))
# Minutes are a list of dictionaries with fields year, meeting, link, and list of lists containing preprocessed paragraphs

dct = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "dct"))
lda = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "lda"))
nmf = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "nmf"))

minutesNew = []

lmRAW = pd.read_csv(os.path.join(os.path.dirname(__file__), "statics", "LmDict.csv"))
lmPOS = set(lmRAW.query('Positive > 0')['Word'])
lmNEG = set(lmRAW.query('Negative > 0')['Word'])
lmUNCERT = set(lmRAW.query('Uncertainty > 0')['Word'])

####################################################
# Document-level tone computation
####################################################
minutes.reverse()
for i, row in enumerate(minutes):

    netToneScoreAggLda = {i: 0 for i in range(0, 8)}
    uncertScoreAggLda = {i: 0 for i in range(0, 8)}
    netToneScoreAggNmf = {i: 0 for i in range(0, 8)}
    uncertScoreAggNmf = {i: 0 for i in range(0, 8)}
    docLevelNetToneScore = 0
    docLevelUncertScore = 0
    for paragraph in row["filteredParagraphs"]:
        if not len(paragraph):  # Skip if paragraph is empty, would crash the /len(paragraph) part without
            continue
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
        # Compute final metrics
        for index, weight in ldatopics:  # Iterate through Lda topics
            # EQUATION 6 IN JEWU (PAGE 17)
            netToneScoreAggLda[index] += (posScore-negScore)*weight/len(paragraph)
            uncertScoreAggLda[index] += uncertScore*weight/len(paragraph)
        for index, weight in nmftopics:  # Iterate through Nmf topics
            netToneScoreAggNmf[index] += (posScore-negScore)*weight/len(paragraph)
            uncertScoreAggNmf[index] += uncertScore*weight/len(paragraph)
        docLevelNetToneScore += (posScore-negScore)/len(paragraph)
        docLevelUncertScore += uncertScore/len(paragraph)
        posnegcounter = posScore+negScore
        uncertcounter = uncertScore

    netToneLda = {"ldaNetTone"+str(key+1): value for key, value in netToneScoreAggLda.items()}
    uncertLda = {"ldaUncert"+str(key+1): value for key, value in uncertScoreAggLda.items()}
    netToneNmf = {"nmfNetTone"+str(key+1): value for key, value in netToneScoreAggNmf.items()}
    uncertNmf = {"nmfUncert"+str(key+1): value for key, value in uncertScoreAggNmf.items()}
    minutesNew.append({**row, **netToneLda, **uncertLda, **netToneNmf, **uncertNmf, "DL_nettone": docLevelNetToneScore,
                       "DL_uncert": docLevelUncertScore, "posnegcnt": posnegcounter, "uncertcnt": uncertcounter})
    # print(i, "of", len(minutes), row["year"])

# Dump dataset containing timeseries of textual analysis to csv for Stata
with open(os.path.join(os.path.dirname(__file__), "data", "dataExport.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minutesNew[0].keys())
    writer.writeheader()
    writer.writerows(minutesNew)
