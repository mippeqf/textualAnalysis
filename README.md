# Textual Analysis

## Abstract/Introduction

Start with Baker Wurgler, short overview over the sentiment literature
Examining news releases is particularly interesting because ...
Summarize every one of the following section in a short paragraph
Clearly state how this thesis might contribute to the literature

## 1 Data

### 1.1 Data sources (LM dictionary, market, minutes)

Downloaded from …
Market data is from yahoo finance
Details on characteristics of fomc minutes, only available in today's format since 1993. Include that one graphic from the fed publication here.

I do not merge HV and LM dictionary. Although there seems to be somewhat of a drought around the year 2000 in term occurence, merging the Harvard lexicon onto LM would defeat the entire purpose of the LM dictionary.

### 1.2 Preparation of textual data

spacy

### 1.3 Descriptives

- Random minutes paragraph a. before processing b. after tokenization and lemmatization c. after vectorization. Keep this one short!

- Evolution of tone and uncertainty (and possibly changes of those metrics, but not really informative)
- Academic wordcloud - most frequent negative words (also by topic) with respective frequency (or weights)
- Dicuss the word drought around 2000! - Keeping that in should work against me and taking it out after observing it might possibly induce bias

## 2 Methodology: Topic modelling and tone computation

### 2.1 LDA setup

Roughly summarize section 3.2 of JeWu, for intuition have another look at the youtube video by the Italian.
Also include some graphic for the two-sequential distributions intuition
Parameter optimization doesn't really add any academic insight, best to just follow JeWu and use 8 topcis.

### 2.2 LDA vs NMF

Not sure yet on the performance metric, running all results with both methods seems a little over the top, coherence score might be a good ex-ante proxy.
Simple side-by-side comparison of top 4 topics and relevant words will do, along with some quantitative measure like coherence.

### 2.3 Tone computation

Short description of dictionary-lookup process and aggregation to document-level net tone score.
For overall-document tone without topic modelling, set topic proportions symmetrically to 1. That leaves the sum of the tone-specific words scaled by the paragraph length. (Using the same setup with different inputs is cleaner than two separate approaches)

### 2.4 Descriptives

Intertemporal progression of topic shares and net tone per document

## 3 Empirical results

### 3.1 Minutes and the Market (contemporaneous correlations)

Linking tone (and derivatives like tone change etc) to market
Linking uncertainty to market, esp volatility

### 3.2 Predicting market with Twitter

Loosely following Azar 2016

### 3.3 Predicting tone with Twitter

My unique contribution, might have mildly interesting implications in combination with prior two results.

### 3.4 Predictive power of uncertainty

## (Check uniqueness of finding)

Can finding be explained using established models? (Eg a new trading strategy using a regular Fama-French-5-factor model)
If so, room for further dissection (eg see Time series momentum: Even though tsm can be explained with csm, the prior actually constitutes part of the latter. Thus, chain of causation is suggested.)

## 4 Implications/Interpretation/Dicussion

Assuming negligible sentiment leakage from the Fed and, if Twitter can predict FOMC tone, the FOMC merely aggregates public sentiment. (Even if Twitter merely predicts a third factor which causes FOMC sentiment, that - under the no-leakage assumption - will be in the public realm as well). Thus, this association determines the "uniquness" of the FOMC's tone.

## 5 Robustness checks

#### Lookahead bias in model training - do if time allows

Concern by Schmeling/Wagner about lookahead bias if topic model is trained with whole-period data. Would make sense if I were to predict topic proportions or the like but is that really also the case when predicting market returns? - sequential model training with data of previous 5-10 years

#### 2011

Pre- and post-2011 behavior of market correlations

#### NMF - direkt in Hauptteil

Do NMF as a robustness test, if it does perform better, switch the entire layout and develop the first section around NMF, including ADL as a robustness check

#### Different methods for tone computation

Aggregate tone using **sign** instead of absolute score - every paragraph is either + or -, these values are then aggregated to the document-level (paragraph-based tone computation)

## 6 Conclusion

tbd