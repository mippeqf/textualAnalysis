cls
clear
// set scheme s2color
set scheme s1mono
eststo clear
set graphics off

use ".\data\marketImpact.dta", clear

//--------------------------------------------------
// Descriptive charts
//--------------------------------------------------

// Raw word count
sort date
tsset date // Set timeseries to 'natural dates' to get even spacing. As soon as we're not looking solely at financial data, natural dates are the proper series. When generating lags for financial ts, remember to temporarily switch back to the bcal!

tsline paracnt, yaxis(1) lcolor(maroon) ytitle("") || tsline wordcntfiltered, yaxis(2) lcolor(navy) plotregion(style(none)) xtitle("") ytitle("", axis(1)) legend(order(2 "Words (right)" 1 "Paragraphs (left)")) 
graph export ".\img\desc\totalNumberWords.png", as(png) replace

// tsline paracnt, lcolor(navy maroon) plotregion(style(none)) ytitle("Total paragraph count") xtitle("")
// graph export ".\img\totalNumberParagraphs.png", as(png) replace
//
gen avgwordsperpara = wordcntfiltered/paracnt
// gen avgwordsperparaRAW = wordcntraw/paracnt
// tsline avgwordsperpara avgwordsperparaRAW, lcolor(navy maroon) plotregion(style(none)) ytitle("Total paragraph count") xtitle("")
// graph export ".\img\avgWordsPerParagraph.png", as(png) replace

tsline poscnt negcnt uncertcnt, ///
lcolor(forest_green cranberry navy) legend(region(lwidth(0)) label(1 "Positive") label(2 "Negative") label(3 "Uncertain")) ///
plotregion(style(none)) ytitle("Word count") xtitle("")
graph export ".\img\desc\abscontentCounts.png", as(png) replace

gen relpos = poscnt/wordcntfiltered
gen relneg = negcnt/wordcntfiltered
gen relunc = uncertcnt/wordcntfiltered
quietly sum relneg
gen rectemp = recession*(r(max)+0.01)
twoway (area rectemp date, color(gs14)) (tsline relpos relneg relunc, lcolor(forest_green cranberry navy)), ///
plotregion(style(none)) ytitle("Term fraction") xtitle("") yline(0.06) ///
legend(region(lwidth(0)) label(1 "Recession") label(2 "Positive") label(3 "Negative") label(4 "Uncertain"))
graph export ".\img\desc\relContentCounts.png", as(png) replace
drop rectemp

estpost sum wordcntfiltered wordcntraw paracnt avgwordsperpara
esttab, cells("mean sd min max") nonumber nomtitle noobs

// Tone
gen rectemp = recession*12-6
twoway (area rectemp date, color(gs14) base(-6)) (tsline dl_nettone dl_uncert, lcolor(maroon navy) legend(region(lwidth(0)) label(1 "Recession") label(2 "Net tone") label(3 "Uncertainty"))), plotregion(style(none)) ytitle("Tone score") xtitle("") yline(0) 
graph export ".\img\desc\DLtone.png", as(png) replace

// Topic proportions done in Python!
// Stata doesn't support stacked area charts out of the box

// Macro descriptives