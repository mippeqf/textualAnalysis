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
foreach var of varlist nmf*1{
	label var `var' "Economic activity"
}
foreach var of varlist nmf*2{
	label var `var' "Policy action"
}
foreach var of varlist nmf*3{
	label var `var' "Economic outlook"
}
foreach var of varlist nmf*4{
	label var `var' "Unemployment"
}
foreach var of varlist nmf*5{
	label var `var' "Financial Markets"
}
foreach var of varlist nmf*6{
	label var `var' "Inflation"
}
save "./data/tone.dta", replace


// Parse spy
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\spyYF.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date dividends stocksplits
rename date1 date

gen R_24 = (close-close[_n-1])/close[_n-1], after(close)
label var R_24 "R_{24}"
gen R_intra = (close-open)/open, after(R_24)
label var R_intra "R_{intra}"
gen vola_temp = high-low, after(close)
sum(vola_temp)
gen V = (high-low)/r(mean), after(vola_temp)
drop vola_temp
label var V "V"
// by link: gen dl_nettone_change = dl_nettone[_n]-dl_nettone[_n-1] if _merge==3, after(dl_nettone)
rename close spy
label var spy "S&P500"
save "./statics/spy.dta", replace


// Parse vix
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\VIXCLS.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename vixcls vix
label var vix "VIX"
save ".\statics\vix.dta", replace

// Parse treasuryyield
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\DGS10.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
rename dgs10 yield
label var yield "10-year treasury yield"
save ".\statics\yield.dta", replace

// Parse bofa bond index
import delimited "C:\Users\Markus\Desktop\BA\textualAnalysis\statics\BOND.csv", clear
tostring date, replace
generate date1 = date(date,"YMD"), after(date)
format %tdDD/NN/CCYY date1
drop date
rename date1 date
label var bond "BofA Bond Index"
save ".\statics\bond.dta", replace

// -------------- Merge
use "./data/tone.dta", clear
sort date

merge 1:1 date using ".\statics\spy.dta", nogen
merge 1:1 date using ".\statics\vix.dta", nogen
merge 1:1 date using ".\statics\yield.dta", nogen
merge 1:1 date using ".\statics\bond.dta", nogen

gen fomcdummy=cond(missing(year),0,1)
label var fomcdummy "Release day dummy"
label var dl_nettone "naiveNettone"
label var dl_uncert "naiveUncert"
label var dl_pos "naivePos"
label var dl_neg "naiveNeg"


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
label var tradebalance "Tradebalance"
rename cpiaucsl cpiaucsl
label var cpiaucsl "Consumer Price Index"
rename fedfunds interest
label var interest "Federal Funds Rate"
rename unrate unemployment
label var unemployment "Unemployment Rate"
rename usrec recession
label var recession "Recession"

drop if date < date("29/01/1993", "DMY") // Vix goes back to 1990

save ".\data\main.dta", replace
