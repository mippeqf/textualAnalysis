import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim import models
import matplotlib.pyplot as plt
import spacy
from pprint import pprint
from wordcloud import WordCloud
nlp = spacy.load("en_core_web_lg")
nlp.max_length = 1500000  # Ensure sufficient memory

recentList = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
archiveList = "https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm"


FOMCMinutes = []  # A list of lists to form the corpus
FOMCWordCloud = []  # Single list version of the corpus for WordCloud
FOMCTopix = []  # List to store minutes ID (date) and weight of each para

# Define function to prepare corpus


def PrepareCorpus(urlpath, urlext, minslist, minparalength):

    fomcmins = []
    fomcwordcloud = []
    fomctopix = []

    for minutes in minslist:

        response = requests.get(f'https://www.federalreserve.gov/monetarypolicy/fomcminutes{date}.htm')  # Get the URL response
        soup = BeautifulSoup(response.content, 'lxml')  # Parse the response

        # Extract minutes content and convert to string
        minsTxt = str(soup.find("div", {"id": "content"}))  # Contained within the 'div' tag

        # Clean text - stage 1
        minsTxt = minsTxt.strip()  # Remove white space at the beginning and end
        minsTxt = minsTxt.replace('\r', '')  # Replace the \r with null
        minsTxt = minsTxt.replace('&nbsp;', ' ')  # Replace "&nbsp;" with space.
        minsTxt = minsTxt.replace('&#160;', ' ')  # Replace "&#160;" with space.
        while '  ' in minsTxt:
            minsTxt = minsTxt.replace('  ', ' ')  # Remove extra spaces

        # Clean text - stage 2, using regex (as SpaCy incorrectly parses certain HTML tags)
        minsTxt = re.sub(r'(<[^>]*>)|'  # Remove content within HTML tags
                         '([_]+)|'  # Remove series of underscores
                         '(http[^\s]+)|'  # Remove website addresses
                         '((a|p)\.m\.)',  # Remove "a.m" and "p.m."
                         '', minsTxt)  # Replace with null

        # Find length of minutes document for calculating paragraph weights
        minsTxtParas = minsTxt.split('\n')  # List of paras in minsTxt, where minsTxt is split based on new line characters
        cum_paras = 0  # Set up variable for cumulative word-count in all paras for a given minutes document
        for para in minsTxtParas:
            if len(para) > minparalength:  # Only including paragraphs larger than 'minparalength'
                cum_paras += len(para)

        # Extract paragraphs
        for para in minsTxtParas:
            if len(para) > minparalength:  # Only extract paragraphs larger than 'minparalength'

                topixTmp = []  # Temporary list to store minutes date & para weight tuple
                topixTmp.append(minutes)  # First element of tuple (minutes date)
                topixTmp.append(len(para)/cum_paras)  # Second element of tuple (para weight), NB. Calculating weights based on pre-SpaCy-parsed text

                # Parse cleaned para with SpaCy
                minsPara = nlp(para)

                minsTmp = []  # Temporary list to store individual tokens

                # Further cleaning and selection of text characteristics
                for token in minsPara:
                    # Retain words that are not a stop word nor punctuation, and only if a Noun, Adjective or Verb
                    if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                        minsTmp.append(token.lemma_.lower())  # Convert to lower case and retain the lemmatized version of the word (this is a string object)
                        fomcwordcloud.append(token.lemma_.lower())  # Add word to WordCloud list
                fomcmins.append(minsTmp)  # Add para to corpus 'list of lists'
                fomctopix.append(topixTmp)  # Add minutes date & para weight tuple to list for storing

    return fomcmins, fomcwordcloud, fomctopix


# Prepare corpus
FOMCMinutes, FOMCWordCloud, FOMCTopix = PrepareCorpus(urlpath=URLPath, urlext=URLExt, minslist=MinutesList, minparalength=200)

# Generate and plot WordCloud for full corpus
wordcloud = WordCloud(background_color="white").generate(','.join(FOMCWordCloud))  # NB. 'join' method used to convert the list to text format
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Form dictionary by mapping word IDs to words
ID2word = corpora.Dictionary(FOMCMinutes)
# Set up Bag of Words and TFIDF
corpus = [ID2word.doc2bow(doc) for doc in FOMCMinutes]  # Apply Bag of Words to all documents in corpus
TFIDF = models.TfidfModel(corpus)  # Fit TF-IDF model
trans_TFIDF = TFIDF[corpus]  # Apply TF-IDF model

SEED = 130  # Set random seed
NUM_topics = 8  # Set number of topics
ALPHA = 0.15  # Set alpha
ETA = 1.25  # Set eta
# Train LDA model using the corpus
lda_model = gensim.models.LdaMulticore(corpus=trans_TFIDF, num_topics=NUM_topics, id2word=ID2word, random_state=SEED, alpha=ALPHA, eta=ETA, passes=100)

# Set up coherence model
coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=FOMCMinutes, dictionary=ID2word, coherence='c_v')
# Calculate coherence
coherence_lda = coherence_model_lda.get_coherence()

# Coherence values for varying alpha


def compute_coherence_values_ALPHA(corpus, dictionary, num_topics, seed, eta, texts, start, limit, step):
    coherence_values = []
    model_list = []
    for alpha in range(start, limit, step):
        model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=seed, eta=eta, alpha=alpha/20, passes=100)
        model_list.append(model)
        coherencemodel = gensim.models.CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values


model_list, coherence_values = compute_coherence_values_ALPHA(dictionary=ID2word, corpus=trans_TFIDF, num_topics=NUM_topics, seed=SEED, eta=ETA, texts=FOMCMinutes, start=1, limit=20, step=1)

# Plot graph of coherence values by varying alpha
limit = 20
start = 1
step = 1
x_axis = []
for x in range(start, limit, step):
    x_axis.append(x/20)
plt.plot(x_axis, coherence_values)
plt.xlabel("Alpha")
plt.ylabel("Coherence score")
plt.legend(("coherence"), loc='best')
plt.show()

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
