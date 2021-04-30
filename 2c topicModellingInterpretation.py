import logging
import pickle

from gensim.models import LdaModel

# Set up logging
# Print topics prints to INFO level - won't work without logging enabled!!
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lda = LdaModel.load("data/lda.model")
lda.print_topics(5, 10)

# Use pyLDAvis
# Look at this article https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/#14.-pyLDAVis
