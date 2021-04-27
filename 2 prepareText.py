import csv
import re
import json
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# PURPOSE
# Second paragraph of seciton 2.2 in JeWu
# The TDS tutorial actually does a good bit more, leave that out for now and focus only on JeWu

# TODO
# 1. Remove admin sections according to JeWu section 2.2
# Rule that seems to work is to cut off after the last paragraph containin the word "vote"
# that is not in the last 5% of the document.
# 2. Break the document into individual paragraphs
# 3. Record the specific sections where each paragraph is located - WHY?
# 4. Obtain paragraph length, ie number of words


minutes = json.load(open("data/1 fomcLinks.txt", "r"))

for row in tqdm(minutes):
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

    minutes.append({**row, "text": text})

    continue

    # Don't split paragraphs, whole text needed for LM approach
    # Downloading text might also not be a good idea

    # 2 Break document into paragraphs with min length 100 characters
    paragraphs = text.split("\n")
    for i, par in enumerate(paragraphs):
        if len(par) < 100:
            paragraphs.pop(i)

    minutes.append({**row, "paragraphs": paragraphs})

    # 1 Remove admin section - TODO
    # Based on a histogram of where the word "vote" is located in the document,
    # a cutoff point of 0.6 is chosen
    # print(row["year"], end=": ")
    # for i, par in enumerate(paragraphs):
    #     if par.find("vote") != -1:
    #         print(round(i/len(paragraphs)*100), "% ", end="")
    # print()

json.dump(minutes, open("data/2 minutesProcessed.txt", "w", encoding="UTF-8"))
