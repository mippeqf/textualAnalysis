set scheme s1color
set graphics off
import delimited coherenceExport.csv, clear
drop v21
gen id = _n, before(v1)
label var id "Number of topics"
tsset id

// tsline v*, legend(off) yscale(r(-2 -1))

graph drop _all
local i = 1
foreach val of varlist v*{
	label var `val' "Coherence Topic `i'"
	local ++i
	di "`val'"
	tsline `val', legend(off) name(`val') yscale(r(-4 -1)) xscale(r(1 20)) ylabel(#3)
	local graphs "`graphs' `val'"
}
set graphics on
graph combine `graphs', iscale(0.5) // title("Coherence progression of individual topics")
graph export "img/coherenceIndividual.png", replace


import delimited coherenceAggExport.csv, clear
gen id = _n, before(v1)
label var id "Number of topics"
label var v1 "Aggregate coherence"
tsset id
tsline v1, // title("Progression of the aggregated coherence score")
graph export "img/coherenceAgg.png", replace