cls
clear
set scheme s2color
// set scheme s1mono
eststo clear


import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\BOPGSTB.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename bopgstb tradebalance
save ".\statics\tb.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\CPIAUCSL.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename cpiaucsl cpi
save ".\statics\cpi.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\FEDFUNDS.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename fedfunds interest
save ".\statics\interest.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\UNRATE.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename unrate unemployment
save ".\statics\unemployment.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\USREC.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename usrec recession
save ".\statics\recession.dta", replace

use ".\3 dataPrepared.dta", clear
merge 1:m date using ".\statics\tb.dta", nogen
merge 1:m date using ".\statics\cpi.dta", nogen
merge 1:m date using ".\statics\interest.dta", nogen
merge 1:m date using ".\statics\unemployment.dta", nogen
merge 1:m date using ".\statics\recession.dta", nogen
drop if date < td(29january1993)

// Set dataset up as timeseries to use lag operators in regressions
drop trading_days
bcal create spy_cal, from(date) replace generate(trading_days)
tsset trading_days

// Lag control variables forwards
replace cpi = cpi[_n] if missing(cpi)

local controls "tradebalance cpi interest unemployment recession"

// Start with volatility (controlled for k lags), then move onto directional changes - 1. Does anything happen at all? - 2. Does stuff happen the way our model would predict (pos tone means higher equity)
// Return is the same as directional change in JeWu

// -----------------------------------------------------
// "CONTROL REGRESSION" - fomcdummy
// -----------------------------------------------------
eststo clear
quietly eststo: reg R_intra fomcdummy
quietly eststo: reg V fomcdummy
quietly eststo: reg volume fomcdummy
esttab, ar2 

// -----------------------------------------------------
// DOCUMENT-LEVEL NETTONE & UNCERT ASSOCIATION
// -----------------------------------------------------
// Volume
eststo clear
quietly eststo: reg V dl_nettone
quietly eststo: reg V dl_uncert
quietly eststo: reg V dl_nettone dl_uncert
quietly eststo: reg V L(1/10).V dl_nettone
quietly eststo: reg V L(1/10).V dl_uncert
quietly eststo: reg V L(1/10).V dl_nettone dl_uncert
esttab, ar2 indicate("Lagged volatility" = L*.V)

// Return
eststo clear
quietly eststo: reg R_intra dl_nettone
quietly eststo: reg R_intra dl_uncert
quietly eststo: reg R_intra dl_nettone dl_uncert
quietly eststo: reg R_24 dl_nettone
quietly eststo: reg R_24 dl_uncert
quietly eststo: reg R_24 dl_nettone dl_uncert
esttab, ar2

// -----------------------------------------------------
// INFORMATIVENESS OF INDIVIDUAL TOPICS
// -----------------------------------------------------
// Technical note: Drop the first topic to avoid quasi-multicollinearity! Stata doesn't complain because topic weights don't add up to 1 precisely, but margin is less than 1%, so standard errors will be large and significance will suffer

// QUANTITATIVE
eststo clear
quietly eststo: reg V L(1/10).V proptopic2-proptopic8
quietly eststo: reg V proptopic2-proptopic8
quietly eststo: reg R_intra proptopic2-proptopic8
quietly eststo: reg R_24 proptopic2-proptopic8
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Financial markets and consumption are significant. Coeff of consumption is negative, thus talk about consumption can be assumed to overall be more positive than negative. - Can I control for the tone of consumption to determine whether the quantity is actually relevant? Not really, best to just use general macro variables for that

// QUALITATIVE
// Net tone LDA
eststo clear
quietly eststo: reg V L(1/10).V ldanettone2-ldanettone8
quietly eststo: reg V ldanettone2-ldanettone8
quietly eststo: reg R_intra ldanettone2-ldanettone8
quietly eststo: reg R_24 ldanettone2-ldanettone8
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Nettone NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfnettone2-nmfnettone8
quietly eststo: reg V nmfnettone2-nmfnettone8
quietly eststo: reg R_intra nmfnettone2-nmfnettone8
quietly eststo: reg R_24 nmfnettone2-nmfnettone8
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert LDA
eststo clear
quietly eststo: reg V L(1/10).V ldauncert2-ldauncert8
quietly eststo: reg V ldauncert2-ldauncert8
quietly eststo: reg R_intra ldauncert2-ldauncert8
quietly eststo: reg R_24 ldauncert2-ldauncert8
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfuncert2-nmfuncert8
quietly eststo: reg V nmfuncert2-nmfuncert8
quietly eststo: reg R_intra nmfuncert2-nmfuncert8
quietly eststo: reg R_24 nmfuncert2-nmfuncert8
esttab, ar2 indicate("Lagged volatility" = L*.V)
