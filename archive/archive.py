# Add topic proportions - quantitative topics
minutesNewNew = []
for doc in tqdm(minutesNew):
    topicAgg = {i: 0 for i in range(0, 8)}
    docLength = sum([len(para) for para in doc["rawParagraphs"]])  # total length of entire document
    for i, para in enumerate(doc["filteredParagraphs"]):
        paraLength = len(doc["rawParagraphs"][i])
        # print(lda.get_document_topics(dct.doc2bow(para)))
        for index, weight in lda.get_document_topics(dct.doc2bow(para)):
            topicAgg[index] += weight*paraLength/docLength
    topicProps = {"propTopic"+str(key+1): value for key, value in topicAgg.items()}
    minutesNewNew.append({**doc, **topicProps})


# Add top topic proportions - quantitative topics
# TODO Infuse topic props with sentiment score - qualitative topics
# Yes, it would be a lot more efficient if combined with the first for-loop, but I wouldn't understand anything two weeks down the road
minutesNewNewNew = []
for doc in tqdm(minutesNewNew):
    topTopicLdaAgg = {i: 0 for i in range(0, 8)}
    topTopicNmfAgg = {i: 0 for i in range(0, 8)}
    for i, para in enumerate(doc["filteredParagraphs"]):
        if not len(para):  # Skip if paragraph is empty, would crash the /len(paragraph) part without
            continue
        bow = dct.doc2bow(para)  # generate word vector / bag-of-words from tokenized paragraph
        ldatopics = lda.get_document_topics(bow, minimum_phi_value=0.01)  # Paramter necessary, bug in the library
        nmftopics = nmf.get_document_topics(bow)
        topTopicLdaAgg[sorted(ldatopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1
        if len(nmftopics):
            topTopicNmfAgg[sorted(nmftopics, key=lambda tup: tup[1], reverse=True)[0][0]] += 1
    # Divide topTopic counts by the total number of paragraphs, blows up list comprehension for some reason
    for key, value in topTopicLdaAgg.items():
        if not sum(0 if val == "." else val for val in topTopicLdaAgg.values()):
            topTopicLdaAgg[key] = "."  # missing
        else:
            topTopicLdaAgg[key] = value/sum(0 if val == "." else val for val in topTopicLdaAgg.values())
    for key, value in topTopicNmfAgg.items():
        if not sum(0 if val == "." else val for val in topTopicNmfAgg.values()):
            topTopicNmfAgg[key] = "."  # missing
        else:
            topTopicNmfAgg[key] = value/sum(0 if val == "." else val for val in topTopicNmfAgg.values())
    topTopicPropLda = {"topTopicPropLda"+str(key+1): value for key, value in topTopicLdaAgg.items()}
    topTopicPropNmf = {"topTopicPropNmf"+str(key+1): value for key, value in topTopicNmfAgg.items()}
    minutesNewNewNew.append({**doc, **topTopicPropLda, **topTopicPropNmf})
