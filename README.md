# Textual Analysis

## Abstract/Introduction

Start with Baker Wurgler, short overview over the sentiment literature
Examining news releases is particularly interesting because ...
Summarize every one of the following section in a short paragraph
Clearly state how this thesis might contribute to the literature

## 1 Data

### 1.1 Auxiliary data (LM dictionary, market)

Downloaded from …
Market data is from yahoo finance

### 1.2 Preparation of textual data

spacy

### 1.3 Descriptives

Random minutes paragraph a. before processing b. after tokenization and lemmatization c. after vectorization. Keep this one short!

## 2 Methodology: Tone computation and topic modelling

### 2.1 Tone computation

Short description of dictionary-lookup process and

### 2.2 LDA setup

Roughly summarize section 3.2 of JeWu, for intuition have another look at the youtube video by the Italian.

### 2.3 LDA vs NMF

Not sure yet on the performance metric, running all results with both methods seems a little over the top, coherence score might be a good ex-ante proxy.

### 2.4 Descriptives

Intertemporal progression of topic shares per document - based on document-level net-score measure

## 3 Empirical results

### 3.1 Minutes and the Market (contemporaneous correlations)

Linking tone (and derivatives like tone change etc) to market
Linking uncertainty to market

### 3.2 Predicting market with Twitter

Loosely following Azar 2016

### 3.3 Predicting tone with Twitter

My unique contribution, might have mildly interesting implications in combination with prior two results.

## 4 Implications/Interpretation/Dicussion

Assuming negligible sentiment leakage from the Fed and, if Twitter can predict FOMC tone, the FOMC merely aggregates public sentiment. (Even if Twitter merely predicts a third factor which causes FOMC sentiment, that - under the no-leakage assumption - will be in the public realm as well). Thus, this association determines the "uniquness" of the FOMC's tone.

## 5 Robustness checks

Concern by Schmeling/Wagner about lookahead bias if topic model is trained with whole-period data. Would make sense if I were to predict topic proportions or the like but is that really also the case when predicting market returns?

Perhaps move ADL vs NMF here?

## 6 Conclusion

tbd
