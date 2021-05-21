cls
clear
set scheme s2color
set scheme s1mono
eststo clear
set graphics off

use ".\data\vixPrep.dta"


//--------------------------------------------------
// Prepare vix data set
//--------------------------------------------------

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\VIXCLS.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename vixcls vix
save ".\statics\vix.dta", replace

// Merge
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\marketImpact.dta", nogen
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!
sort date // Just to make sure

// Create derivative variables
drop if missing(vix) // business calendar doesn't include non-weekend holidays! Although regression employs casewise deletion, computing deltas will still introduce problems, thus drop missing observations beforehand
// bcal create vix_cal, from(date) replace generate(trading_days)
// tsset trading_days
gen d_vix = vix[_n]-vix[_n-1], after(vix)

// Set dataset up as timeseries to use lag operators in regressions
// bcal create spy_cal, from(date) replace generate(trading_days)
// tsset trading_days

save ".\data\vixPrep.dta", replace

// ---------------------------------
// Timeseries setup
// ---------------------------------

// Newey doesn't accept business calendars even though they've been around for several years now. Because dates need to be spaced perfectly evenly without missing values in the regressand and regressors, I generate a new date variable and replace missing regression variables by their lcoeffsed versions.
gen pseudodate = _n, after(date) // Pseuodate will do, bcal probably does the same
tsset pseudodate
tsfill
replace vix = vix[_n-1] if missing(vix)
replace fomcdummy = 0 if missing(fomcdummy)
replace d_vix = 0 if missing(d_vix)
foreach a of varlist dl* {
	replace `a' = `a'[_n-1] if missing(`a')
}
foreach a of varlist lda* {
	replace `a' = `a'[_n-1] if missing(`a')
}
foreach a of varlist nmf* {
	replace `a' = `a'[_n-1] if missing(`a')
}

drop if date < date("29/01/1993", "DMY") // Vix goes back to 1990

// ---------------------------------
// Impact analyses
// ---------------------------------

// Document-level regressions
impact vix dl_nettone 0 500 30
graph export ".\img\pred\DLnettoneONvix.png", replace
impact vix dl_uncert 0 500 30
graph export ".\img\pred\DLuncertONvix.png", replace

// Topic-level regressions
impact vix ldanettone* 0 500 30
graph export ".\img\pred\ldanettoneONvix.png", replace
impact vix ldauncert* 0 500 30
graph export ".\img\pred\ldanetuncertONvix.png", replace
impact vix nmfnettone* 0 500 30
graph export ".\img\pred\nmfnettoneONvix.png", replace
impact vix nmfuncert* 0 500 30
graph export ".\img\pred\nmfuncertONvix.png", replace


exit