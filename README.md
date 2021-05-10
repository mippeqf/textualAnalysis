# Textual Analysis

## 0 Abstract/Introduction

Start with Baker Wurgler, short overview over the sentiment literature
Examining news releases is particularly interesting because ...
Summarize every one of the following sections in a short paragraph
Clearly state how this thesis might contribute to the literature

Two aims:

1. Examine the impact of FOMC minutes on the market using 
   a. a simple word-count method (which will likely yield results that are rather unexciting)
   b. a topic-modelling approach, as individual topics are likely to be perceived with individual significance. Comparison of two methods: LDA and NMF
2. Prediction of FOMC minutes tone as a whole and topic-wise using Twitter data
3. If both of the first and second step yield significant results, test whether spy returns are predictable. (Evidence that they are from Azar)

## 1 Introduction - leave this open until the end

<details>
    <summary>Introduction</summary>
   - Baker Wurgler 2006 is the key paper regarding sentiment. They use a number of proxies (eg closed-fund discount, NYSE volume etc) but analyzing tone is nothing other than using textual data as a proxy for sentiment. —> Start of with sth like "Starting with Baker Wurgler, financial academia has seen a rapid increase in the research on sentiment as a determinant of asset pricing. In recent years, analyses of textual tone in relevant data has established itself as (one of) the most promising subareas in the field."
