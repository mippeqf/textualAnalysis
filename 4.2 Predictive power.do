cls
clear
set scheme s2color
set scheme s1mono
eststo clear
set graphics on

use "data\main.dta", clear

// ---------------------------------
// Timeseries setup
// ---------------------------------

drop if missing(vix) | missing(spy) | missing(yield) | missing(bond)
// business calendar doesn't include non-weekend holidays! Although regression employs casewise deletion, computing deltas will still introduce problems, thus drop missing observations beforehand

// Newey doesn't accept business calendars even though they've been around for several years now. Because dates need to be spaced perfectly evenly without missing values in the regressand and regressors, I generate a new date variable and replace missing regression variables by their lcoeffsed versions.
gen pseudodate = _n, after(date) // Pseuodate will do, bcal probably does the same
tsset pseudodate
tsfill

// dependent vars to previous if missing -- not necessary, dropped missing ones already
// replace spy = spy[_n-1] if missing(spy)
// replace vix = vix[_n-1] if missing(vix)
// replace yield = yield[_n-1] if missing(yield)
replace fomcdummy = 0 if missing(fomcdummy)

// impact vars to 0 if missing
foreach list in dl* nmf*{
	foreach a of varlist `list'{
		replace `a' = 0 if missing(`a')
	}
}

// Kick lda
// drop lda*
	

// Attempt to purge DL nettone loading from individual topic tone combinations
// Although values differ slightly, shape of impact(residuals), regressand(spy) 
// is precisely the same for all topics. WHY? Residuals 
if 0{
	foreach tone of varlist nmfnettone*{
		reg `tone' dl_nettone, r // Doesnae matter whether to use reg or newey
			// Only predictions are used, not SEs/CIs and that's the only point of difference (obvs)
		predict double resid`tone', residuals
		label var resid`tone' "`tone' Residuals"
		replace resid`tone' = 0 if missing(link)
		// 	impact(resid`tone'), regressand(spy)
		// 	drop resid`tone'
	}
	impact(residnmfnettone*), regressand(spy)
	exit

	// Plot residuals - graphically independent!
	graph drop _all
	foreach var of varlist residnmfnettone*{
		replace `var' = . if missing(link)
		tsline `var', name(`var') yline(0) 
		local graphs "`graphs' `var'"
	}
	graph combine `graphs', title("Topic on NaiveTone Residuals") iscale(0.5)
	graph export ".\img\topicToneResiduals.png", replace
	
	// Test relationship of topic-tone residuals among one another and to dl_nettone
	// Result: not related to dl_nettone but related among each other
	eststo clear
	forvalues i = 1/7{
		local next = `i'+1
		quietly eststo: reg residnmfnettone`i' residnmfnettone`next'
		quietly eststo: reg residnmfnettone`i' dl_nettone
	}
	esttab, r2 nocons
}

exit

// ---------------------------------
// Impact analyses
// ---------------------------------

// PreReleaseVolatilityDrift
impact V, regressand(V) max(200) step(10) lag
graph export ".\img\pred\PreReleaseVolatilityDrift.png", replace

// Naive tone predictions 
	// DO NOT COMBINE WITH ROUTINE BELOW!! Otherwise you'd control for every other naive tone in the 
	// prediction regressions, but I want them standalone!
local depset = "spy bond vix" // dep for dependent variable
local controls = ""
foreach dep in `depset'{
	local deplabel: var label `dep'
	local graphs = ""
	graph drop _all
	foreach var of varlist dl_*{
		quietly impact `var', regressand(`dep') controls(`controls') keepgraph
		local graphs "`graphs' `var'"
	}
	graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with naive tone") subtitle("Controls: `controls'")
	graph export "./img/pred/naiveON`dep'.png", replace
}


local depset = "spy bond vix" // dep for dependent variable
local controls = ""
local topicset = "nmfnettone nmfuncert nmfneg nmfpos"
foreach dep in `depset'{
	local deplabel: var label `dep'
	foreach topic in `topicset'{
		local graphs = ""
		graph drop _all
		foreach var of varlist `topic'*{
			quietly impact `var', regressand(`dep') controls(`controls') keepgraph notopiccontrol
			local graphs "`graphs' `var'"
		}
		graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with `topic'") subtitle("Controls: `controls'")
		graph export "./img/pred/`topic'ON`dep'.png", replace
	}
}

exit




// Lda stuff
// impact vix ldanettone* 500 30
// graph export ".\img\pred\ldanettoneONvix.png", replace
// impact vix ldauncert* 500 30
// graph export ".\img\pred\ldanetuncertONvix.png", replace



// Time variable handling: OLD APPROACH

// gen d_vix = vix[_n]-vix[_n-1], after(vix)
// replace d_vix = 0 if missing(d_vix)

// bcal create vix_cal, from(date) replace generate(trading_days)
// tsset trading_days

// Set dataset up as timeseries to use lag operators in regressions
// bcal create spy_cal, from(date) replace generate(trading_days)
// tsset trading_days

// foreach a of varlist dl* {
// 	replace `a' = `a'[_n-1] if missing(`a')
// }
// foreach a of varlist lda* {
// 	replace `a' = `a'[_n-1] if missing(`a')
// }
// foreach a of varlist nmf* {
// 	replace `a' = `a'[_n-1] if missing(`a')
// }
