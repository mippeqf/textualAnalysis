import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle

filteredParagraphs = pickle.load(open(""))

# Flatten main list for word cloud
flattenedList = [token for paragraph in filteredParagraphs for token in paragraph]
wordcloud = WordCloud(background_color="white").generate(','.join(flattenedList))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
