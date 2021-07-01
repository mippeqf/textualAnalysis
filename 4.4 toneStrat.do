set scheme s1color
set graphics off

use "data\main.dta", clear

gen pseudodate = _n, after(date) // Pseuodate will do, bcal probably does the same
tsset pseudodate
tsfill

local preds "dl_ nmfpos nmfneg nmfnet nmfuncert"
foreach list in `preds'{
	eststo clear
	set graphics off
	graph drop _all
	local graphs ""
	foreach pred of varlist `list'*{
		capture drop pl cumpl size
		qui sum `pred'
		gen size = (`pred'-r(mean))/r(sd)
		gen pl = size * (spy[_n+250]-spy[_n]) if !missing(size)
		gen cumpl = sum(pl)
		label var cumpl "Cum PL"
// 		qui eststo: reg cumpl spy, r
		qui sum cumpl
		di r(mean)/r(sd) // SUBTRACT RF
		local title: variable label `pred'
		twoway (line cumpl date, lcolor(navy) yaxis(1)) (line spy date, yline(0, lcolor(black)) yaxis(2) lcolor(maroon)), name(`pred') xlabel(#3, labsize(vsmall)) ylabel(#5, labsize(small)) title(`title')
		local graphs "`graphs' `pred'"
	}
	set graphics on
	graph combine `graphs', iscale(0.5) title("`list' strategy") //subtitle("Controls: `controls'")
	graph export "./img/strat/`list'.png", replace
}
exit






















// NOT USED

// PARTIALLING OUT
// Attempt to purge DL nettone loading from individual topic tone combinations
// Although values differ slightly, shape of impact(residuals), regressand(spy) 
// is precisely the same for all topics. WHY? Residuals 
capture drop residnmf*
foreach tone of varlist nmfneg*{
	quietly reg `tone' dl_nettone, r // Doesnae matter whether to use reg or newey
		// Only predictions are used, not SEs/CIs and that's the only point of difference (obvs)
	predict double resid`tone', residuals
	label var resid`tone' "`tone' Residuals"
	replace resid`tone' = 0 if missing(link)
	// 	impact(resid`tone'), regressand(spy)
	// 	drop resid`tone'
}
// impact(residnmfnettone*), regressand(spy)
// exit


if 0{
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
