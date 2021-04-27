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

import pysentiment2 as ps
import json
from bs4 import BeautifulSoup
import requests
import csv
import pickle

minutes = pickle.load(open("data/1fomcLinks", "rb"))
# Minutes are a list of dictionaries with fields year, meeting, link, type, paragraphs!
hiv4 = ps.HIV4()
lm = ps.LM()

minutesNew = []

for i, row in enumerate(minutes):
    if not "minutes" in row["link"].lower() or not row["type"] == "htm":
        continue
    soup = BeautifulSoup(requests.get("https://www.federalreserve.gov"+row["link"]).content, "html.parser")
    text = soup.find("div", id="content").get_text() if soup.find("div", id="content") != None else soup.find("body").get_text()

    # 0 GENERAL CLEANING (not in JeWu)
    text = text.strip()  # Remove white space at the beginning and end
    text = text.replace('\r', '')  # Replace the \r with null
    text = text.replace('&nbsp;', ' ')  # Replace "&nbsp;" with space.
    text = text.replace('&#160;', ' ')  # Replace "&#160;" with space.
    while '  ' in text:
        text = text.replace('  ', ' ')  # Remove extra spaces

    tokens = hiv4.tokenize(text)  # text can be tokenized by other ways however, dict in HIV4 is preprocessed by the default tokenizer in the library
    hiv4score = hiv4.get_score(tokens)
    tokens = lm.tokenize(text)
    lmscore = lm.get_score(tokens)
    minutesNew.append({**row, "hvPos": hiv4score["Positive"], "hvNeg": hiv4score["Negative"], "hvPol": hiv4score["Polarity"], "hvSub": hiv4score["Subjectivity"],
                      "lmPos": lmscore["Positive"], "lmNeg": lmscore["Negative"], "lmPol": lmscore["Polarity"], "lmSub": lmscore["Subjectivity"], })
    print(i, "of", len(minutes), row["year"], " Harvard score: ", hiv4score, " LM score: ", lmscore)

pickle.dump(minutesNew, open("data/3toneAnalysisDump", "wb"))
