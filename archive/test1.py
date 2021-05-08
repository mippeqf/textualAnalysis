import csv
import pickle
import os
minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))

with open(os.path.join(os.path.dirname(__file__), "data", "processedText.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minspickeled[0].keys())
    writer.writeheader()
    writer.writerows(minspickeled)
