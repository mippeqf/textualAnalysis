# Code structure

## Folders

- archive: Old versions of the scripts or assets
- data: Output of scripts upstream and input for scripts downstream
- img: Images produced to include in the thesis
- models: Models trained by NMF that are used by the model evaluation scripts
- statics: External data from FRED and Yahoo Finance
- tex: Stata table output in Latex format to be used in thesis

## Scripts

#### Data Preparation

2.1 Download SPY: Uses *yfinance* library to download the S&P500 ETF time series from Yahoo Finance and saves series to folder "statics".

2.2 Link Load: Systematically collects links to all pages that contain FOMC Meeting Minutes from the website of the Federal Reserve. Saves the data set as a pickled list of dictionaries to folder "data". Data set at this point contains links to all Meeting Minutes alongside the corresponding release date. 

2.3 Text Processing: Query every link from the server of the Federal Reserve, parse HTML, and split into paragraphs. Every paragraph is then run through an NLP pipeline provided by the open-source library *spacy* to tokenize and lemmatize words, identify syntactical word function, and filter out the most meaningful words.  The filtered paragraphs are added to the dataset as a list of lists of words. Additionally, I add a marker to the observation if one or more committee members dissented in the final vote on policy action. The data are again saved to the directory "data" as a pickled list of dictionaries.

#### Model selection and tone computation

3.1 Train Model: Use the open-source library *gensim* to produce a "dictionary" and "corpus" based on the filtered paragraphs. The dictionary assigns a unique index to every word across paragraphs, as subsequent methods require a numerical basis for calculations. The "corpus" or "bag of words" is a vector that associates the occurrence of every word within a paragraph with the unique ID provided by the dictionary. It thereby discards any information that was conveyed in the sentence structure and treats the paragraphs as an unordered set of words. The corpus is now used as an input for NMF, which I train with 6 topics.

3.2 Coherence Optimization: Trains 20 models each with a different number of topics as an input and saves every one to the folder "models". Once a model is trained, I also compute the coherence score of type *U_Mass* for both the overall model and every individual topic. The collection of both values is transformed and saved as a CSV to be graphed using Stata.
*This particular script ran for about 2 hours on my machine! To replicate only the graph construction, set the if-statement at the very top to False and load the models from the directory "models" instead.*

3.3 Tone Computation: Center piece of the entire process. Compute tone metrics according to specification in paper by iterating over documents and paragraphs. The Loughran & McDonald dictionary is loaded from a CSV for this purpose. The resulting data set is saved with name "dataExport.csv" to be imported for statistical analyses by Stata.

3.4 Model Descriptives: Load model of choice, trained in 3.1, and generate final word cloud to visualize the second factor matrix. To select 6 as the ideal number of topics, I generated word clouds for all 20 possible models, saved to img/nmfClouds. (To replicate the latter step, switch the if-statement at the top of the second block to true.) To visualize the first factor matrix, generate a topic proportion plot over time.

#### Statistical analysis in Stata

4.0 Data Preparation: Load the tone score data set produced in 3.3 and merge with financial variables on the daily level, as well as with macroeconomic variables obtained from FRED on the monthly level. Also produce derivative variables "volatility" and "return". Save data set to data/main.dta. 

4.1 Text Descriptives: Produce the simple tone progression graphs used in the thesis.

4.2 Market Impact: Straightforward regressions of tone onto intra-day market volatility and intra-day return. Generate tables with the package "estout" and save them in Latex format to the folder "tex".

4.3 Predictive Power:  Generate prediction graphs for naive tone and topic tone. Essentially just three nested for-loops that feed data into the "impact" command, which I elaborate on below.

impact.ado: Custom-built command to produce impact graphs. Takes a regressand, a list of regressors and a list of control variables as an input, alongside a few secondary parameters. For the final thesis version, data series are used to compute regressions as specified in the paper over k periods using White standard errors. The resulting array of coefficients is then fed into the library "coefplot", which plots the confidence interval over time. For the final thesis version, single graphs are produced and combined to a multi-graph image in 4.3.

4.4 Tone Strat: Compute the performance of a simple strategy as defined in the thesis and plot the cumulated P/L alongside the progression of the S&P500. Images are saved to the folder img/strat.

4.5 Coherence Graph: Load the sets of coherence scores extracted from the NMF models in 3.2 and generate graphs. This would have been possible using Matplotlib, however Stata is much more efficient and convenient regarding formatting. Plots are saved to the folder img.

## Miscellaneous files

- envVars: Holds the number of topics for the final choice of NMF model and is imported in a number of scripts.
- requirements.txt: Setup file to install libraries for replication. (*pip install requirements.txt*)
- sampleParagraphs.py: Basis for table 8 in the appendix. Sort paragraphs by topic weight and print the text of the top 5 paragraphs for every topic.
- spy_cal.stbcal: Timeseries setup support file for Stata
- All other files pertaining to coherence: Temporary storage files for the coherence score computation. Should have been moved to a separate folder (eg data). To avoid breaking anything, I refrain from doing so now though.