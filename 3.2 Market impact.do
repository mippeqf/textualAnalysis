cls
clear
set scheme s2color
// set scheme s1mono
eststo clear
set graphics off

use ".\data\3 dataPrepared.dta", clear

tsset trading_days
sort trading_days

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
quietly eststo: reg V dissent
quietly eststo: reg V dl_nettone dl_uncert dissent
quietly eststo: reg V L(1/10).V dl_nettone
quietly eststo: reg V L(1/10).V dl_uncert
quietly eststo: reg V L(1/10).V dissent
quietly eststo: reg V L(1/10).V dl_nettone dl_uncert dissent
esttab, ar2 indicate("Lagged volatility" = L*.V) 

// Return
eststo clear
quietly eststo: reg R_intra dl_nettone
quietly eststo: reg R_intra dl_uncert
quietly eststo: reg R_intra dissent
quietly eststo: reg R_intra dl_nettone dl_uncert dissent
quietly eststo: reg R_24 dl_nettone
quietly eststo: reg R_24 dl_uncert
quietly eststo: reg R_24 dissent
quietly eststo: reg R_24 dl_nettone dl_uncert dissent
esttab, ar2

// -----------------------------------------------------
// INFORMATIVENESS OF INDIVIDUAL TOPICS
// -----------------------------------------------------
// Technical note: Drop the first topic to avoid quasi-multicollinearity! Stata doesn't complain because topic weights don't add up to 1 precisely, but margin is less than 1%, so standard errors will be large and significance will suffer
// Amendment: Drop constant instead, interpretations are cleaner that way!

// QUANTITATIVE
eststo clear
quietly eststo: reg V L(1/10).V ldaprop*, nocons
quietly eststo: reg V ldaprop*, nocons
quietly eststo: reg R_intra ldaprop*, nocons
quietly eststo: reg R_24 ldaprop*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Financial markets and consumption are significant. Coeff of consumption is negative, thus talk about consumption can be assumed to overall be more positive than negative. - Can I control for the tone of consumption to determine whether the quantity is actually relevant? Not really, best to just use general macro variables for that
eststo clear
quietly eststo: reg V L(1/10).V nmfprop*, nocons
quietly eststo: reg V nmfprop*, nocons
quietly eststo: reg R_intra nmfprop*, nocons
quietly eststo: reg R_24 nmfprop*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)


// QUALITATIVE
// Net tone LDA
eststo clear
quietly eststo: reg V L(1/10).V ldanettone*, nocons
quietly eststo: reg V ldanettone*, nocons
quietly eststo: reg R_intra ldanettone*, nocons
quietly eststo: reg R_24 ldanettone*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Nettone NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfnettone*, nocons
quietly eststo: reg V nmfnettone*, nocons
quietly eststo: reg R_intra nmfnettone*, nocons
quietly eststo: reg R_24 nmfnettone*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert LDA
eststo clear
quietly eststo: reg V L(1/10).V ldauncert*, nocons
quietly eststo: reg V ldauncert*, nocons
quietly eststo: reg R_intra ldauncert*, nocons
quietly eststo: reg R_24 ldauncert*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfuncert*, nocons
quietly eststo: reg V nmfuncert*, nocons
quietly eststo: reg R_intra nmfuncert*, nocons
quietly eststo: reg R_24 nmfuncert*, nocons
esttab, ar2 indicate("Lagged volatility" = L*.V)
