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
gen missingtone = cond(missing(dl_nettone),1,0), before(open)
foreach list in dl* nmf*{
	foreach a of varlist `list'{
		replace `a' = 0 if missing(`a')
	}
}

	
exit

// ---------------------------------
// Impact analyses
// ---------------------------------

// PreReleaseVolatilityDrift
impact V, regressand(V) max(10) step(1) lag
graph export ".\img\pred\PreReleaseVolatilityDrift.png", replace

exit


// Naive tone predictions 
	// DO NOT COMBINE WITH ROUTINE BELOW!! Otherwise you'd control for every other naive tone in the 
	// prediction regressions, but I want them standalone!
local depset = "spy" // dep for dependent variable
local controls = "missingtone"
order dl_nettone dl_pos dl_neg dl_uncert
foreach dep in `depset'{
	local deplabel: var label `dep'
	local graphs = ""
	graph drop _all
	foreach var of varlist dl_*{
		quietly impact `var', regressand(`dep') controls(`controls') keepgraph max(250) step(10)
		local graphs "`graphs' `var'"
	}
	graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with naive tone") //subtitle("Controls: `controls'")
	graph export "./img/pred/`dep'ONnaive.png", replace
}

exit


// Topic-tone predictions - no tone controls
local depset = "spy" // dep for dependent variable
local controls = "missingtone"
local topicset = "nmfnet nmfpos nmfneg nmfuncert"
foreach dep in `depset'{
	local deplabel: var label `dep'
	foreach topic in `topicset'{
		local graphs = ""
		graph drop _all
		foreach var of varlist `topic'*{
			quietly impact `var', regressand(`dep') controls(`controls') keepgraph notopiccontrol max(250) step(10)
			local graphs "`graphs' `var'"
		}
		graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with `topic'") //subtitle("Controls: `controls'")
		graph export "./img/pred/`dep'ON`topic'.png", replace
	}
}

exit


//---------------------------------------------
// STUFF BELOW USES CONTROLS
// --------------------------------------------

// Topic-tone predictions - CONTROL: respective naive tone
local depset = "spy" // dep for dependent variable
local controls = "missingtone"
local topicset = "nmfnettone nmfuncert nmfneg nmfpos"
foreach dep in `depset'{
	local deplabel: var label `dep'
	foreach topic in `topicset'{
		local graphs = ""
		graph drop _all
		foreach var of varlist `topic'*{
			local naive = subinstr("`topic'","nmf","dl_",1)
			di "`var' `topic' `naive'"
			quietly impact `var', regressand(`dep') controls("`naive' `controls'") keepgraph notopiccontrol
			local graphs "`graphs' `var'"
		}
		graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with `topic'") subtitle("Controls: naive tone and `controls'")
		graph export "./img/pred/`dep'ON`topic'ALT.png", replace
	}
}

exit


// Topic-tone predictions - CONTROL: macro trends

local depset = "spy" // dep for dependent variable
local controls = "missingtone interest unemployment recession"
local topicset = "nmfnettone nmfuncert nmfneg nmfpos"
foreach dep in `depset'{
	local deplabel: var label `dep'
	foreach topic in `topicset'{
		local graphs = ""
		graph drop _all
		foreach var of varlist `topic'*{
			di "`var' `topic' `naive'"
			quietly impact `var', regressand(`dep') controls(`controls') keepgraph notopiccontrol
			local graphs "`graphs' `var'"
		}
		graph combine `graphs', iscale(0.5) title("Predicting `deplabel' with `topic'") subtitle("Controls: `controls'")
		graph export "./img/pred/`dep'ON`topic'MACRO.png", replace
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
