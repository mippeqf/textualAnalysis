cls
clear
set scheme s1mono
eststo clear

// Python can be called from within stata, perhaps do a master stata file

//--------------------------------------------------
// DATA PREPARATION
//--------------------------------------------------

// Parse minutes
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\data\dataExport.csv", clear
tostring release, replace
generate date = date(release,"YMD"), after(release)
format %tdDD/NN/CCYY date
label variable date "Release date"
drop release filteredparagraphs 
save "./data/tone.dta", replace

// Parse financial data
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date
save "./data/spyYF.dta", replace

// Merge
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\tone.dta", 
sort date // Just to make sure
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!

// Create derivative variables
gen fomcdummy=cond(missing(year),0,1)
gen R_24 = (close-close[_n-1])/close[_n-1], after(close)
label var R_24 "Close-close diff"
gen R_intra = (close-open)/open, after(R_24)
label var R_intra "Intraday return, close-open diff"
gen vola_temp = high-low, after(close)
sum(vola_temp)
gen V = (high-low)/r(sd), after(vola_temp)

// Set dataset up as timeseries to use lag operators in regressions
bcal create spy_cal, from(date) replace generate(trading_days)
tsset trading_days

//--------------------------------------------------
// DESCRIPTIVES
//--------------------------------------------------
// Stuff to do in Python:
// - Proportion evolution (see Medium article)
// - Wordcloud by topic (as list with according topic weights in second column)

// line volume date // JeWu start in 2000 as prior spy vol is low

// Word drought around 2000
// line posnegcnt date if _merge==3
// line uncertcnt date if _merge==3

//--------------------------------------------------
// EMPIRICAL TESTS
//--------------------------------------------------
// Start with volatility (controlled for k lags), then move onto directional changes - 1. Does anything happen at all? - 2. Does stuff happen the way our model would predict (pos tone means higher equity)
// Return is the same as directional change in JeWu

// "Control regressions" - dummy and document-level
eststo clear
quietly eststo: reg R_intra fomcdummy
quietly eststo: reg V fomcdummy
quietly eststo: reg volume fomcdummy
esttab, ar2 

eststo clear
quietly eststo: reg V dl_nettone
quietly eststo: reg V dl_uncert
quietly eststo: reg V dl_nettone dl_uncert
quietly eststo: reg V L(1/10).V dl_nettone
quietly eststo: reg V L(1/10).V dl_uncert
quietly eststo: reg V L(1/10).V dl_nettone dl_uncert
esttab, ar2 indicate("Lagged volatility" = L*.V)

eststo clear
quietly eststo: reg R_intra dl_nettone
quietly eststo: reg R_intra dl_uncert
quietly eststo: reg R_intra dl_nettone dl_uncert
quietly eststo: reg R_24 dl_nettone
quietly eststo: reg R_24 dl_uncert
quietly eststo: reg R_24 dl_nettone dl_uncert
esttab, ar2

// Informativeness of individual topics
eststo clear
quietly eststo: reg V L(1/10).V nettone*
quietly eststo: reg V nettone*
quietly eststo: reg R_intra nettone*
quietly eststo: reg R_24 nettone*
esttab, ar2 indicate("Lagged volatility" = L*.V)
eststo clear
quietly eststo: reg V L(1/10).V uncert*
quietly eststo: reg V uncert*
quietly eststo: reg R_intra uncert*
quietly eststo: reg R_24 uncert*
esttab, ar2 indicate("Lagged volatility" = L*.V)