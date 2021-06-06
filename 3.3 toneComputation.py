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
from envVars import NUM_TOPICS

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))
# Minutes are a list of dictionaries with fields year, meeting, link, and list of lists containing preprocessed paragraphs

dct = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "dct"))
nmf = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "nmf"))

minutesNew = []

lmRAW = pd.read_csv(os.path.join(os.path.dirname(__file__), "statics", "LmDict.csv"))
lmPOS = set(lmRAW.query('Positive > 0')['Word'])
lmNEG = set(lmRAW.query('Negative > 0')['Word'])
lmUNCERT = set(lmRAW.query('Uncertainty > 0')['Word'])

# NUM_TOPICS = 10

# Compute document-level tone/uncert and topic-specific scores - qualitative topics
minutes.reverse()
for row in tqdm(minutes):

    netToneScoreAggNmf = {i: 0 for i in range(0, NUM_TOPICS)}
    uncertScoreAggNmf = {i: 0 for i in range(0, NUM_TOPICS)}
    negScoreAggNmf = {i: 0 for i in range(0, NUM_TOPICS)}
    topTopicPropNmfAgg = {i: 0 for i in range(0, NUM_TOPICS)}
    topTopicSentNmfAgg = {i: 0 for i in range(0, NUM_TOPICS)}
    nmfTopicPropAgg = {i: 0 for i in range(0, NUM_TOPICS)}
    docLength = sum([len(para) for para in row["filteredParagraphs"]])  # total length of entire document
    docLevelNetToneScore = 0
    docLevelUncertScore = 0
    docLevelNegScore = 0
    poscounter = 0
    negcounter = 0
    uncertcounter = 0

    for paragraph in row["filteredParagraphs"]:

        # Skip if paragraph is empty, would crash the /len(paragraph) part without
        if not len(paragraph):
            continue

        # Feed text into topic models
        bow = dct.doc2bow(paragraph)  # generate word vector / bag-of-words from tokenized paragraph
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

        # Compute proportion of current paragraph to entire document
        paraLength = len(paragraph)
        paraProp = paraLength/docLength

        # COMPUTE PARAGRAPH-LEVEL METRICS AND ADD TO AGGREGATORS

        # Regular topic sentiment (net tone and uncertainty) (regular means "use all topic weights, not just #1")
        for index, weight in nmftopics:  # Iterate through Nmf topics
            netToneScoreAggNmf[index] += (posScore-negScore)*weight*paraProp
            uncertScoreAggNmf[index] += uncertScore*weight*paraProp
            negScoreAggNmf[index] += negScore*weight*paraProp

        # Regular topic proportions
        for index, weight in nmf.get_document_topics(dct.doc2bow(paragraph)):
            nmfTopicPropAgg[index] += weight*paraProp

        # Top topic sentiment
        if len(nmftopics):  # Nmf can return no topics, thus check
            topTopicSentNmfAgg[sorted(nmftopics, key=lambda tup: tup[1], reverse=True)[0][0]] += (posScore-negScore)*paraProp

        # Top topic proportion
        if len(nmftopics):  # Nmf can return no topics, thus check
            topTopicPropNmfAgg[sorted(nmftopics, key=lambda tup: tup[1], reverse=True)[0][0]] += paraProp

        # Document-level metrics
        docLevelNetToneScore += (posScore-negScore)*paraProp
        docLevelUncertScore += uncertScore*paraProp
        docLevelNegScore += negScore
        poscounter += posScore
        negcounter += negScore
        uncertcounter += uncertScore

    # COMPUTE FINAL DOCUMENT-LEVEL METRICS

    # Divide topTopic counts by the total number of paragraphs, blows up list comprehension for some reason
    for key, value in topTopicPropNmfAgg.items():
        if not sum(0 if val == "." else val for val in topTopicPropNmfAgg.values()):
            topTopicPropNmfAgg[key] = "."  # missing
        else:
            topTopicPropNmfAgg[key] = value/sum(0 if val == "." else val for val in topTopicPropNmfAgg.values())

    netToneNmf = {"nmfNetTone"+str(key+1): value for key, value in netToneScoreAggNmf.items()}
    uncertNmf = {"nmfUncert"+str(key+1): value for key, value in uncertScoreAggNmf.items()}
    negNmf = {"nmfneg"+str(key+1): value for key, value in negScoreAggNmf.items()}
    propNmf = {"nmfProp"+str(key+1): value for key, value in nmfTopicPropAgg.items()}
    # topTopicPropLda = {"topTopicPropLda"+str(key+1): value for key, value in topTopicPropLdaAgg.items()}
    # topTopicPropNmf = {"topTopicPropNmf"+str(key+1): value for key, value in topTopicPropNmfAgg.items()}
    # topTopicSentLda = {"topTopicSentLda"+str(key+1): value for key, value in topTopicSentLdaAgg.items()}
    # topTopicSentNmf = {"topTopicSentNmf"+str(key+1): value for key, value in topTopicSentNmfAgg.items()}
    minutesNew.append({**row, **netToneNmf, **uncertNmf,  **negNmf, **propNmf,
                       #    **topTopicPropLda, **topTopicPropNmf, **topTopicSentLda, **topTopicSentNmf,
                       "DL_nettone": docLevelNetToneScore, "DL_uncert": docLevelUncertScore, "DL_neg": docLevelNegScore,
                       "poscnt": poscounter, "negcnt": negcounter, "uncertcnt": uncertcounter})

# Append some basic word and paragraph count variables
minutesNewnew = []
for row in minutesNew:
    paraCnt = len(row["filteredParagraphs"])
    # paraCntRaw = len([para for para in row["rawParagraphs"] if para]) # paraCntRaw is the same as filtered because empty paragraph were kicked already
    wordCntFiltered = sum([len(para) for para in row["filteredParagraphs"]])
    wordCntRaw = sum([len(para) for para in row["rawParagraphs"]])
    minutesNewnew.append({**row, "wordCntFiltered": wordCntFiltered, "wordCntRaw": wordCntRaw, "paraCnt": paraCnt})

# Reduce size of dataset before exporting
for i, mins in enumerate(minutesNewnew):
    del mins["rawParagraphs"]
    del mins["filteredParagraphs"]
    minutesNewnew[i] = mins
# Dump dataset containing timeseries of textual analysis to csv for Stata
with open(os.path.join(os.path.dirname(__file__), "data", "dataExport.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minutesNewnew[0].keys())
    writer.writeheader()
    writer.writerows(minutesNewnew)
pickle.dump(minutesNewnew, open(os.path.join(os.path.dirname(__file__), "data", "dataExport"), "wb"))  # Doesn't contain bigrams

# Print out a few word/paragraph count statistics for the entire dataset
paraCount = sum([len(mins["filteredParagraphs"]) for mins in minutes])
wordCount = sum([len(para) for mins in minutes for para in mins["filteredParagraphs"]])
print("Number of documents", len(minutes))
print("Total number of paragraphs", paraCount)
print("Total number of words", wordCount)
print("Average number of paragraphs per document", round(paraCount/len(minutes)))
print("Average number of words per document", round(wordCount/len(minutes)))
