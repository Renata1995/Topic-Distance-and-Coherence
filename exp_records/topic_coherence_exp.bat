FOR %%A IN (10 20 30 40 50 60 70 80 90) DO (
	FOR %%B IN (t c b) DO (
		FOR %%C IN (3 4 5 6 7 8 9 10 15 20 30 50 80 100) DO (
			python reuters_LDA tcReader.py %%B %%C pp_reuters %%A
		)
	)
)
