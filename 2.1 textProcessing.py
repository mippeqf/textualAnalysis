import os
import pickle
import csv
import re

import requests
import spacy
from bs4 import BeautifulSoup
from gensim.models import Phrases
from tqdm import tqdm
from wordcloud import WordCloud

nlp = spacy.load("en_core_web_lg")
nlp.max_length = 1500000  # Set up buffer length

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "1fomcLinks"), "rb"))
# minutes.reverse()  # DEBUG starting from 1993

minutesNew = []

for row in tqdm(minutes):
    # if row["link"] != "https://www.federalreserve.gov/monetarypolicy/fomcminutes20091104.htm":
    #     continue
    soup = BeautifulSoup(requests.get(row["link"]).content, "html.parser")
    body = str(soup)
    text = soup.find("div", id="content") if soup.find("div", id="content") != None else soup.find("body")

    # Break document into paragraphs with min length 100 characters
    # text.split("\n") doesn't work, minutes before 2000 use \n for every linebreak even within paragraphs!
    # Straightforward solution: Get textContent of <p> tags
    # Major problem: Using Html closing tags apparently ran counter to Greenspan era policy, so using the above rule
    # yields no text in many instances from around 1997 to 2003.
    # Solution: check whether there are any closing tags at all and apply different splitting method if so.
    paragraphstmp = []
    paragraphs = []
    if body.count("</p></p></p>"):  # bs4 adds closing tags
        paragraphstmp = body.split("<p>")  # Split the document on opening p tags
        paragraphstmp.pop(0)  # Remove the first section before the first p tag
        for para in paragraphstmp:
            par = re.sub('<[^>]*>', '', para)
            par = re.sub("(\r\n|\n|\r|\t)", " ", par)
            par = re.sub("  ", " ", par)
            par.strip()
            if len(par) > 300:
                paragraphs.append(par)
    else:
        paragraphstmp = text.find_all("p")
        for para in paragraphstmp:
            if not len(para.find_all("p")) and len(para.text) > 300:  # Assure that there's no nested paragraph and min length
                paragraphs.append(para.text)

    DLfilteredparagraphs = []
    DLrawparagraphs = []
    for para in tqdm(paragraphs, leave=False):
        # Run standard spacy classification pipeline (tokenization, identification of word type etc)
        paraClassified = nlp(para)
        filteredTokens = []
        rawTokens = []
        for token in paraClassified:
            if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                filteredTokens.append(token.lemma_.lower())
            rawTokens.append(token.lower_)
        DLfilteredparagraphs.append(filteredTokens)
        DLrawparagraphs.append(rawTokens)  # only tokenized and decapitalised, no type filtering
    minutesNew.append({**row, "filteredParagraphs": DLfilteredparagraphs, "rawParagraphs": DLrawparagraphs})

# Add dissent variable
minutesNewnew = []
for row in minutesNew:
    soup = BeautifulSoup(requests.get(row["link"]).content, "html.parser")
    text = soup.find("div", id="content") if soup.find("div", id="content") != None else soup.find("body")
    dissent = 0
    index = text.text.find("against this action:")+20
    assert index > 0, ("against this action: not found", row["link"])
    if "None" in text.text[index:index+10]:
        dissent = 1
    minutesNewnew.append({**row, "dissent": dissent})

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
pickle.dump(minutesNewnew, open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "wb"))  # Doesn't contain bigrams

# Done for now
# TODO optional: Fine tune bigram parameter
# TODO optional: admin section cutoff by occurence of word "vote"

with open(os.path.join(os.path.dirname(__file__), "data", "processedText.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minutesNewnew[0].keys())
    writer.writeheader()
    writer.writerows(minutesNewnew)
