cls
clear
set scheme s2color
// set scheme s1mono
eststo clear
set graphics off

use ".\data\marketImpact.dta", clear

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
quietly eststo: reg V dl_nettone, r
quietly eststo: reg V dl_uncert, r
quietly eststo: reg V dissent, r
quietly eststo: reg V dl_nettone dl_uncert dissent, r
quietly eststo: reg V L(1/10).V dl_nettone, r
quietly eststo: reg V L(1/10).V dl_uncert, r
quietly eststo: reg V L(1/10).V dissent, r
quietly eststo: reg V L(1/10).V dl_nettone dl_uncert dissent, r
esttab, ar2 indicate("Lagged volatility" = L*.V) 

// Return
eststo clear
quietly eststo: reg R_intra dl_nettone, r
quietly eststo: reg R_intra dl_uncert, r
quietly eststo: reg R_intra dissent, r
quietly eststo: reg R_intra dl_nettone dl_uncert dissent, r
quietly eststo: reg R_24 dl_nettone, r
quietly eststo: reg R_24 dl_uncert, r
quietly eststo: reg R_24 dissent, r
quietly eststo: reg R_24 dl_nettone dl_uncert dissent, r
esttab, ar2

// -----------------------------------------------------
// INFORMATIVENESS OF INDIVIDUAL TOPICS
// -----------------------------------------------------
// Technical note: Drop the first topic to avoid quasi-multicollinearity! Stata doesn't complain because topic weights don't add up to 1 precisely, but margin is less than 1%, so standard errors will be large and significance will suffer
// Amendment: Drop constant instead, interpretations are cleaner that way!

// QUANTITATIVE
eststo clear
quietly eststo: reg V L(1/10).V ldaprop*, nocons r
quietly eststo: reg V ldaprop*, nocons r
quietly eststo: reg R_intra ldaprop*, nocons r
quietly eststo: reg R_24 ldaprop*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Financial markets and consumption are significant. Coeff of consumption is negative, thus talk about consumption can be assumed to overall be more positive than negative. - Can I control for the tone of consumption to determine whether the quantity is actually relevant? Not really, best to just use general macro variables for that
eststo clear
quietly eststo: reg V L(1/10).V nmfprop*, nocons r
quietly eststo: reg V nmfprop*, nocons r
quietly eststo: reg R_intra nmfprop*, nocons r
quietly eststo: reg R_24 nmfprop*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)


// QUALITATIVE
// Net tone LDA
eststo clear
quietly eststo: reg V L(1/10).V ldanettone*, nocons r
quietly eststo: reg V ldanettone*, nocons r
quietly eststo: reg R_intra ldanettone*, nocons r
quietly eststo: reg R_24 ldanettone*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Nettone NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfnettone*, nocons r
quietly eststo: reg V nmfnettone*, nocons r
quietly eststo: reg R_intra nmfnettone*, nocons r
quietly eststo: reg R_24 nmfnettone*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert LDA
eststo clear
quietly eststo: reg V L(1/10).V ldauncert*, nocons r
quietly eststo: reg V ldauncert*, nocons r
quietly eststo: reg R_intra ldauncert*, nocons r
quietly eststo: reg R_24 ldauncert*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfuncert*, nocons r
quietly eststo: reg V nmfuncert*, nocons r
quietly eststo: reg R_intra nmfuncert*, nocons r
quietly eststo: reg R_24 nmfuncert*, nocons r
esttab, ar2 indicate("Lagged volatility" = L*.V)
