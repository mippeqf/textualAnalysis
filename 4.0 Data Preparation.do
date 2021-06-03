cls
clear
set scheme s2color
// set scheme s1mono
eststo clear
set graphics off

// Python can be called from within stata, perhaps do a master stata file

//--------------------------------------------------
// Prepare daily variables (financial)
//--------------------------------------------------

// Parse minutes
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\data\dataExport.csv", clear
tostring release, replace
generate date = date(release,"YMD"), after(release)
format %tdDD/NN/CCYY date
label variable date "Release date"
drop release 
// gen dl_nettone_change = dl_nettone[_n] - dl_nettone[_n-1], after(dl_nettone)
// gen dl_uncert_change = dl_uncert[_n] - dl_uncert[_n-1], after(dl_uncert)
// Delete two of three observations referring to the same document
drop if strpos(link, "#") // Specific to this dataset!
save "./data/tone.dta", replace


// Parse spy
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date

gen R_24 = (close-close[_n-1])/close[_n-1], after(close)
label var R_24 "Close-close diff"
gen R_intra = (close-open)/open, after(R_24)
label var R_intra "Intraday return, close-open diff"
gen vola_temp = high-low, after(close)
sum(vola_temp)
gen V = (high-low)/r(mean), after(vola_temp)
drop vola_temp
label var V "Intraday volatility"
// by link: gen dl_nettone_change = dl_nettone[_n]-dl_nettone[_n-1] if _merge==3, after(dl_nettone)

save "./statics/spy.dta", replace


// Parse vix
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\VIXCLS.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename vixcls vix
save ".\statics\vix.dta", replace

// Parse treasuryyield
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\DGS10.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename dgs10 yield
save ".\statics\yield.dta", replace


// -------------- Merge
use "./data/tone.dta", clear
sort date

merge 1:1 date using ".\statics\spy.dta", nogen
merge 1:1 date using ".\statics\vix.dta", nogen
merge 1:1 date using ".\statics\yield.dta", nogen

gen fomcdummy=cond(missing(year),0,1)

sort date

// ------------- Timeseries setup

// Set dataset up as timeseries to use lag operators in regressions
bcal create spy_cal, from(date) replace generate(trading_days)
// bcal create fomc_cal, from(date) replace generate(fomc_date)
// bcal create spy_cal, from(date) replace generate(spy_date)
order trading_days, after(date)
tsset trading_days

// -------------- Prep monthly merge

// Unique identifier for month (xth month since 1960m1)
gen month = mofd(date), after(date)

save "./data/main.dta", replace


// -----------------------------------------------------------------
// Prepare monthly vars (macro)
// -----------------------------------------------------------------

// ---------- Prepare monthly data
local data "BOPGSTB CPIAUCSL FEDFUNDS UNRATE USREC"
foreach str in `data'{
	di "./statics/`str'.csv"
	import delimited "./statics/`str'.csv", clear
	generate month = mofd(date(date,"YMD")), after(date)
	drop date
	save "./statics/`str'.dta", replace
}

use ".\data\main.dta", clear
foreach str in `data'{
	di "`str'"
	merge m:1 month using "./statics/`str'.dta", nogen
}
sort date // Merging messes up the ordering somehow
drop if missing(date) // Only missing for exceeding control variables

rename bopgstb tradebalance
rename cpiaucsl cpiaucsl
rename fedfunds interest
rename unrate unemployment
rename usrec recession

drop if date < date("29/01/1993", "DMY") // Vix goes back to 1990

save ".\data\main.dta", replace