- Side note on general qualitative data, eg noise level matters on trading floors (can predict volatility!)
- Especially interesting to look at sentiment regarding specific news releases due to a number of reasons: (Look at JegadeeshWu, good Motivation section, also Azar, all 3 Schmeling papers on Sentiment and Hillert's work)
  Also delineate from other subfields of research that do not offer these benefits.
- Summarize every following \section{} with one paragraph
- Relate presented work to all relevant fields of literature
- Clearly state how this paper contributes to the above literature: 
  - Predictiveness of both FOMC tone and Twitter sentiment has been shown to be indicative of market returns
  - What has yet not been examined is the predictive power of Twitter sentiment for FOMC tone.
  - If relationship is significant, then predictive power of Twitter works at least partially through gauging central bank tone.
  - If relationship does not hold (insignificance of t-test might not enough!), that's an indication for Twitter predicting something other than FOMC tone. Because Twitter sentiment preceeds FOMC tone and leakage of  information from inside the Fed to social media is likely negligible, we can assume that Twitter sentiment is not endogenous.
- One paragraph on how the paper proceeds (Really just put the subheaders into sentences: Section 2 does this, section 3 does that and we'll conclude with section 4)
- Because a paper on this topic has already been published, I closely follow it and expand upon it in places where I see fit
</details>

#### 1.1 Motivation

Why is this an interesting question to ask

#### 1.2 Summary by main section

One paragraph (about 5 sentences) on every major section - save this until the end obvs

#### 1.3 Literature & Contribution

How does my stuff relate to the existing literature? Simply wrangle together 3-5 sections of similar papers on this one (Look for a brand-new one, should give good overview)

Schmeling: 1. Effect of mopo on asset prices in general 2. Quantification of mopo effect (by using short time window around release) 3. Equity returns around poliy meetings (Lucca Moench)

My contribution: To the best of my knowledge, I'm the first to use NMF on FOMC Minutes. Previous work has been done by Jegadeesh and Wu employing LDA 

#### 1.4 Paper structure

One paragraph with one sentence each for every major topic. Essentially just the section topics put into sentences.

## 2 Data

#### 2.1 Data sources

The dataframe used for further empirical analyses comprises three separate datasets and sources:

1. Textual data of the FOMC meeting minutes scraped from the website of the Federal Reserve, parsed and prepared using custom-built Python scripts
2. Time series of the S&P500's open, high, low, close and volume on a daily basis sourced from Yahoo Finance using the Python library yfinance **cite**
3. Time series of several macroeconomic variables employed primarily as control variables from FRED St Louis

In addition, the sentiment dictionary for financial terminology developed by Loughran and McDonald **cite** is used to compute scores of FOMC tone based on the Meeting Minutes. 

**TODO** FOMC minutes data: paragraph on why specifically those (include diagram from that one fomc publication on minutes types)

**3 types of Minutes**: - although the format of these documents does change slightly, it's worth it to examine 

- Modern ones - 1993 to present (released at 2pm at least since 2005 - https://www.federalreserve.gov/pubs/bulletin/2005/spring05_fomc.pdf)
- Record of Policy Actions and Minutes of Actions - 67 to 92 (Varying publication schedule)
- Historical Minutes - 36 to 67 - Were not published until 1964 (under the Freedom of Information Act), thus not interesting in regards to market impact

#### 2.2 Selection of minutes and preparation of textual data

- FOMC minutes background

  - Chosen because they provide rich information on the disucssion within the commitee and thereby lend themselves very well to seach for emotional clues between the lines in regards to policy maker sentiment. Transcripts are an alternativet hat would offer an even greater level of detail, however these documents have historially not been released on a fixed schedule and due to their nature verbatim nature, are even harder to process. In particular, advanced natural language processing techniques such as topic modelling to not lend themselves very well to unstructured text. 
  - The kind of minutes published in recent years have only been released starting in 1993 with {story of chair being pressured into more transparency}. Thus, I source minutes only within that time period. Historical tests would in theory also be possible, however documents before that point had originally not been intended to be published and were only released in the wake of {the transparency story}.
  - The most prominent publication by the FOMC are however the "Statements" which briefly summarize the Minutes' content. Although the length of the statements had been continually rising until Janet Yellen became chair of the comittee in 2014, their overall brevity inhibits impedes the construction of consistent estimators of sentiment. 
  - Hence, the Minutes offer the ideal tradeoff between the level of detail and a sense of structured coherence that facilitates topic modelling techniques.

  <img src="C:\Users\Markus\Desktop\BA\textualAnalysis\statics\Minutes nomenclature.PNG" style="zoom:33%;" />

- Processing details
  - Use html parsing library bs4 **cite** to parse raw html files and use pre-trained text classification framework "spacy" **cite** to extract the most content-relevant words on a paragraph level. Specifically, only extract nouns, verbs and adjectives and finally lemmatize and lowercase those. 
  - Although reliant on a heuristic-based framework like spacy, this black-box approach performs significantly better than basic stop-word removal and stemming at purging words that do not make a meaningful contribution towards information content and thus would only add noise to the topic-modelling techniques employed at later stages.
  - Do not merge LM dict with Harvard, as this is precisely the thing bias that LM wanted to avoid!

#### 2.3 Descriptives

**Raw counts**: Examining raw word counts by content type reveals surprisingly much about the changing language of the committee in regards to macroeconomic events. While the number of positive and uncertain words (color and color in fig abscontentCounts) closely follows the pattern of the overall word count (fig totalWordCount), the number of negative words (color) seems much more sensitive to economic and financial crises, such as the aftermath of the dotcom bubble, the 2008 financial crisis and the economic reaction to the sanctions due to the Coronavirus pandemic. The progression of the number of content-specific words relative to the overall word count (fig relContentCounts) reveals that these three events did in fact cause the highest (relative) spikes in the usage of negative words. Peculiarly, the pessimism in the minutes' tone seems to have spiked close to the level of the financial crisis 2008 only 3-4 years later again before settling down to non-crisis levels until the global pandemic struck in 2020.

<img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\abscontentCounts.png" style="zoom:33%;" /> <img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\totalNumberWords.png" style="zoom:33%;" /><img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\relContentCounts.png" alt="relContentCounts" style="zoom:33%;" />





- **Academic wordcloud** - most frequent negative words (also by topic) with respective frequency (or weights)
- **Paragraph before and after:** Random minutes paragraph a. before processing b. after tokenization and lemmatization c. after vectorization. Keep this one short!

#### 2.4 Derivative variables

- Variance: Open-low because that measure carries a higher information content than daily returns squared. At the same time, it doesn't penalize higher deviation disproportionally, which is sth OLS does, but what isn't really desirable. Deviations are squared in OLS simply because the target function is of second order and thereby very tractable, ie slap on a FOC and you're done. Absolute deviations aren't employed because they produce a non-continuous target function. Point is that squared deviations are simply chosen because they're convenient to work with, but since we can construct a more detailed volatility measure out of the high and low values, we take advantage of that.

## 3 Methodology: Topic modelling and tone computation

#### 3.1 Topic modelling

Roughly summarize section 3.2 of JeWu, for intuition have another look at the youtube video by the Italian.
Also include some graphic for the two-sequential distributions intuition
Parameter optimization doesn't really add any academic insight, best to just follow JeWu and use 8 topcis.

- Implementation using gensim **cite**, purging words that appear less than 3 times in the entire corpus and those that appear in more than 85% of documents
- Models are trained on entire-period documents, for OOS robustness test see penultimate section
- Use N=10 topics because I do not remove the admin section

#### 3.3 Tone computation

Tone without differentiation between topics is computed by multiplying the frequency of terms $\phi$ of a given sentiment topic $c\in\{positive, negative, uncertain\}$ in paragraph $p$ at time $t$ with the proportion of words $\omega$ that the same paragraph comprises of total document length $\Omega$. This score is summed over all paragraphs in a minutes document, such that the resulting metric $\Lambda$ measures the average score of sentiment type $c$ at time $t$, weighted by the length of the corresponding paragraph relative to overall document length:
$$
\Lambda_{c,t} = \sum_{p=1}^P \phi_{c,p,t}\frac{\omega_{p,t}}{\Omega_t}
$$
Jegadeesh and Wu employ a slightly different weighting scheme in their 2015 paper; specifically, they weigh the paragraph-level tone score by the inverse paragaph length, arguing that the relevance of sentiment-specific term frequency declines in the length of the paragraph. This notion is based on the assumption that longer sections are generally more difficult to comprehend and thus transmit a lower impact per emotion-specific word. Although I would see this specification fit for purposes with a more popular audience, I believe that because publications of this type are targeted specifically at a professional audience, section length does not compromise the perceived weight of sentiment-specific words. Hence positing a (positive) linear relationship between the number of words assigned to sentiment category $c$ and the paragraph sentiment score, I weigh paragraphs proportionally to their relative length instead of inversely to their absolute length. Dividing by the document's length has the additional advantage of not assuming stationarity of the overall level of detail of the minutes' writing style. Evidence for non-stationarity is apparent in **table X**, showing the total word count of the entire document steadily declining by about 1/3 until 2005 and since doubling until today. A weighting scheme that does not account for this type of variability would - assuming uniform sentiment word distribution - assign higher sentiment scores to longer publications, even if differing document length was entirely caused by variations in the level of detail.

To compute topic-specific tone $\lambda$, the weighted term frequency $\phi_{c,p}$ is additionally multiplied with the estimated model-generated weight $\theta$ of topic $n$ in paragraph $p$ before summing over all paragraphs:
$$
\lambda_{n,c,t} = \sum_{p=1}^P \theta_{c,n,p,t}\phi_{c,p,t}\frac{\omega_{p,t}}{\Omega_t}
$$

### 3.4 Descriptives

1. Progression of tone and uncertainty on a document level
2. Progression of topic shares

<img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\DLtone.png" style="zoom:33%;" /> <img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\ldaProp1-4.png" style="zoom:33%;" /><img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\ldaProp5-8.png" style="zoom:33%;" /><img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\nmfProp1-4.png" style="zoom:33%;" /><img src="C:\Users\Markus\Desktop\BA\textualAnalysis\img\nmfProp5-8.png" style="zoom:33%;" />

### Copied

#### Market impact

- Bag of word method (using only negative words from the LM dictionary - see Schmeling 2015)
- Topic modelling
  - Rough overview over workings of and intuition for ADL (use JeWu!) and NMF
  - *The objective of topic models is to extract the underlying topics from a given collection of text documents. Each document in the text is considered as a combination of topics and each topic is considered as a combination of related words.* [source](https://www.machinelearningplus.com/nlp/gensim-tutorial/#6howtocreateabagofwordscorpusfromatextfile)
- ADL
  - Include that generic diagram about the parameter structure
  - Iteration over every word with computation of probability that given word belongs to any category. Two criteria: Probability of obtaining word given certain topic and probability of obtaining topic given the current document. Word is assigned the topic which from both criteria seems "more certain"
  - That process is done over and over again until it converges (necessity of convergence can probably be proven mathematically)
- NMF
  - Dimensionality reduction, similar to PCA - only works when components are positive (similar to PCA)
  - A is the vectorized corpus, ie words as features/columns/variables, (rows are the documents, and values are the count of word in the given column)
  - Factorization cannot be solved in closed form, but has to be approximated. Thus minimize an error function that squares the deviation of the product of the estimated factors from the actual document-word matrix. 
  - As with ADL, more iteration means more precise approximation and thus 

#### Predictability

- Twitter in regards to FOMC/Fed/{name of then fed chair} as predictor for tone
  - Works sort of like an instrumental variable: Correlated with tone and also exogenous, but tone itself is exogenous, thus a fitting name would be "two-stage predictor"
- Uncertainty and Policy scores as predictors for macroeconomic variables - Use a VAR most likely

## 4 Empirical results

#### 4.1 Minutes and the Market (contemporaneous correlations)

Linking tone (and derivatives like tone change etc) to market
Linking uncertainty to market, esp volatility

// Start with volatility (controlled for k lags), then move onto directional changes - 1. Does anything happen at all? - 2. Does stuff happen the way our model would predict (pos tone means higher equity)
// Return is the same as directional change in JeWu

#### 4.2 Predicting market with Twitter

Loosely following Azar 2016

#### 4.3 Predicting tone with Twitter

My unique contribution, might have mildly interesting implications in combination with prior two results.

#### 4.4 Predictive power of uncertainty

## (Check uniqueness of finding)

Can finding be explained using established models? (Eg a new trading strategy using a regular Fama-French-5-factor model)
If so, room for further dissection (eg see Time series momentum: Even though tsm can be explained with csm, the prior actually constitutes part of the latter. Thus, chain of causation is suggested.)

## 5 Implications/Interpretation/Dicussion

Assuming negligible sentiment leakage from the Fed and, if Twitter can predict FOMC tone, the FOMC merely aggregates public sentiment. (Even if Twitter merely predicts a third factor which causes FOMC sentiment, that - under the no-leakage assumption - will be in the public realm as well). Thus, this association determines the "uniquness" of the FOMC's tone.

## 6 Robustness checks

#### Lookahead bias in model training - do if time allows

Concern by Schmeling/Wagner about lookahead bias if topic model is trained with whole-period data. Would make sense if I were to predict topic proportions or the like but is that really also the case when predicting market returns? - sequential model training with data of previous 5-10 years

#### 2011

Pre- and post-2011 behavior of market correlations

#### NMF - direkt in Hauptteil

Do NMF as a robustness test, if it does perform better, switch the entire layout and develop the first section around NMF, including ADL as a robustness check

#### Different methods for tone computation

Aggregate tone using **sign** instead of absolute score - every paragraph is either + or -, these values are then aggregated to the document-level (paragraph-based tone computation)

#### Dissent variable

- Examine association of at least one comitee member dissenting in the final vote and market reaction, specifically volatility! Perhaps lower response than normal if added to other regressions because decision doesn't seem quite as firm?
- Reference Madeira & Madeira 2017 <cite> Lucca Moench 2017</cite>

#### Copied

- OOS test for topic modelling (Schm 2015 2.2)
- Merge LM and Harvard dictionaries
- *Robustness is not just about adding alternative control varibles, but more generally about assessing the same question with a slightly different approach. Also good opportunity to obviate critiques on methodology*

#### Top topic specification

## 7 Conclusion

tbd

## 8 Outlook

- Results could be improved by testing differing numbers of topics based eg on the coherence score. One likely contributer that my results deviate slightly from JeWu is the fact that I do not trim the admin section, as this is hard to do both objectively and thereby in an algorithmic fashion. A higher number of topics (eg 10) should allow for separation of topics in the admin section and thereby improve topic coherence in the core section.



----



# Notes

- Minutes live since 1993 (Jeg, Schm, [FOMC website](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm), Emmanuel paper)
- Overfitting through topic modelling? (Schmeling 2015 2.2) — Do OOS test!
- **Predictive power** of Uncertainty of topic "Policy" omitted in Jegadeesh and Wu (2015) — Dive into that when time allows
- **Causal relation** is established by examining a very short period of time affected by a high-impact event. Most, if not all of the price variation is highly likely to stem from the event. (Jeg and Schm both comment on that)
  - Hillert's comment on examination of causal structure: I interpret that as dissecting the different channels (eg Schmeling's discount vs outlook vs risk channel on equity)
- Handle **pre-release drift** (Lucca, Moench) - Returns are systematically different from 0 on release days (positive I think). Not the case for ECB press conferences though
- Superb article on **Medium** https://towardsdatascience.com/modeling-topic-trends-in-fomc-meetings-a10cf3d8bac5, draws on JegadeeshWu and [SaretMitra](https://www.twosigma.com/wp-content/uploads/Ai_approach.pdf) (TwoSigma Publication)
- **White standard errors** are simply the conventional robust ones, **Newey and West** are robust to heteroskedasticity and also autocorrelation (also known as HAC - Heteroskedasticity and Autocorrelation Consistent) - watch out which one to use for time series and cite the respective one (added to references already)
- One page has 400 +/- 50 words - aiming for 20-50 pages gives 10.000-20.000 words in total
- Include **Emanuel** in the Acknowledgements if transparency issue turns out to be critical
- - 

- Question that can be answered by predicting FOMC tone with Twitter data: **Does FOMC tone merely reflect public sentiment or does it produce unique, exogenous information?** — 3-Pfeil-Diagramm