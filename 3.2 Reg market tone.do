cls
clear
eststo clear

// Parse dates of both data sets
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\data\dataExport.csv", clear

tostring release, replace
generate date = date(release,"YMD"), after(release)
format %tdDD/NN/CCYY date
label variable date "Release date"
drop release filteredparagraphs 
save "./data/tone.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear

tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date
save "./data/spyYF.dta", replace

// Merge
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\tone.dta", keep(match) nogen
sort date
gen return = close-open, after(close)

br

quietly eststo: reg return lmneg
quietly eststo: reg return lmneg lmpos
quietly eststo: reg return lmneg lmpos lmpol lmsub
esttab, p r2
eststo clear
quietly eststo: reg return hvneg
quietly eststo: reg return hvneg hvpos
quietly eststo: reg return hvneg hvpos hvpol hvsub
esttab, p r2

// TODO figure out how to properly interpret these regressions - see Schmeling Wagner

br
