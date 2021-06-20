cls
clear
// set scheme s2color
set scheme s1mono
eststo clear
set graphics off

use ".\data\main.dta", clear

tsset trading_days
sort trading_days

// -----------------------------------------------------
// DAY EFFECT REGRESSION - fomcdummy
// -----------------------------------------------------
eststo clear
local dep "V R_intra R_24 bond vix" //bond yield vix"
foreach var in `dep'{
	quietly eststo, title(`dep'): reg `var' fomcdummy, r
	estadd scalar cnt = 225
}
esttab, ar2 nonum replace b(3) label scalars(cnt) sfmt(%9.0g)
esttab using ".\tex\fomcdummyreg.txt", ar2 tex nonum replace b(3) scalars(cnt) sfmt(%9.0g)

exit
// coefplot est*, drop(_cons) xline(0)

// -----------------------------------------------------
// NAIVE TONE IMPACT
// -----------------------------------------------------

// MULTIVAR VERSION -  THAT'S FINAL AND IN THE DRAFT NOW
eststo clear
local vars1 = "dl_pos dl_neg dl_uncert dissent" // Drop nettone because it is a linear combination of pos and neg
local vars2 = "dl_nettone dl_uncert dissent"
local controls = "interest unemployment recession"
local deps "V R_intra"
eststo clear
foreach dep in `deps'{
	qui eststo: reg `dep' `vars1', r
	qui eststo: reg `dep' `vars2', r
	qui eststo: reg `dep' `vars1' `controls', r
	qui eststo: reg `dep' `vars2' `controls', r
}
esttab, ar2 nonum replace b(3) label order(dl_nettone dl_pos dl_neg dl_uncert dissent interest unemployment recession)
esttab using ".\tex\naiveToneImpact.txt", ar2 nonum replace b(3) label order(dl_nettone dl_pos dl_neg dl_uncert dissent interest unemployment recession) float tex

exit


// -----------------------------------------------------
// TOPIC-TONE IMPACT
// -----------------------------------------------------
// Note: Drop the first topic to avoid quasi-multicollinearity! Stata doesn't complain because topic weights don't add up to 1 precisely, but margin is less than 1%, so standard errors will be large and significance will suffer
// Amendment: Drop constant instead, interpretations are cleaner that way! - nocons
// Amendment the second: Multicoll isn't a concern for the tone scores, only for the proportion regressions!

cls
// QUALITATIVE REGRESSIONS
local deps = "V R_intra"
local vars = "nmfnettone nmfpos nmfneg nmfuncert"
local controls = "interest unemployment recession"
foreach dep in `deps'{
	local cnt = 1
	foreach var in `vars'{
		eststo clear
		quietly eststo: reg `dep' `var'*, r
		quietly eststo: reg `dep' `var'* `controls', r
// 		local naive = subinstr("`var'","nmf","dl_",1)
//		Adding naive tone as control is non-sensical interpretation-wise, it can't be fixed with a changing topic-tone!
// 		quietly eststo: reg `dep' `var'* `naive', nocons r
// 		quietly eststo: reg `dep' `var'* `naive' `controls', nocons r		
		di ""
		di "`dep' `var' `naive'"
		esttab, mtitle nonum ar2
		if `cnt'>1{
			esttab using ".\tex\nmf`dep'impact.txt", mtitle ar2 tex float nonum append b(3)
		}
		else{
			esttab using ".\tex\nmf`dep'impact.txt", mtitle ar2 tex float nonum replace b(3)
		}
		local ++cnt
	}
}

exit



// QUANTITATIVE REGRESSIONS
cls
eststo clear
local deps = "V R_intra"
local controls = "interest unemployment recession"
foreach dep in `deps'{
	quietly eststo: reg `dep' nmfprop*, r nocons
	quietly eststo: reg `dep' nmfprop* `controls', r nocons
}
esttab, mtitle nonum ar2 label
esttab using ".\tex\nmfprop.txt", mtitle ar2 label tex float nonum replace b(3)

exit









// ---------- ARCHIVE


