import csv
import pickle
import os
minspickeled = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "2DLparagraphs"), "rb"))

with open(os.path.join(os.path.dirname(__file__), "data", "processedText.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, minspickeled[0].keys())
    writer.writeheader()
    writer.writerows(minspickeled)

minutesNew = []

for row in minspickeled:
    soup = BeautifulSoup(requests.get(row["link"]).content, "html.parser")
    text = soup.find("div", id="content") if soup.find("div", id="content") != None else soup.find("body")
    dissent = 0
    index = text.text.find("against this action:")+20
    assert index > 0, ("against this action: not found", row["link"])
    if "None" in text.text[index:index+10]:
        dissent = 1
    minutesNew.append({**row, "dissent": dissent})
