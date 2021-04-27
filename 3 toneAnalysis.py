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

minutes = json.load(open("data/2 minutesProcessed.txt", "r"))
# Minutes are a list of dictionaries with fields year, meeting, link, type, paragraphs!
hiv4 = ps.HIV4()

for doc in minutes:
    tokens = hiv4.tokenize(minutes)  # text can be tokenized by other ways however, dict in HIV4 is preprocessed by the default tokenizer in the library
    score = hiv4.get_score(tokens)

lm = ps.LM()
tokens = lm.tokenize(text)
score = lm.get_score(tokens)