// // coefplot est*, drop(_cons) xline(0)
// // eststo clear
// quietly eststo: reg V L(1/1).V dl_nettone, r
// quietly eststo: reg V L(1/1).V dl_uncert, r
// quietly eststo: reg V L(1/1).V dissent, r
// quietly eststo: reg V L(1/1).V dl_nettone dl_uncert dissent, r
// esttab using ".\tex\impact.txt", ar2 indicate("Lagged volatility" = L*.V) tex float nonum append b(3)
// // coefplot est*, drop(_cons) xline(0)
//
// // Return
// eststo clear
// quietly eststo: reg R_intra dl_nettone, r
// quietly eststo: reg R_intra dl_uncert, r
// quietly eststo: reg R_intra dissent, r
// quietly eststo: reg R_intra dl_nettone dl_uncert dissent, r
// // esttab using ".\tex\impact.txt", ar2 tex float nonum append b(3)
// //
// // eststo clear
// quietly eststo: reg R_24 dl_nettone, r
// quietly eststo: reg R_24 dl_uncert, r
// quietly eststo: reg R_24 dissent, r
// quietly eststo: reg R_24 dl_nettone dl_uncert dissent, r
// esttab using ".\tex\impact.txt", ar2 tex float nonum append b(3)

// eststo clear
// quietly eststo: reg V L(1/1).V ldaprop*, nocons r
// quietly eststo: reg V ldaprop*, nocons r
// quietly eststo: reg R_intra ldaprop*, nocons r
// quietly eststo: reg R_24 ldaprop*, nocons r
// esttab, ar2 indicate("Lagged volatility" = L*.V)
// Financial markets and consumption are significant. Coeff of consumption is negative, thus talk about consumption can be assumed to overall be more positive than negative. - Can I control for the tone of consumption to determine whether the quantity is actually relevant? Not really, best to just use general macro variables for that

// Uncert LDA
// eststo clear
// quietly eststo: reg V L(1/1).V ldauncert*, nocons r
// quietly eststo: reg V ldauncert*, nocons r
// quietly eststo: reg R_intra ldauncert*, nocons r
// quietly eststo: reg R_24 ldauncert*, nocons r
// esttab, ar2 indicate("Lagged volatility" = L*.V)

// Net tone LDA
// eststo clear
// quietly eststo: reg V L(1/1).V ldanettone*, nocons r
// quietly eststo: reg V ldanettone*, nocons r
// quietly eststo: reg R_intra ldanettone*, nocons r
// quietly eststo: reg R_24 ldanettone*, nocons r
// esttab, ar2 indicate("Lagged volatility" = L*.V)


local vars = "dl_nettone dl_pos dl_neg dl_uncert dissent"
local deps "V R_intra R_24 bond vix"
foreach dep in `deps'{
	eststo clear
	local res = ""
	foreach var in `vars'{
		di "`dep' `var'"
		qui eststo `var': reg `dep' `var', r
		local res "`res' `var'"
	}
	esttab, ar2 nonum replace b(3) nocons label
	eststo stacked: appendmodels `res'
	esttab stacked, ar2 nonum replace b(3) nocons label
	esttab stacked using "./tex/`dep'ImpactReg.txt", tex float noobs nonum nocons replace b(3)
}
exit

// ADD CONTROLS
local vars = "dl_nettone dl_pos dl_neg dl_uncert dissent"
local deps "V R_intra R_24"
foreach dep in `deps'{
	eststo clear
	local res = ""
	foreach var in `vars'{
		di "`dep' `var'"
		qui eststo `var': reg `dep' `var' interest unemployment recession, r
		local res "`res' `var'"
	}
	esttab, ar2 nonum replace b(3) nocons label
// 	eststo stacked: appendmodels `res'
// 	esttab stacked using "./tex/`dep'ImpactReg.txt", tex float noobs nonum nocons replace b(3)
}

exit


// QUANTITATIVE - Appendix
eststo clear
// quietly eststo: reg V L(1/1).V nmfprop*, nocons r
quietly eststo V: reg V nmfprop*, nocons r
quietly eststo R_intra: reg R_intra nmfprop*, nocons r
quietly eststo R_24: reg R_24 nmfprop*, nocons r
quietly esttab, mtitle nonum noobs
transpose
esttab, mtitle nonum noobs
esttab using ".\tex\nmfPropImpact.txt", mtitle noobs tex float nonum nocons replace b(3)
