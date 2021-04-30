import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle

filteredParagraphs = pickle.load(open("data/2filteredParagraphs", "rb"))
rawParagraphs = pickle.load(open("data/2rawParagraphs", "rb"))

# Flatten main list for word cloud
flattenedList = [token for paragraph in filteredParagraphs for token in paragraph]
wordcloud = WordCloud(background_color="white").generate(','.join(flattenedList))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Same for raw paragraphs as a comparison
flattenedList = [token for paragraph in rawParagraphs for token in paragraph]
wordcloud = WordCloud(background_color="white").generate(','.join(flattenedList))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# TODO Do some sort of table showing the most common words overall, most common negative and most common positive words
# similar to the table in Schmeling and Wagner
