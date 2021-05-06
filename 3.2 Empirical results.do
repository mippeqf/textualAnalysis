cls
clear
set scheme s2color
// set scheme s1mono
eststo clear

use ".\3 dataPrepared.dta", clear

//--------------------------------------------------
// EMPIRICAL TESTS
//--------------------------------------------------
// Start with volatility (controlled for k lags), then move onto directional changes - 1. Does anything happen at all? - 2. Does stuff happen the way our model would predict (pos tone means higher equity)
// Return is the same as directional change in JeWu

// "CONTROL REGRESSION" - fomcdummy
eststo clear
quietly eststo: reg R_intra fomcdummy
quietly eststo: reg V fomcdummy
quietly eststo: reg volume fomcdummy
esttab, ar2 

// DOCUMENT-LEVEL NETTONE & UNCERT ASSOCIATION
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

// INFORMATIVENESS OF INDIVIDUAL TOPICS
// Net tone LDA
eststo clear
quietly eststo: reg V L(1/10).V ldanettone*
quietly eststo: reg V ldanettone*
quietly eststo: reg R_intra ldanettone*
quietly eststo: reg R_24 ldanettone*
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Nettone NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfnettone*
quietly eststo: reg V nmfnettone*
quietly eststo: reg R_intra nmfnettone*
quietly eststo: reg R_24 nmfnettone*
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert LDA
eststo clear
quietly eststo: reg V L(1/10).V ldauncert*
quietly eststo: reg V ldauncert*
quietly eststo: reg R_intra ldauncert*
quietly eststo: reg R_24 ldauncert*
esttab, ar2 indicate("Lagged volatility" = L*.V)
// Uncert NMF
eststo clear
quietly eststo: reg V L(1/10).V nmfuncert*
quietly eststo: reg V nmfuncert*
quietly eststo: reg R_intra nmfuncert*
quietly eststo: reg R_24 nmfuncert*
esttab, ar2 indicate("Lagged volatility" = L*.V)

//--------------------------------------------------
// Twitter predictiveness
//--------------------------------------------------

// Possibly do topic modelling on Twitter posts to run separate corrleations for topics
// https://ourcodingclub.github.io/tutorials/topic-modelling-python/