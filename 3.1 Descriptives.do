cls
clear
// set scheme s2color
set scheme s1mono
eststo clear
set graphics off

use ".\data\3 dataPrepared.dta", clear

//--------------------------------------------------
// Descriptive charts
//--------------------------------------------------

// Raw word count
sort date
tsset date // Set timeseries to 'natural dates' to get even spacing. As soon as we're not looking solely at financial data, natural dates are the proper series. When generating lags for financial ts, remember to temporarily switch back to the bcal!

tsline wordCntFiltered, lcolor(navy) plotregion(style(none)) ytitle("Total word count") xtitle("")
graph export ".\img\totalNumberWords.png", as(png) replace

tsline poscnt negcnt uncertcnt, ///
lcolor(forest_green cranberry navy) legend(region(lwidth(0)) label(1 "Positive") label(2 "Negative") label(3 "Uncertain")) ///
plotregion(style(none)) ytitle("Word count") xtitle("")
graph export ".\img\abscontentCounts.png", as(png) replace

gen relpos = poscnt/wordCntFiltered
gen relneg = negcnt/wordCntFiltered
gen relunc = uncertcnt/wordCntFiltered
quietly sum relneg
gen rectemp = recession*(r(max)+0.01)
twoway (area rectemp date, color(gs14)) (tsline relpos relneg relunc, lcolor(forest_green cranberry navy)), ///
plotregion(style(none)) ytitle("Term fraction") xtitle("") yline(0.06) ///
legend(region(lwidth(0)) label(1 "Recession") label(2 "Positive") label(3 "Negative") label(4 "Uncertain"))
graph export ".\img\relContentCounts.png", as(png) replace
drop rectemp

// Tone
gen rectemp = recession*12-6
twoway (area rectemp date, color(gs14) base(-6)) (tsline dl_nettone dl_uncert, lcolor(maroon navy) legend(region(lwidth(0)) label(1 "Recession") label(2 "Net tone") label(3 "Uncertainty"))), plotregion(style(none)) ytitle("Tone score") xtitle("") yline(0) 
graph export ".\img\DLtone.png", as(png) replace

// Topic proportions done in Python!
// Stata doesn't support stacked area charts out of the box

// Macro descriptives