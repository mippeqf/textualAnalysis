import pickle
import csv

data = pickle.load(open("data/3toneAnalysisDump", "rb"))
# for i, row in enumerate(data):
#     if i > 10:
#         break
#     print(row)

with open("data/dataExport.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, data[0].keys())
    writer.writeheader()
    writer.writerows(data)
