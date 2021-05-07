cls
clear
set scheme s2color
// set scheme s1mono
eststo clear

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\VIXCLS.csv"
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename vixcls vix
save ".\statics\vix.dta", replace

// Merge
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\tone.dta", 
sort date // Just to make sure
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!

// Create derivative variables
gen fomcdummy=cond(missing(year),0,1)
gen d_vix = vix[_n]-vix[_n-1]

// Set dataset up as timeseries to use lag operators in regressions
bcal create spy_cal, from(date) replace generate(trading_days)
tsset trading_days

save ".\3 vixPrep.dta", replace

eststo clear
quietly eststo: reg vix fomcdummy
quietly eststo: reg vix dl_nettone
quietly eststo: reg vix dl_uncert
esttab, ar2
eststo clear
quietly eststo: reg vix ldauncert2-ldauncert8
esttab, ar2
eststo clear
quietly eststo: reg vix nmfuncert2-nmfuncert8
esttab, ar2 

eststo clear
quietly eststo: reg F1.d_vix dl_uncert, r
quietly eststo: reg F2.d_vix dl_uncert, r
quietly eststo: reg F3.d_vix dl_uncert, r
quietly eststo: reg F4.d_vix dl_uncert, r
quietly eststo: reg F5.d_vix dl_uncert, r
quietly eststo: reg F6.d_vix dl_uncert, r
quietly eststo: reg F7.d_vix dl_uncert, r
quietly eststo: reg F8.d_vix dl_uncert, r
quietly eststo: reg F9.d_vix dl_uncert, r
quietly eststo: reg F10.d_vix dl_uncert, r
// All significant -- price change is persistent!
esttab, ar2
eststo clear
quietly eststo: reg F1.d_vix dl_nettone, r
quietly eststo: reg F2.d_vix dl_nettone, r
quietly eststo: reg F3.d_vix dl_nettone, r
quietly eststo: reg F4.d_vix dl_nettone, r
quietly eststo: reg F5.d_vix dl_nettone, r
quietly eststo: reg F6.d_vix dl_nettone, r
quietly eststo: reg F7.d_vix dl_nettone, r
quietly eststo: reg F8.d_vix dl_nettone, r
quietly eststo: reg F9.d_vix dl_nettone, r
quietly eststo: reg F10.d_vix dl_nettone, r
// All significant -- price change is persistent!
esttab, ar2


gen fvix = F1.vix, after(vix)
