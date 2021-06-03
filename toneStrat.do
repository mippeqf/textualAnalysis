cls
set scheme s1mono

use "data\main.dta", clear

gen pseudodate = _n, after(date) // Pseuodate will do, bcal probably does the same
tsset pseudodate
tsfill

gen tone = nmfnettone2 if nmfnettone2!=0
keep tone close pseudodate date

gen pl = tone * (close[_n+300]-close[_n]) if !missing(tone)
gen cumpl = sum(pl)
sum pl
di r(sum)
twoway (line cumpl date, lcolor(navy) yaxis(1)) (line tone date, yline(0) yaxis(2) lcolor(maroon))
graph export "img\pred\topic2strat.png", replace