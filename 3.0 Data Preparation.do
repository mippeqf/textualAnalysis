cls
clear
set scheme s2color
// set scheme s1mono
eststo clear
set graphics off

// Python can be called from within stata, perhaps do a master stata file

//--------------------------------------------------
// Preload data and prepare for merging
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
desc

// Parse financial data
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date
save "./statics/spyYF.dta", replace

//--------------------------------------------------
// Merge
//--------------------------------------------------
merge 1:m date using "C:\Users\Markus\Desktop\BA\textualAnalysis\data\tone.dta", // 1:m only because for one date, three different links exist
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!

sort date // Just in case


//--------------------------------------------------
// Create derivative variables
//--------------------------------------------------
gen fomcdummy=cond(missing(year),0,1)
gen R_24 = (close-close[_n-1])/close[_n-1], after(close)
label var R_24 "Close-close diff"
gen R_intra = (close-open)/open, after(R_24)
label var R_intra "Intraday return, close-open diff"
gen vola_temp = high-low, after(close)
sum(vola_temp)
gen V = (high-low)/r(sd), after(vola_temp)
// by link: gen dl_nettone_change = dl_nettone[_n]-dl_nettone[_n-1] if _merge==3, after(dl_nettone)

//--------------------------------------------------
// Set as TS, prepare for macro merge and save
//--------------------------------------------------
// Set dataset up as timeseries to use lag operators in regressions
bcal create spy_cal, from(date) replace generate(trading_days)
// bcal create fomc_cal, from(date) replace generate(fomc_date)
// bcal create spy_cal, from(date) replace generate(spy_date)
order trading_days, after(date)
tsset trading_days

// Unique identifier for month (xth month since 1960m1)
gen month = mofd(date), after(date)

save ".\3 dataPrepared.dta", replace

//--------------------------------------------------
// Prepare&merge macro data
//--------------------------------------------------

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\BOPGSTB.csv", clear
tostring date, replace
generate month = mofd(date(date,"YMD")), after(date)
rename bopgstb tradebalance
drop date
save ".\statics\tb.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\CPIAUCSL.csv", clear
tostring date, replace
generate month = mofd(date(date,"YMD")), after(date)
rename cpiaucsl cpi
drop date
save ".\statics\cpi.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\FEDFUNDS.csv", clear
tostring date, replace
generate month = mofd(date(date,"YMD")), after(date)
rename fedfunds interest
drop date
save ".\statics\interest.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\UNRATE.csv", clear
tostring date, replace
generate month = mofd(date(date,"YMD")), after(date)
rename unrate unemployment
drop date
save ".\statics\unemployment.dta", replace

import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\USREC.csv", clear
tostring date, replace
generate month = mofd(date(date,"YMD")), after(date)
rename usrec recession
drop date
save ".\statics\recession.dta", replace

use ".\3 dataPrepared.dta", clear
merge m:1 month using ".\statics\tb.dta", nogen
merge m:1 month using ".\statics\cpi.dta", nogen
merge m:1 month using ".\statics\interest.dta", nogen
merge m:1 month using ".\statics\unemployment.dta", nogen
merge m:1 month using ".\statics\recession.dta", nogen
sort date // Merging messes up the ordering somehow
drop if missing(date) // Only missing for exceeding control variables

// Package controls into one variable, doesn't work properly yet
local controls "tradebalance cpi interest unemployment recession"

save ".\data\3 dataPrepared.dta", replace