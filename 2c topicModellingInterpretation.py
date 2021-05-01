import logging
import pickle

from gensim.models import LdaModel

# Set up logging
# Print topics prints to INFO level - won't work without logging enabled!!
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lda = LdaModel.load("data/lda.model")
lda.print_topics(5, 10)

# TODO Several useful descriptive insight methods in this article
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#15visualizethetopicskeywords
# https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/#14.-pyLDAVis

#####################################################################################
# Interpretation of topic mix
#####################################################################################
# Computes the share of topics in every minutes document over time
# TODO One of the key descripte statistics before correlating with market returns!!
# Also does word clouds for every relevant topic, might also be an idea
# TODO Perhaps just list the most common words and their respective prevalence/weight as a table though

# Generate weighted topic proportions across all paragraphs in the corpus
para_no = 0  # Set document counter
for para in FOMCTopix:
    TFIDF_para = TFIDF[corpus[para_no]]  # Apply TFIDF model to individual minutes documents
    # Generate and store weighted topic mix for each para
    for topic_weight in lda_model.get_document_topics(TFIDF_para):  # List of tuples ("topic number", "topic proportion") for each para, where 'topic_weight' is the (iterating) tuple
        FOMCTopix[para_no].append(FOMCTopix[para_no][1]*topic_weight[1])  # Weights are the second element of the pre-appended list, topic proportions are the second element of each tuple
    para_no += 1

# Generate aggregate topic mix for each minutes transcript
# Form dataframe of weighted topic proportions (paragraphs) - include any chosen topic names
FOMCTopixDF = pd.DataFrame(FOMCTopix, columns=['Date', 'Weight', 'Inflation', 'Topic 2', 'Consumption', 'Topic 4', 'Market', 'Topic 6', 'Topic 7', 'Policy'])

# Aggregate topic mix by minutes documents (weighted sum of paragraphs)
TopixAggDF = pd.pivot_table(FOMCTopixDF, values=['Inflation', 'Topic 2', 'Consumption', 'Topic 4', 'Market', 'Topic 6', 'Topic 7', 'Policy'], index='Date', aggfunc=np.sum)

topic = 0  # Initialize counter
while topic < NUM_topics:
    # Get topics and frequencies and store in a dictionary structure
    topic_words_freq = dict(lda_model.show_topic(topic, topn=50))
    topic += 1

    # Generate Word Cloud for topic using frequencies
    wordcloud = WordCloud(background_color="white").generate_from_frequencies(topic_words_freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Plot results - select which topics to print
TopixAggDF.plot(y=['Inflation', 'Consumption', 'Market', 'Policy'], kind='line', use_index=True)
