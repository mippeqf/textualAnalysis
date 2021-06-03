capture program drop impact

// INPUTS
// 1: dependent variable (vix)
// 2: varlist (eg ldanettone*)
// 3: min 
// 4: max
// 5: step

program define impact
	syntax varlist, regressand(varlist min=1 max=1) [max(integer 500) step(integer 30) lag]
	// To implement min&max limit on varlist = 1 if lag option is specified!
// 	macro drop _all // Not a good idea, drops the input variables
	set graphics off
	graph drop _all
	matrix drop _all
	noisily di as text "Inputs: `1' `2' `3' `4' `5'"
	noisily di as text "Inputs: `varlist' `regressand' `max' `step' `lag'"
// 	args regressand regressor max step lag
	local min = 1 // Hardcoded, not really needed as an option
		// Also, foolproofing: Including 0 messes up the regression, see below
	local max = `max'+1 - mod(`max',`step')
	foreach val of numlist `min'(`step')`max'{
		local cnames "`cnames'  `val'"
	}
	local maxlag = ceil(sqrt(sqrt(_N))) 
	// Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
	foreach topic of varlist `varlist' {
		di as result "`topic'"
		local sorlabel: variable label `topic'
		matrix dir
		matrix A = J(4,`max'/`step'+1,.)
		matrix rownames A = "b" "ll" "ul" "at"
		matrix colnames A = `cnames'
		forvalues i = `min'(`step')`max' {
			if "`lag'" == ""{
				quietly newey S`i'.F`i'.`regressand' `varlist', lag(`maxlag')
				// Fi : lead the dependent variable by i periods
				// Si : Difference between var in t and t-i
				// Both combined give the the difference between t and t+i
				// Not sure whether double TS operators work correctly, let's hope they do
				// Always start with 1 as min, with 0 you're using the scalar 0 as a regressor I believe
				di as text "Iteration " (`i'-1)/`step'+1 ": Computing `topic' impact onto `regressand' differential on day " `i' " after event"
// 				di as text "S`i'.F`i'.`regressand' `varlist'"
// 				matlist r(table)
				matrix A[1,colnumb(A,"`i'")] = r(table)["b","`topic'"]
				matrix A[2,colnumb(A,"`i'")] = r(table)["ll","`topic'"]
				matrix A[3,colnumb(A,"`i'")] = r(table)["ul","`topic'"]
				matrix A[4,colnumb(A,"`i'")] = `i'
// 				matlist A
			} 
			else { 
				quietly newey `regressand' L`i'.`varlist', lag(`maxlag')
				di as text "Iteration " (`i'-1)/`step'+1 ": Computing `topic' impact onto `regressand' level on day " `i' " before event"
// 				di as text "`regressand' L`i'.`varlist'"
// 				matlist r(table)
				matrix A[1,colnumb(A,"`i'")] = r(table)["b",1]
				matrix A[2,colnumb(A,"`i'")] = r(table)["ll",1]
				matrix A[3,colnumb(A,"`i'")] = r(table)["ul",1]
				matrix A[4,colnumb(A,"`i'")] = `i'
// 				matlist A
			}
		}
		matlist A
		coefplot matrix(A[1]), ci((A[2] A[3])) at(A[4]) xtitle(Days) ///
			ytitle(Coefficient) recast(line) ciopts(recast(rline) ///
			lpattern(dash)) yline(0, lcolor(black)) vertical title(`sorlabel') ///
			name(`topic') xlabel(#5, labsize(medium)) ylabel(#5, labsize(medium))
		local graphs "`graphs' `topic'"
		matrix drop A
		local i = `i'+1
	}
	di as result "Graphs: `graphs'"
	set graphics on
	ds `varlist'
// 	di r(varlist)
	di wordcount(r(varlist))
	if wordcount(r(varlist)) > 2{
		graph combine `graphs', title("Impact on `regressand'") iscale(0.25)
	}
	else{
		graph combine `graphs', title("Impact on `regressand'") iscale(0.75)
	}
end

// Efficiency could perhaps be improved by grabbing all coefficients at once in the inner loop.
// Would require a three-dimensional data structure and a for loop for subgraph construction though.