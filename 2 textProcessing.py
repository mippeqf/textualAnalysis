# PURPOSE
# Apply LDA and NMF
# Use the paper where Hillert implemented it as a basis

# Use this article for both LDA and NNMF
# https://stackabuse.com/python-for-nlp-topic-modeling/#:~:text=Topic%20modeling%20is%20an%20unsupervised,clusters%20based%20on%20similar%20characteristics.

# For LDA, use parameter "number of topics" N = 1 to test for whole-document relevance

import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm
import spacy
import requests
from wordcloud import WordCloud
nlp = spacy.load("en_core_web_lg")
nlp.max_length = 1500000  # Set up buffer length

minutes = pickle.load(open("data/1fomcLinks", "rb"))

# Container for filtered paragraphs (ie sets of filtered tokens)
# Document boundaries are irrelevant, because following Jegadeesh and Wu, object to
# model topic on is the paragraph and not the document.
# Differing fractions of paragraphs per document can be examiend over time, but that is
# more of a "derivative question" instead of the main focus.
filteredParagraphs = []
minutesNew = []
rawParagraphs = []  # Tokenized paragraphs without filtering - robustness test

for row in tqdm(minutes):

    soup = BeautifulSoup(requests.get(row["link"]).content, "html.parser")
    text = soup.find("div", id="content").get_text() if soup.find("div", id="content") != None else soup.find("body").get_text()

    # Break document into paragraphs with min length 100 characters
    paragraphsTemp = text.split("\n")
    paragraphs = []
    for para in paragraphsTemp:
        if len(para) > 300:
            paragraphs.append(para)

    documentLevelFilteredParagraphs = []
    for para in paragraphs:
        # Run standard spacy classification pipeline (tokenization, identification of word type etc)
        paraClassified = nlp(para)
        filteredTokens = []
        for token in paraClassified:
            if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                filteredTokens.append(token.lemma_.lower())
            rawParagraphs.append(token)
        filteredParagraphs.append(filteredTokens)
        documentLevelFilteredParagraphs.append(filteredTokens)
    minutesNew.append({**row, "filteredParagraphs": documentLevelFilteredParagraphs})

# Preserve filtered paragraphs for further use
pickle.dump(rawParagraphs, open("data/2rawParagraphs", "wb"))
pickle.dump(filteredParagraphs, open("data/2filteredParagraphs", "wb"))
pickle.dump(minutesNew, open("data/2documentlevelFilteredParagraphs", "wb"))
