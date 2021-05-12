import pickle
import os.path
from tqdm import tqdm

#################################################
# Descriptive statistics for the data section
#################################################

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))

paraCount = sum([len(mins["filteredParagraphs"]) for mins in minutes])
wordCount = sum([len(para) for mins in minutes for para in mins["filteredParagraphs"]])

# statsData.append({"numParagraphs": len(mins["filteredParagraphs"])})


print("Number of documents", len(minutes))
print("Total number of paragraphs", paraCount)
print("Total number of words", wordCount)
print("Average number of paragraphs per document", round(paraCount/len(minutes)))
print("Average number of words per document", round(wordCount/len(minutes)))
