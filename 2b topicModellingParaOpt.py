#####################################################################################
# Parameter optimization - alpha
#####################################################################################

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


# Essentially just retrains the model with a range of different alpha values
# Multivariate optimization including the other parameters would be cool, but out of scope!
