capture program drop impact

// INPUTS
// 1: dependent variable (vix)
// 2: varlist (eg ldanettone*)
// 3: min 
// 4: max
// 5: step

program define impact
// 	macro drop _all // Not a good idea, drops the input variables
	set graphics off
	graph drop _all
	matrix drop _all
	noisily di as text "Inputs: `1' `2' `3' `4' `5'"
	args regressand regressor min max step
	local max = `4' - mod(`4',`5')
	foreach val of numlist `min'(`step')`max'{
		local cnames "`cnames'  `val'"
	}
	local maxlag = ceil(sqrt(sqrt(_N))) 
	// Max lag as the fourth root of T, see Greene (Econometric Analysis, 7th edition, section 20.5.2, p. 960).
	foreach topic of varlist `regressor' {
		di as result "`topic'"
		local sorlabel: variable label `topic'
		matrix dir
		matrix A = J(4,`max'/`step'+1,.)
		matrix rownames A = "b" "ll" "ul" "at"
		matrix colnames A = `cnames'
		forvalues i = `min'(`step')`max' {
			quietly newey S`i'.F`i'.`regressand' `regressor', lag(`maxlag')
				// Fi : lead the dependent variable by i periods
				// Si : Difference between var in t and t-i
				// Both combined give the the difference between t and t+i
				// Not sure whether double TS operators work correctly, let's hope they do
			di as text "index " `i'/`step'+1
			matrix A[1,colnumb(A,"`i'")] = r(table)["b","`topic'"]
			matrix A[2,colnumb(A,"`i'")] = r(table)["ll","`topic'"]
			matrix A[3,colnumb(A,"`i'")] = r(table)["ul","`topic'"]
			matrix A[4,colnumb(A,"`i'")] = `i'
// 			matlist A
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
	graph combine `graphs', title("`regressor' impact on `regressand'") iscale(0.35)

end

// Efficiency could perhaps be improved by grabbing all coefficients at once in the inner loop.
// Would require a three-dimensional data structure and a for loop for subgraph construction though.