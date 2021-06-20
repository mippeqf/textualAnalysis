cls
clear
// set scheme s2color
set scheme s1mono
eststo clear
set graphics on

use ".\data\main.dta", clear

//--------------------------------------------------
// Descriptive charts
//--------------------------------------------------

// Raw word count
sort date
tsset date // Set timeseries to 'natural dates' to get even spacing. As soon as we're not looking solely at financial data, natural dates are the proper series. When generating lags for financial ts, remember to temporarily switch back to the bcal!

label var wordcntfiltered "Word count"
label var paracnt "Paragraph count"
tsline paracnt, yaxis(1) lcolor(maroon) || tsline wordcntfiltered, yaxis(2) lcolor(navy) legend(order(2 "Words (filtered)" 1 "Paragraphs")) 
graph export ".\img\desc\totalNumberWords.png", as(png) replace

// ABSOLUTE TONE FIGURE
gen rectemp = recession*300-6
twoway (area rectemp date, color(gs14) base(-6)) (tsline poscnt negcnt uncertcnt, ///
lcolor(forest_green cranberry navy)), legend(region(lwidth(0)) label(1 "Recession") label(2 "Positive") label(3 "Negative") label(4 "Uncertain")) ///
 ytitle("Word count") xtitle("")
graph export ".\img\desc\abscontentCounts.png", as(png) replace
drop rectemp

// RELATIVE TONE FIGURE
gen relpos = poscnt/wordcntfiltered
gen relneg = negcnt/wordcntfiltered
gen relunc = uncertcnt/wordcntfiltered
quietly sum relneg
gen rectemp = recession*(r(max)+0.01)
twoway (area rectemp date, color(gs14)) (tsline relpos relneg relunc, lcolor(forest_green cranberry navy)), ///
 ytitle("Term fraction") xtitle("") yline(0.06) ///
legend(region(lwidth(0)) label(1 "Recession") label(2 "Positive") label(3 "Negative") label(4 "Uncertain"))
graph export ".\img\desc\relContentCounts.png", as(png) replace

// SUMMARY STATS TABLE
// tsline paracnt, lcolor(navy maroon)  ytitle("Total paragraph count") xtitle("")
// graph export ".\img\totalNumberParagraphs.png", as(png) replace
gen avgwordsperpara = wordcntfiltered/paracnt
// gen avgwordsperparaRAW = wordcntraw/paracnt
// tsline avgwordsperpara avgwordsperparaRAW, lcolor(navy maroon)  ytitle("Total paragraph count") xtitle("")
// graph export ".\img\avgWordsPerParagraph.png", as(png) replace
estpost sum wordcntfiltered wordcntraw paracnt avgwordsperpara
esttab, cells("mean sd min max") nonumber nomtitle noobs

// NAIVE TONE FIGURE
capture drop rectemp
gen rectemp = recession*15-6
twoway (area rectemp date, color(gs14) base(-6)) (tsline dl_nettone dl_uncert dl_pos dl_neg, lcolor(navy orange forest_green cranberry) legend(region(lwidth(0)) label(1 "Recession"))), ytitle("Tone score") xtitle("") yline(0) 
graph export ".\img\desc\naiveToneProg.png", as(png) replace
