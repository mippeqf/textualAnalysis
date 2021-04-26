import json
import matplotlib.pyplot as plt
import numpy as np

with open('data/listfile.txt', 'r') as filehandle:
    percentages = json.load(filehandle)
    plt.hist(percentages, bins=np.arange(0, 1, 0.01))
    plt.show()
