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
# Needed for model training and word clouds. Structurally not necessary, can be derived from the DL array at any time
# filteredParagraphs = []
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

    DLfilteredparagraphs = []
    DLrawparagraphs = []
    for para in paragraphs:
        # Run standard spacy classification pipeline (tokenization, identification of word type etc)
        paraClassified = nlp(para)
        filteredTokens = []
        rawTokens = []
        for token in paraClassified:
            if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                filteredTokens.append(token.lemma_.lower())
            rawTokens.append(token.lower_)
        # filteredParagraphs.append(filteredTokens)
        DLfilteredparagraphs.append(filteredTokens)
        DLrawparagraphs.append(rawTokens)  # only tokenized and decapitalised, no type filtering
    minutesNew.append({**row, "filteredParagraphs": DLfilteredparagraphs, "rawParagraphs": DLrawparagraphs})

# TODO Implement bigrams and trigrams!
# Add bigrams to the filteredParagraphs list, spacy has an implementation called noun chunks
if False:
    bigram = Phrases(filteredParagraphs, min_count=20)
    for i in range(len(filteredParagraphs)):
        for token in bigram[filteredParagraphs[i]]:  # gensim uses the entire lemmatized paragraph as an index in the bigram list object for some reason
            if "_" in token:  # Phrases object tacks bigrams onto the paragraph, so check through all to see whether there are any new ones
                filteredParagraphs[i].append(token)  # If bigram is found, append to old paragraph

# Preserve filtered paragraphs for further use
# pickle.dump(rawParagraphs, open("data/2rawParagraphs", "wb")) # Depercated
# pickle.dump(filteredParagraphs, open(os.path.join(os.path.dirname(__file__), "data", "2filteredParagraphs"), "wb")) # Depercated
pickle.dump(minutesNew, open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "wb"))  # Doesn't contain bigrams

# Done for now
# TODO optional: Fine tune bigram parameter
# TODO optional: admin section cutoff by occurence of word "vote"
