import pickle
from tqdm import tqdm
import os.path

minutes = pickle.load(open(os.path.join(os.path.dirname(__file__), "data", "1fomcLinks"), "rb"))
for row in tqdm(minutes):
    print(row["link"])
