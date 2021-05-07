cls
clear
set scheme s2color
// set scheme s1mono
eststo clear

// Python can be called from within stata, perhaps do a master stata file

//--------------------------------------------------
// DATA PREPARATION
//--------------------------------------------------

// Parse minutes
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\data\dataExport.csv", clear
tostring release, replace
generate date = date(release,"YMD"), after(release)
format %tdDD/NN/CCYY date
label variable date "Release date"
drop release 
gen dl_nettone_change = dl_nettone[_n] - dl_nettone[_n-1], after(dl_nettone)
gen dl_uncert_change = dl_uncert[_n] - dl_uncert[_n-1], after(dl_uncert)
save "./data/tone.dta", replace
// Minutes descriptives
sort date
line dl_nettone date
graph export ".\img\nettoneProgression.png", as(png) replace
line dl_nettone_change date
graph export ".\img\nettoneChangeProgression.png", as(png) replace
line dl_uncert date
graph export ".\img\uncertProgression.png", as(png) replace
line dl_uncert_change date
graph export ".\img\uncertChangeProgression.png", as(png) replace
line dl_nettone dl_uncert date
graph export ".\img\baseProgression.png", as(png) replace
line dl_nettone_change dl_uncert_change date
graph export ".\img\changeProgresion.png", as(png) replace
preserve
keep if year>2005
line proptopic3 proptopic2 proptopic6 proptopic8 date
graph export ".\img\topicProportionProgression.png", as(png) replace
restore

// Parse financial data
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date
save "./data/spyYF.dta", replace

// Merge
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\tone.dta", 
sort date // Just to make sure
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!

// Create derivative variables
gen fomcdummy=cond(missing(year),0,1)
gen R_24 = (close-close[_n-1])/close[_n-1], after(close)
label var R_24 "Close-close diff"
gen R_intra = (close-open)/open, after(R_24)
label var R_intra "Intraday return, close-open diff"
gen vola_temp = high-low, after(close)
sum(vola_temp)
gen V = (high-low)/r(sd), after(vola_temp)
// by link: gen dl_nettone_change = dl_nettone[_n]-dl_nettone[_n-1] if _merge==3, after(dl_nettone)

// Set dataset up as timeseries to use lag operators in regressions
bcal create spy_cal, from(date) replace generate(trading_days)
tsset trading_days

save ".\3 dataPrepared.dta", replace

keep if _merge==3
br