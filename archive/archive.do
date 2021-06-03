// Original regressions
reg vix ldanettone*, nocons
matlist r(table)
matrix A = r(table)
matlist A
coefplot matrix(A[1,.]), ci((A[5,.] A[6,.])) xtitle(Days) ytitle(Coefficient) xline(0) ciopts(recast(rcapped)) yline(0, lcolor(black)) title("Coefficient plot of Topic Nettone onto the VIX") horizontal 

exit


// ---------------------------------
// Lda topics nettone predict the Vix
// ---------------------------------
macro drop _all
graph drop _all
matrix drop _all
local min = 0
local max = 500
local step = 30
forvalues val = `min'(`step')`max'{
	local cnames `cnames' " `val'"
}
local maxlag = ceil(sqrt(sqrt(_N))) // Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
foreach topic of varlist ldanettone* {
	di "`topic'"
	matrix dir
	matrix A = J(3,`max'/`step'+1,.)
	matrix rownames A = "b" "ll" "ul"
	matrix colnames A = `cnames'
	forvalues i = `min'(`step')`max' {
		quietly newey L`i'.vix `topic', lag(`maxlag')
		di "index " `i'/`step'+1
		matrix A[1,`i'/`step'+1] = r(table)["b",1]
		matrix A[2, `i'/`step'+1] = r(table)["ll",1]
		matrix A[3, `i'/`step'+1] = r(table)["ul",1]
	}
	coefplot matrix(A[1,.]), ci((A[2,.] A[3,.])) xtitle(Days) ytitle(Coefficient) recast(line) ciopts(recast(rline) ///
		lpattern(dash)) yline(0, lcolor(black)) vertical title(`topic') name(`topic')
	local graphs "`graphs' `topic'"
	matrix drop A
}
di "`graphs'"
graph combine `graphs'
graph export ".\img\ldaTopicsNettonePredictVix.png", as(png) replace



// ---------------------------------
// Lda topics uncert predict the Vix
// ---------------------------------

macro drop _all
graph drop _all
matrix drop _all
local min = 0
local max = 500
local step = 30
forvalues val = `min'(`step')`max'{
	local cnames `cnames' " `val'"
}
local maxlag = ceil(sqrt(sqrt(_N))) // Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
foreach topic of varlist ldauncert* {
	di "`topic'"
	matrix dir
	matrix A = J(3,`max'/`step'+1,.)
	matrix rownames A = "b" "ll" "ul"
	matrix colnames A = `cnames'
	forvalues i = `min'(`step')`max' {
		quietly newey L`i'.vix `topic', lag(`maxlag')
		di "index " `i'/`step'+1
		matrix A[1,`i'/`step'+1] = r(table)["b",1]
		matrix A[2, `i'/`step'+1] = r(table)["ll",1]
		matrix A[3, `i'/`step'+1] = r(table)["ul",1]
	}
	coefplot matrix(A[1,.]), ci((A[2,.] A[3,.])) xtitle(Days) ytitle(Coefficient) recast(line) ciopts(recast(rline) ///
		lpattern(dash)) yline(0, lcolor(black)) vertical title(`topic') name(`topic')
	local graphs "`graphs' `topic'"
	matrix drop A
}
di "`graphs'"
graph combine `graphs'
graph export ".\img\ldaTopicsUncertPredictVix.png", as(png) replace


// ---------------------------------
// Nmf topics nettone predict the Vix
// ---------------------------------

macro drop _all
graph drop _all
matrix drop _all
local min = 0
local max = 500
local step = 30
forvalues val = `min'(`step')`max'{
	local cnames `cnames' " `val'"
}
local maxlag = ceil(sqrt(sqrt(_N))) // Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
foreach topic of varlist nmfnettone* {
	di "`topic'"
	matrix dir
	matrix A = J(3,`max'/`step'+1,.)
	matrix rownames A = "b" "ll" "ul"
	matrix colnames A = `cnames'
	forvalues i = `min'(`step')`max' {
		quietly newey L`i'.vix `topic', lag(`maxlag')
		di "index " `i'/`step'+1
		matrix A[1,`i'/`step'+1] = r(table)["b",1]
		matrix A[2, `i'/`step'+1] = r(table)["ll",1]
		matrix A[3, `i'/`step'+1] = r(table)["ul",1]
	}
	coefplot matrix(A[1,.]), ci((A[2,.] A[3,.])) xtitle(Days) ytitle(Coefficient) recast(line) ciopts(recast(rline) ///
		lpattern(dash)) yline(0, lcolor(black)) vertical title(`topic') name(`topic')
	local graphs "`graphs' `topic'"
	matrix drop A
}
di "`graphs'"
graph combine `graphs'
graph export ".\img\nmfTopicsNettonePredictVix.png", as(png) replace


// ---------------------------------
// Nmf topics uncert predict the Vix
// ---------------------------------

macro drop _all
graph drop _all
matrix drop _all
local min = 0
local max = 500
local step = 30
forvalues val = `min'(`step')`max'{
	local cnames `cnames' " `val'"
}
local maxlag = ceil(sqrt(sqrt(_N))) // Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
foreach topic of varlist nmfuncert* {
	di "`topic'"
	matrix dir
	matrix A = J(3,`max'/`step'+1,.)
	matrix rownames A = "b" "ll" "ul"
	matrix colnames A = `cnames'
	forvalues i = `min'(`step')`max' {
		quietly newey L`i'.vix `topic', lag(`maxlag')
		di "index " `i'/`step'+1
		matrix A[1,`i'/`step'+1] = r(table)["b",1]
		matrix A[2, `i'/`step'+1] = r(table)["ll",1]
		matrix A[3, `i'/`step'+1] = r(table)["ul",1]
	}
	coefplot matrix(A[1,.]), ci((A[2,.] A[3,.])) xtitle(Days) ytitle(Coefficient) recast(line) ciopts(recast(rline) ///
		lpattern(dash)) yline(0, lcolor(black)) vertical title(`topic') name(`topic')
	local graphs "`graphs' `topic'"
	matrix drop A
}
di "`graphs'"
graph combine `graphs'
graph export ".\img\nmfTopicsUncertPredictVix.png", as(png) replace

exit
