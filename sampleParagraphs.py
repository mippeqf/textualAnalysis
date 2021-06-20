import csv
import pickle
from posixpath import join
import pandas as pd
import gensim.utils
import os.path
from tqdm import tqdm
from envVars import NUM_TOPICS

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))

dct = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "dct"))
nmf = gensim.utils.SaveLoad.load(os.path.join(os.path.dirname(__file__), "models", "nmf"))

minutesNew = []

lmRAW = pd.read_csv(os.path.join(os.path.dirname(__file__), "statics", "LmDict.csv"))
lmPOS = set(lmRAW.query('Positive > 0')['Word'])
lmNEG = set(lmRAW.query('Negative > 0')['Word'])
lmUNCERT = set(lmRAW.query('Uncertainty > 0')['Word'])

minutes.reverse()
aggArr = [{i: {"weight": 0, "year": "0", "link": ".", "rawPara": "."} for i in range(0, NUM_TOPICS+1)} for i in range(0, 5)]
for row in tqdm(minutes):

    for i, paragraph in enumerate(row["filteredParagraphs"]):

        # Skip if paragraph is empty, would crash the /len(paragraph) part without
        if not len(paragraph):
            continue

        # Feed text into topic models
        bow = dct.doc2bow(paragraph)  # generate word vector / bag-of-words from tokenized paragraph
        nmftopics = nmf.get_document_topics(bow)

        # Top topic sentiment
        if len(nmftopics):  # Nmf can return no topics, thus check
            top = sorted(nmftopics, key=lambda tup: tup[1], reverse=True)
            for j, agg in enumerate(aggArr):
                if aggArr[j][top[0][0]]["weight"] < top[0][1]:
                    aggArr[j][top[0][0]]["weight"] = top[0][1]
                    aggArr[j][top[0][0]]["year"] = row["year"]
                    aggArr[j][top[0][0]]["link"] = row["link"]
                    aggArr[j][top[0][0]]["rawPara"] = row["filteredParagraphs"][i]
                    break


for i in range(0, NUM_TOPICS):
    print("\n")
    print("---------------------Topic", i, "\n")
    print("\n")
    for j in range(0, len(aggArr)):
        print(aggArr[j][i]["year"], aggArr[j][i]["weight"], aggArr[j][i]["link"])
        print(aggArr[j][i]["rawPara"])
        print("\n")
