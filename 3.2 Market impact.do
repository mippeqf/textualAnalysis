cls
clear
set scheme s2color
// set scheme s1mono
eststo clear

use ".\3 dataPrepared.dta", clear

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
// Technical note: Drop the first topic to avoid quasi-multicollinearity! Stata doesn't complain because topic weights don't add up to 1 precisely, but margin is less than 1%, see checkts in 

// QUANTITATIVE
eststo clear
quietly eststo: reg V L(1/10).V proptopic2-proptopic8
quietly eststo: reg V proptopic2-proptopic8
quietly eststo: reg R_intra proptopic2-proptopic8
quietly eststo: reg R_24 proptopic2-proptopic8
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Financial markets and consumption are significant. Coeff of consumption is negative, thus talk about consumption can be assumed to overall be more positive than negative. - Can I control for the tone of consumption to determine whether the quantity is actually relevant?

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
