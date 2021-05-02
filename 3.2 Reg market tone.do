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
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!

quietly eststo: reg return doclevelnettone
quietly eststo: reg return docleveluncert
quietly eststo: reg return doclevelnettone docleveluncert
quietly eststo: reg return nettone*
quietly eststo: reg return uncert*
esttab, p r2

// TODO figure out how to properly interpret these regressions - see Schmeling Wagner
