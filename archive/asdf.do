
do "C:\Users\Markus\Desktop\BA\textualAnalysis\4.0 Data Preparation.do"

drop if missing(vix) // business calendar doesn't include non-weekend holidays! Although regression employs casewise deletion, computing deltas will still introduce problems, thus drop missing observations beforehand

gen pd = 1, after(date)
replace pd = cond(missing(year),pd[_n-1],pd[_n-1]+1) if _n>1
replace pd = . if missing(year)
br
tsset pd
sort date