# PURPOSE
# Apply LDA and NMF
# Use the paper where Hillert implemented it as a basis

# Use this article for both LDA and NNMF
# https://stackabuse.com/python-for-nlp-topic-modeling/#:~:text=Topic%20modeling%20is%20an%20unsupervised,clusters%20based%20on%20similar%20characteristics.

# For LDA, use parameter "number of topics" N = 1 to test for whole-document relevance

import os
from gensim.models import Phrases
import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm
import spacy
import requests
from wordcloud import WordCloud
nlp = spacy.load("en_core_web_lg")
nlp.max_length = 1500000  # Set up buffer length

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "1fomcLinks"), "rb"))
# minutes.reverse()  # DEBUG starting from 1993

# Container for filtered paragraphs (ie sets of filtered tokens)
# Document boundaries are irrelevant, because following Jegadeesh and Wu, object to
# model topic on is the paragraph and not the document.
# Differing fractions of paragraphs per document can be examiend over time, but that is
# more of a "derivative question" instead of the main focus.
filteredParagraphs = []
minutesNew = []
# rawParagraphs = []  # Tokenized paragraphs without lemmatizing and type filtering - robustness test

for row in tqdm(minutes):

    soup = BeautifulSoup(requests.get(row["link"]).content, "html.parser")
    text = soup.find("div", id="content") if soup.find("div", id="content") != None else soup.find("body")

    # Break document into paragraphs with min length 100 characters
    # text.split("\n") doesn't work, minutes before 2000 use \n for every linebreak even within paragraphs!
    paragraphsTemp = text.find_all("p")
    paragraphs = []
    for para in paragraphsTemp:
        if not len(para.find_all("p")) and len(para.get_text()) > 300:  # If no other p tags within the paragraph and min length
            paragraphs.append(para.get_text())

    documentLevelFilteredParagraphs = []
    for para in paragraphs:
        # Run standard spacy classification pipeline (tokenization, identification of word type etc)
        paraClassified = nlp(para)
        filteredTokens = []
        rawTokens = []
        for token in paraClassified:
            if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                filteredTokens.append(token.lemma_.lower())
            # rawTokens.append(token.lower())
        filteredParagraphs.append(filteredTokens)
        documentLevelFilteredParagraphs.append(filteredTokens)
        # rawParagraphs.append(rawTokens)
    minutesNew.append({**row, "filteredParagraphs": documentLevelFilteredParagraphs})

# Add bigrams to the filteredParagraphs list
# Actually not sure whether spacy does that out-of-the-box as well
bigram = Phrases(filteredParagraphs, min_count=20)
for i in range(len(filteredParagraphs)):
    for token in bigram[filteredParagraphs[i]]:  # gensim uses the entire lemmatized paragraph as an index in the bigram list object for some reason
        if "_" in token:  # Phrases object tacks bigrams onto the paragraph, so check through all to see whether there are any new ones
            filteredParagraphs[i].append(token)  # If bigram is found, append to old paragraph
# Has a minimum parameter, thus cannot work with the document-level version

# Preserve filtered paragraphs for further use
# pickle.dump(rawParagraphs, open("data/2rawParagraphs", "wb"))
pickle.dump(filteredParagraphs, open(os.path.join(os.path.dirname(__file__), "data", "2filteredParagraphs"), "wb"))
pickle.dump(minutesNew, open(os.path.join(os.path.dirname(__file__), "data", "2documentlevelFilteredParagraphs"), "wb"))  # Doesn't contain bigrams

# Done for now
# TODO optional: Fine tune bigram parameter
# TODO optional: admin section cutoff by occurence of word "vote"